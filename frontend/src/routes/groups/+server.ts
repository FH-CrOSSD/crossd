import { db } from "$hook.server";
import { repoRegex } from "$lib/util";
import { error, json } from '@sveltejs/kit';
import { aql } from "arangojs";

// const metricsColl = db.collection("metrics");
// const bakColl = db.collection("bak_metrics");
const scansColl = db.collection("scans");
const groupsColl = db.collection("groups");
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
    // let resp;

    // try {
    //     resp = await request.json();
    // } catch (err: any) {
    //     console.log(err);
    //     if (err instanceof SyntaxError) {
    //         error(400, { message: "Body could not be parsed as json" });
    //     }
    // }
    // const { term, timestamp } = resp;

    // if (!term || !term.match(repoRegex)) {
    //     error(422, { message: "Body needs to contain term of alphanumeric characters and -_./" });
    // }

    // if (!timestamp || !Number.isFinite(timestamp)) {
    //     error(422, { message: "Body needs to contain timestamp with numerical value" });
    // }

    try {
        /**
         * 1. Get scans for the project
         * 2. Get the scan with the requested timestamp
         * 3. Get the metric and bak metrics for this snapshot
         */
        const res = await db.query(aql`
        FOR group IN ${groupsColl}
        FOR tag IN group.tags

        LET scanIds = (
            FOR scan IN ${scansColl}
            FILTER tag IN scan.tags
            RETURN DISTINCT scan._id
        )

        LET projects_ = (
            FOR project IN ${projectsColl}
            FOR scanid IN project.scans
            FILTER scanid IN scanIds
            SORT project.identifier
            RETURN distinct project.identifier
        ) 
        
        RETURN {"group": UNSET(group, "_key", "_id", "_rev"), "scanIds":scanIds, "projects": projects_}

    `);
        let all = await res.all();
        return json({ "data": all });
    } catch (err: any) {
        console.error(err.message);
    }
}

