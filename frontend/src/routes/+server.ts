import { db } from "$hook.server";
import { json } from '@sveltejs/kit';
import { aql } from "arangojs";

const coll = db.collection("projects");
const collections = ["repositories", "metrics", "bak_metrics", "task_results", "scans", "projects", "bak_repos", "commits"];

/** @type {import('./$types').RequestHandler} */
/**
 * Handles POST requests to / and returns generic statistics about the db.
 * 
 * @returns db statistics
 * @throws HTTPError
 */
export async function POST() {
    let figures = { docsSize: 0, docsCount: 0 };
    try {
        const query = await db.query(aql`
        RETURN { "avg_scans_per_project": average(for elem in ${coll} return length(elem.scans)) }
       `);
        let all = (await query.all())[0];

        for (let i = 0; i < collections.length; i++) {
            // get stats for each collection and sum them up
            const tmp = await db.collection(collections[i]).figures();
            figures['docsSize'] += tmp['figures']['documentsSize'];
            figures['docsCount'] += tmp['count'];
            if (collections[i] === 'projects') {
                all['unique_projects'] = tmp['count'];
            }
        }
        let res = { stats: all, figures: figures };
        return json(res);
    } catch (err: any) {
        console.error(err.message);
    }
}
