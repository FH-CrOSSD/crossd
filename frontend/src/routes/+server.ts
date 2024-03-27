import { Database, aql } from "arangojs";
import { json } from '@sveltejs/kit';
import { error } from '@sveltejs/kit';
// import { db } from '../../hook.server.ts';
import { db } from "$hook.server";

const coll = db.collection("projects");
const collections = ["repositories", "metrics", "bak_metrics", "task_results", "scans", "projects", "bak_repos"];
/** @type {import('./$types').RequestHandler} */
export async function POST() {
    let figures = { docsSize: 0, docsCount: 0 };
    try {
        const query = await db.query(aql`
        RETURN { "avg_scans_per_project": average(for elem in ${ coll } return length(elem.scans)) }
       `);
        //     LET aggr = (FOR doc in ${ coll }
        //     COLLECT name = doc.repository.nameWithOwner WITH COUNT INTO length
        //     RETURN { "name": name, "length": length }
        //     )
        //   RETURN { "avg_scans_per_project": average(for elem in aggr return elem.length), "unique_projects": count(unique(for elem in aggr return elem.name)) }

        let all = (await query.all())[0];
        console.log(all);
        for (let i = 0; i < collections.length; i++) {
            const tmp = await db.collection(collections[i]).figures();
            figures['docsSize'] += tmp['figures']['documentsSize'];
            figures['docsCount'] += tmp['count'];
            if (collections[i]==='projects'){
                all['unique_projects']=tmp['count'];
            }
        }
        let res = { stats: all, figures: figures };
        return json(res);
    } catch (err: any) {
        console.error(err.message);
    }
}

// const metrics = db.collection("metrics");
// const inputRegex = /^[a-zA-Z0-9-_./]+$/;
// /** @type {import('./$types').RequestHandler} */
// export async function POST({ request }) {
//     const { term } = await request.json();
//     if (!term.match(inputRegex)) {
//         throw error(422, { message: "Only alphanumeric characters and -_./ allowed" })
//     }
//     const sterm = '%' + term + '%';
//     try {
//         const res = await db.query(aql`
//       FOR metric IN ${metrics}
//       FILTER metric.identity.name_with_owner LIKE ${sterm}
//       RETURN metric
//     `);
//         // FILTER metric.task_id == "9b607b21-18eb-4ee0-a8e7-1a93afbf1105"
//         // console.log(await res.all());
//         let all = await res.all();
//         for await (const metric of all) {
//             console.log(metric.task_id);
//         }
//         return json(all);
//     } catch (err: any) {
//         console.error(err.message);
//     }
// }