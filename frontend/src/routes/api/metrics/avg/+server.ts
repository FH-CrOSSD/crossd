import { db } from "$hook.server";
import { repoRegex } from "$lib/util";
import { error, json } from '@sveltejs/kit';
import { aql } from "arangojs";

const metricsColl = db.collection("metrics");

/** @type {import('./$types').RequestHandler} */
/**
 * Handles POST requests to /metrics and returns metrics for a project.
 * 
 * @param request - contains term (part of a valid github owner/name) inside the json body.
 * @returns metrics of all snapshots of a project
 * @throws HTTPError
 */
export async function POST({ request }) {
    try {
        /**
         * 1. Get all scan ids of a project
         * 2. Get metric document for each scan id
         * 3. Get bak_metrics document for each scan id
         */
        const res = await db.query(aql`
            FOR m IN ${metricsColl}
            COLLECT aggregate elephant_avg=AVERAGE(m.elephant_factor), maturity_avg=AVERAGE(m.maturity_level), criticality_avg=AVERAGE(m.criticality_score), 
                github_score_avg=AVERAGE(m.github_community_health_percentage.custom_health_score), support_avg=AVERAGE(m.support_rate)
            
            RETURN {
                "avg":{"elephant_factor":ROUND(elephant_avg*100)/100,"maturity_level":ROUND(maturity_avg*100)/100, "criticality_score":ROUND(criticality_avg*100)/100,"support_rate":ROUND(support_avg*100)/100, "github_community_health_percentage":ROUND(github_score_avg*100)/100},
            }
    `);
        let all = await res.all();
        console.log(all[0]);
        return json(all[0]);
    } catch (err: any) {
        console.error(err.message);
    }
}
