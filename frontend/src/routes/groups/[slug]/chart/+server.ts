import { db } from "$hook.server";
import { repoRegex } from "$lib/util";
import { error, json } from '@sveltejs/kit';
import { aql } from "arangojs";

// const metricsColl = db.collection("metrics");
// const bakColl = db.collection("bak_metrics");
const scansColl = db.collection("scans");
const groupsColl = db.collection("groups");
const projectsColl = db.collection("projects");
const choices = new Set(["elephant_factor", "maturity_level", "criticality_score", "support_rate", "github_community_health_percentage"]);

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
    const { parameter, name } = resp;

    if (!parameter || !(choices.has(parameter))) {
        error(422, { message: "Body needs to contain valid parameter" });
    }
    if (!name || !name.match(repoRegex)) {
        error(422, { message: "Body needs to contain group name of alphanumeric characters and -_./" });
    }

    try {
        const res = await db.query(aql`
        FOR group IN groups
            FILTER group.name == ${name}
            FOR tag IN group.tags
                LET scanIds = (
                    FOR scan IN scans
                    FILTER tag IN scan.tags
                    RETURN DISTINCT scan._id
                )
                
                LET aggr = (
                    FOR m IN metrics
                    FILTER m.scan_id IN scanIds
                    LET ts = m.timestamp*1000
                    FILTER m.${parameter}
                    COLLECT month = DATE_MONTH(ts)<10 ? CONCAT_SEPARATOR("/", DATE_YEAR(ts), CONCAT(0, DATE_MONTH(ts))) : CONCAT_SEPARATOR("/", DATE_YEAR(ts), DATE_MONTH(ts))
                    AGGREGATE avg_ = AVG(m.${parameter}), min_ = MIN(m.${parameter}), max_ = MAX(m.${parameter}), agg_ = SUM(m.${parameter}), stddev_ = STDDEV(m.${parameter})
                    RETURN {"month": month, "avg": ROUND(avg_*100)/100, "min": ROUND(min_*100)/100, "max": ROUND(max_*100)/100, "agg": ROUND(agg_*100)/100, "stddev": ROUND(stddev_*100)/100}
                )
                FOR month IN aggr
                    FILTER month.avg != null
                    RETURN month
        `);
        let all = (await res.all());
        // console.log(all);
        return json(all);
    } catch (err: any) {
        console.error(err.message);
    }
}

