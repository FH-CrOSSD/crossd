import { db } from "$hook.server";
import { repoRegex } from "$lib/util";
import { error, json } from '@sveltejs/kit';
import { aql } from "arangojs";

const projectsColl = db.collection("projects");
const scansColl = db.collection("scans");

/** @type {import('./$types').RequestHandler} */
/**
 * Handles POST requests to /metrics and returns metrics for a project.
 * 
 * @param request - contains term (part of a valid github owner/name) inside the json body.
 * @returns metrics of all snapshots of a project
 * @throws HTTPError
 */
export async function POST({ request }) {
    const { term } = await request.json();
    if (!term.match(repoRegex)) {
        error(422, { message: "Only alphanumeric characters and -_./ allowed" });
    }
    try {
        /**
         * 1. Get all scan ids of a project
         * 2. Get metric document for each scan id
         * 3. Get bak_metrics document for each scan id
         */
        const res = await db.query(aql`
        FOR doc IN ${projectsColl}
        FILTER doc.identifier == ${term}
        LET scans = (
            FOR elem IN doc.scans
            LET metric = (
                FOR metric IN metrics
                FILTER elem == metric.scan_id && metric.identity.name_with_owner == doc.identifier
                LIMIT 1
                RETURN UNSET(metric, "_key", "_id", "_rev")
            )
            LET bak = (
                FOR bak IN bak_metrics
                FILTER elem == bak.scan_id && bak.identity.name_with_owner == doc.identifier
                LIMIT 1
                RETURN UNSET(bak, "_key", "_id", "_rev")
            )
            FOR scan IN ${scansColl}
            FILTER elem == scan._id
            RETURN MERGE(UNSET(scan, "_key", "_id", "_rev"),{metric: metric,bak: bak})
        )
        RETURN MERGE(UNSET(doc, "_key", "_id", "_rev"), {scans: scans})
    `);
        let all = await res.all();
        return json(all);
    } catch (err: any) {
        console.error(err.message);
    }
}

