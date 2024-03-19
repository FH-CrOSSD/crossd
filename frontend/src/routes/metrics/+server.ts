import { Database, aql } from "arangojs";
import { json } from '@sveltejs/kit';
import { error } from '@sveltejs/kit';
import { db } from "$hook.server";
import { repoRegex } from "$lib/util";

const projectsColl = db.collection("projects");
const scansColl = db.collection("scans");

/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
    const { term } = await request.json();
    if (!term.match(repoRegex)) {
        error(422, { message: "Only alphanumeric characters and -_./ allowed" });
    }
    // const sterm = '%' + term + '%';
    try {
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
        // FILTER metric.task_id == "9b607b21-18eb-4ee0-a8e7-1a93afbf1105"
        // console.log(await res.all());
        let all = await res.all();
        // for await (const metric of all) {
        //     console.log(metric.task_id);
        // }
        return json(all);
    } catch (err: any) {
        console.error(err.message);
    }
}

