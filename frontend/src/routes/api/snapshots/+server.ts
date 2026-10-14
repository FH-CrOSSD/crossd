import { db } from "$hook.server";
import { repoRegex } from "$lib/util";
import { error, json } from '@sveltejs/kit';
import { aql } from "arangojs";

const projectsColl = db.collection("projects");
const scansColl = db.collection("scans");
const metricsColl = db.collection("metrics");

/** @type {import('./$types').RequestHandler} */
/**
 * Handles POST requests to /api/snapshots and returns a list of all snapshots for a project stored in the ArangoDB database.
 * 
 * @param request - contains term (part of a valid github owner/name) inside the json body.
 * @returns list of snapshots for a project
 * @throws HTTPError
 */
export async function POST({ request }) {
    let term;
    try {
        term = (await request.json()).term;
    } catch (err: any) {
        console.log(err);
        if (err instanceof SyntaxError) {
            error(400, { message: "Body could not be parsed as json" });
        }
    }

    if (!term || !term.match(repoRegex)) {
        error(422, { message: "Body needs to contain term of alphanumeric characters and -_./" });
    }

    try {
        /**
         * 1. Get scan ids for a specific project
         * 2. Retrieve timestampt for those scans
         */
        const res = await db.query(aql`
        FOR doc IN ${projectsColl}
        FILTER doc.identifier == ${term}
        FOR scan IN doc.scans
        FOR entry IN ${scansColl}
            FILTER scan == entry._id
            FOR metric in ${metricsColl}
                filter metric.scan_id == entry._id
                SORT entry.issuedAt
                RETURN entry.issuedAt
    `);
        let all = await res.all();
        // list of timestamps or empty list
        return json(all ?? []);
    } catch (err: any) {
        console.error(err.message);
    }
}

