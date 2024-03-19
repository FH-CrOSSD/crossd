import { Database, aql } from "arangojs";
import { json } from '@sveltejs/kit';
import { error } from '@sveltejs/kit';
import { db } from "$hook.server";
import { repoRegex } from "$lib/util";

const metrics = db.collection("bak_metrics");
/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
    const { term } = await request.json();
    if (!term.match(repoRegex)) {
        error(422, { message: "Only alphanumeric characters and -_./ allowed" });
    }
    // const sterm = '%' + term + '%';
    try {
        const res = await db.query(aql`
      FOR metric IN ${metrics}
      FILTER metric.identity.name_with_owner == ${term}
      RETURN UNSET(metric, "_key","_id","_rev")
    `);
        // FILTER metric.task_id == "9b607b21-18eb-4ee0-a8e7-1a93afbf1105"
        // console.log(await res.all());
        let all = await res.all();
        for await (const metric of all) {
            console.log(metric.task_id);
        }
        return json(all);
    } catch (err: any) {
        console.error(err.message);
    }
}

