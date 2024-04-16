import { aql } from "arangojs";
import { json } from '@sveltejs/kit';
import { error } from '@sveltejs/kit';
import { db } from "$hook.server";
import { repoRegex } from "$lib/util";

const metricsColl = db.collection("metrics");
const bakColl = db.collection("bak_metrics");
const scansColl = db.collection("scans");
const projectsColl = db.collection("projects");

/** @type {import('./$types').RequestHandler} */
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
    const { term, timestamp } = resp;

    if (!term || !term.match(repoRegex)) {
        error(422, { message: "Body needs to contain term of alphanumeric characters and -_./" });
    }

    if (!timestamp || !Number.isFinite(timestamp)) {
        error(422, { message: "Body needs to contain timestamp with numerical value" });
    }

    try {
        const res = await db.query(aql`
        FOR project in ${projectsColl}
        FILTER project.identifier == ${term}
        FOR doc IN ${scansColl}
        FILTER doc._id in project.scans
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
        RETURN {"metrics":data[0], "bak":bak[0]}
    `);
        let all = await res.all();
        return json(all[0]);
    } catch (err: any) {
        console.error(err.message);
    }
}

