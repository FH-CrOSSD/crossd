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
                SORT m.timestamp DESC
                LET ts = m.timestamp*1000
                FILTER m.${parameter} != null
                COLLECT month = DATE_MONTH(ts)<10 ? CONCAT_SEPARATOR("/", DATE_YEAR(ts), CONCAT(0, DATE_MONTH(ts))) : CONCAT_SEPARATOR("/", DATE_YEAR(ts), DATE_MONTH(ts)) into clustered = {scan_id:m.scan_id,identity:m.identity,timestamp:m.timestamp}
                RETURN {"month": month, "objects": clustered}
            )
            LET aggr2 = (
                FOR item IN aggr
                LET tmp = (
                    FOR obj IN item.objects
                    COLLECT name = obj.identity.name_with_owner INTO elems = obj //otherwise each object is {obj: {scan_id: ..., ...}}
                    RETURN {"name": name, "projects": elems}
                )
                RETURN {"month": item.month, "month_project": tmp}
            )
            
            FOR month IN aggr2
            LET res = (
                LET metrics_month = (
                    FOR proj IN month.month_project
                        LET finished = (
                            FOR s IN proj.projects
                            FOR m IN metrics
                            FILTER m.scan_id == s.scan_id
                            LIMIT 1
                            RETURN m
                        )
                    RETURN finished[0]
                )
                FOR m IN metrics_month
                COLLECT AGGREGATE avg_ = AVG(m.${parameter}), min_ = MIN(m.${parameter}), max_ = MAX(m.${parameter}), agg_ = SUM(m.${parameter}), stddev_ = STDDEV(m.${parameter})
                RETURN {"avg": ROUND(avg_*100)/100, "min": ROUND(min_*100)/100, "max": ROUND(max_*100)/100, "agg": ROUND(agg_*100)/100, "stddev": ROUND(stddev_*100)/100}
            )
            RETURN MERGE({month: month.month}, res[0])
        `);
        let all = (await res.all());
        // console.log(all);
        return json(all);
    } catch (err: any) {
        console.error(err.message);
    }
}

