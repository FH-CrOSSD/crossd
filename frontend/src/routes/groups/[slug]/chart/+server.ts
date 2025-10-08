import { db } from "$hook.server";
import { repoRegex } from "$lib/util";
import { error, json } from '@sveltejs/kit';
import { aql } from "arangojs";
import { literal } from "arangojs/aql";

// const metricsColl = db.collection("metrics");
// const bakColl = db.collection("bak_metrics");
const scansColl = db.collection("scans");
const groupsColl = db.collection("groups");
const projectsColl = db.collection("projects");
const choices = new Set(["elephant_factor", "maturity_level", "criticality_score", "support_rate", "github_community_health_percentage.custom_health_score"]);

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
    let { parameter, name } = resp;

    if (!parameter || !(choices.has(parameter))) {
        error(422, { message: "Body needs to contain valid parameter" });
    }
    if (!name || !name.match(repoRegex)) {
        error(422, { message: "Body needs to contain group name of alphanumeric characters and -_./" });
    }
    if (choices.has(parameter) && parameter.includes(".")) {
        parameter = literal(parameter);
    }

    try {
        const res = await db.query(aql`
        LET targetGroup = FIRST(
            FOR g IN groups
                FILTER g.name == ${name}
                LIMIT 1
                RETURN g
        )

        LET relevantTags = targetGroup.tags

        LET scanIds = (
            FOR scan IN scans
            FILTER scan.tags != null
                FILTER LENGTH(INTERSECTION(scan.tags, relevantTags)) > 0
                RETURN DISTINCT scan._id
        )

        FOR m IN metrics
            FILTER m.scan_id IN scanIds
            FILTER m.${parameter} != null

            LET month_ = DATE_MONTH(m.timestamp * 1000) < 10
                ? CONCAT(DATE_YEAR(m.timestamp * 1000), "/0", DATE_MONTH(m.timestamp * 1000))
                : CONCAT(DATE_YEAR(m.timestamp * 1000), "/", DATE_MONTH(m.timestamp * 1000))

            COLLECT month__ = month_, project = m.identity.name_with_owner
                INTO grouped = {scan_id: m.scan_id, timestamp: m.timestamp, value: m.${parameter}, identity: m.identity}

            // Pick the newest scan for this project in the month
            LET newestScan = FIRST(
                FOR g IN grouped
                SORT g.timestamp DESC
                LIMIT 1
                RETURN g
            )

            COLLECT month = month__ INTO monthGroup = newestScan

            // Aggregate across newest scans of all projects in the month
            LET agg = {
                avg: ROUND(AVG(monthGroup[*].value) * 100) / 100,
                min: ROUND(MIN(monthGroup[*].value) * 100) / 100,
                max: ROUND(MAX(monthGroup[*].value) * 100) / 100,
                agg: ROUND(SUM(monthGroup[*].value) * 100) / 100,
                stddev: ROUND(STDDEV(monthGroup[*].value) * 100) / 100
            }

            RETURN MERGE({month}, agg)
        `);
        let all = (await res.all());
        return json(all);
    } catch (err: any) {
        console.error(err.message);
    }
}

