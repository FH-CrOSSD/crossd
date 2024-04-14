import { aql } from "arangojs";
import { json } from '@sveltejs/kit';
import { db } from "$hook.server";

const projectsColl = db.collection("projects");

/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
    try {
        const res = await db.query(aql`
        FOR doc IN ${projectsColl}
        RETURN doc.identifier
    `);
        let all = await res.all();
        return json(all);
        // returns error if nothing is returned
    } catch (err: any) {
        console.error(err.message);
    }
}

