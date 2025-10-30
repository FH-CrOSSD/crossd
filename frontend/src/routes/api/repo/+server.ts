import { db } from "$hook.server";
import { repoRegex } from "$lib/util";
import { error, json } from '@sveltejs/kit';
import { aql } from "arangojs";

const repoColl = db.collection("repositories");
const scansColl = db.collection("scans");
const projectsColl = db.collection("projects");

/** @type {import('./$types').RequestHandler} */
/**
 * Handles POST requests to /api/metrics and returns the metrics for a specific project at a specific time (snapshot).
 * 
 * @param request - needs to contains term (part of a valid github owner/name) and timestamp (epoch) in the json body. 
 * @returns metrics of the project from the specified timestamp
 * @throws HTTPError
 */
export async function POST({ request }) {
    let resp;

    try {
        resp = await request.json();
    } catch (err: any) {
        console.log(err);
        if (err instanceof SyntaxError) {
            error(400, { message: "Body could not be parsed as json" });
        }
    }
    const { term, timestamp } = resp;

    if (!term || !term.match(repoRegex)) {
        error(422, { message: "Body needs to contain term of alphanumeric characters and -_./" });
    }

    if (!timestamp || !Number.isFinite(timestamp)) {
        error(422, { message: "Body needs to contain timestamp with numerical value" });
    }

    try {
        /**
         * 1. Get scans for the project
         * 2. Get the scan with the requested timestamp
         * 3. Get the metric and bak metrics for this snapshot
         */
        const res = await db.query(aql`
        FOR project in ${projectsColl}
        FILTER project.identifier == ${term}
        FOR doc IN ${scansColl}
        FILTER doc._id in project.scans
        FILTER doc.issuedAt == ${timestamp}
        LET data = (
            FOR repo IN ${repoColl}
            FILTER repo.scan_id == doc._id
            RETURN UNSET(repo, "_key", "_id", "_rev")
        )
        RETURN {"repository":data[0]}
    `);
        let all = await res.all();
        return json(all[0]);
    } catch (err: any) {
        console.error(err.message);
    }
}

