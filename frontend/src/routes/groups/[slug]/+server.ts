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
    let resp;

    try {
        resp = await request.json();
    } catch (err: any) {
        console.log(err);
        if (err instanceof SyntaxError) {
            error(400, { message: "Body could not be parsed as json" });
        }
    }
    const { name } = resp;

    if (!name || !name.match(repoRegex)) {
        error(422, { message: "Body needs to contain group name of alphanumeric characters and -_./" });
    }

    try {
        /**
         * 1. Get scans for the project
         * 2. Get the scan with the requested timestamp
         * 3. Get the metric and bak metrics for this snapshot
         */
        const res = await db.query(aql`
        FOR group IN ${groupsColl}
        FILTER group.name == ${name}
        FOR tag IN group.tags

        LET scanIds = (
            FOR scan IN ${scansColl}
            FILTER tag IN scan.tags
            RETURN DISTINCT scan._id
        )
        
        LET projects_ = (
            FOR scanid IN scanIds
            FOR m IN metrics
            FILTER m.scan_id==scanid
            RETURN DISTINCT m.identity.name_with_owner
        )
        LET data=(
            FOR s IN scanIds
            FOR m IN metrics
            FILTER m.scan_id == s
            FILTER m.version > "2"
            COLLECT aggregate elephant_avg=AVERAGE(m.elephant_factor), maturity_avg=AVERAGE(m.maturity_level), criticality_avg=AVERAGE(m.criticality_score), 
                github_score_avg=AVERAGE(m.github_community_health_percentage.custom_health_score), support_avg=AVERAGE(m.support_rate),
                elephant_min=MIN(m.elephant_factor), maturity_min=MIN(m.maturity_level), criticality_min=MIN(m.criticality_score), 
                github_score_min=MIN(m.github_community_health_percentage.custom_health_score), support_min=MIN(m.support_rate),
                elephant_max=MAX(m.elephant_factor), maturity_max=MAX(m.maturity_level),criticality_max=MAX(m.criticality_score), 
                github_score_max=MAX(m.github_community_health_percentage.custom_health_score), support_max=MAX(m.support_rate),
                elephant_sum=SUM(m.elephant_factor), maturity_sum=SUM(m.maturity_level),criticality_sum=SUM(m.criticality_score), 
                github_score_sum=SUM(m.github_community_health_percentage.custom_health_score), support_sum=SUM(m.support_rate),
                elephant_stddev=STDDEV(m.elephant_factor), maturity_stddev=STDDEV(m.maturity_level),criticality_stddev=STDDEV(m.criticality_score), 
                github_score_stddev=STDDEV(m.github_community_health_percentage.custom_health_score), support_stddev=STDDEV(m.support_rate)
            RETURN {
                "avg":{"elephant_factor":ROUND(elephant_avg*100)/100,"maturity_level":ROUND(maturity_avg*100)/100, "criticality_score":ROUND(criticality_avg*100)/100,"support_rate":ROUND(support_avg*100)/100, "github_community_health_percentage":ROUND(github_score_avg*100)/100},
                "min":{"elephant_factor":ROUND(elephant_min*100)/100,"maturity_level":ROUND(maturity_min*100)/100, "criticality_score":ROUND(criticality_min*100)/100,"support_rate":ROUND(support_min*100)/100, "github_community_health_percentage":ROUND(github_score_min*100)/100},
                "max":{"elephant_factor":ROUND(elephant_max*100)/100,"maturity_level":ROUND(maturity_max*100)/100, "criticality_score":ROUND(criticality_max*100)/100,"support_rate":ROUND(support_max*100)/100, "github_community_health_percentage":ROUND(github_score_max*100)/100},
                "sum":{"elephant_factor":ROUND(elephant_sum*100)/100,"maturity_level":ROUND(maturity_sum*100)/100, "criticality_score":ROUND(criticality_sum*100)/100,"support_rate":ROUND(support_sum*100)/100, "github_community_health_percentage":ROUND(github_score_sum*100)/100},
                "stddev":{"elephant_factor":ROUND(elephant_stddev*100)/100,"maturity_level":ROUND(maturity_stddev*100)/100, "criticality_score":ROUND(criticality_stddev*100)/100,"support_rate":ROUND(support_stddev*100)/100, "github_community_health_percentage":ROUND(github_score_stddev*100)/100}
        }
        )
        RETURN {"group": UNSET(group, "_key", "_id", "_rev"), "scanIds":scanIds, "projects": projects_, data:data[0]}
        `);
        let all = (await res.all())[0];
        console.log(all);
        return json(all);
    } catch (err: any) {
        console.error(err.message);
    }
}

