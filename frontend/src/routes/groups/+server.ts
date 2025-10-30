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
    try {
        const res = await db.query(aql`
        FOR group IN ${groupsColl}

        // Get all scans that match any of the group's tags
        LET scanIds = (
            FOR scan IN ${scansColl}
            FILTER scan.tags != null
            FILTER LENGTH(INTERSECTION(scan.tags, group.tags)) > 0
            RETURN scan._id
        )

        // Get all projects referencing those scans
        LET projects_ = (
            FOR project IN ${projectsColl}
            FILTER LENGTH(INTERSECTION(project.scans, scanIds)) > 0
            SORT project.identifier
            RETURN project.identifier
        )

        RETURN {
            group: UNSET(group, "_key", "_id", "_rev"),
            //scanIds: scanIds,
            //projects: projects_
            projects: LENGTH(projects_)
        }
    `);
        let all = await res.all();
        return json({ "data": all });
    } catch (err: any) {
        console.error(err.message);
    }
}

