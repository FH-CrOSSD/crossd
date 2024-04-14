import { aql } from "arangojs";
import { json } from '@sveltejs/kit';
import { error } from '@sveltejs/kit';
import { db } from "$hook.server";

const metricsColl = db.collection("metrics");
const bakColl = db.collection("bak_metrics");
const scansColl = db.collection("scans");

/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
    const { timestamp } = await request.json();
    if (!Number.isFinite(timestamp)) {
        error(422, { message: "Only numerical timestamp is allowed" });
    }
    try {
        const res = await db.query(aql`
        FOR doc IN ${scansColl}
        FILTER doc.issuedAt == ${timestamp}
        LET data = (
            FOR repo IN ${metricsColl}
            FILTER repo.scan_id == doc._id
            RETURN UNSET(repo, "_key", "_id", "_rev")
        )
        LET bak = (
            FOR repo IN ${bakColl}
            FILTER repo.scan_id == doc._id
            RETURN UNSET(repo, "_key", "_id", "_rev")
        )
        RETURN {"metrics":data, "bak":bak}
    `);
        let all = await res.all();
        return json(all[0]);
    } catch (err: any) {
        console.error(err.message);
    }
}

