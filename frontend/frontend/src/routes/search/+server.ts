import { Database, aql } from "arangojs";
import { json } from '@sveltejs/kit';
import { error } from '@sveltejs/kit';
// import { db } from '../../hook.server.ts';
import { db } from "$hook.server";

const collection = db.collection("repositories");
const inputRegex = /^[a-zA-Z0-9-_./]+$/;
/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
    const { term } = await request.json();
    if (!term.match(inputRegex)) {
        error(422, { message: "Only alphanumeric characters and -_./ allowed" });
    }
    const sterm = '%' + term + '%';
    try {
        const res = await db.query(aql`
        FOR doc IN ${collection}
        FILTER LOWER(doc.repository.nameWithOwner) LIKE LOWER(${sterm})
        SORT doc.timestamp DESC
        COLLECT name = doc.repository.nameWithOwner INTO group
        LET new = FIRST(group)
        RETURN {"name":name,"timestamp":new.doc.timestamp,"task_id":new.doc.task_id, "repository":{"nameWithOwner":new.doc.repository.nameWithOwner,"description":new.doc.repository.description, "readmes":new.doc.repository.readmes}}
    `);

        //   FOR metric IN ${ metrics }
        //   FILTER LOWER(metric.repository.nameWithOwner) LIKE LOWER(${ sterm })
        //   RETURN metric
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