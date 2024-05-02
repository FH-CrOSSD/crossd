import { db } from "$hook.server";
import { json } from '@sveltejs/kit';
import { aql } from "arangojs";

const projectsColl = db.collection("projects");

/** @type {import('./$types').RequestHandler} */
/**
 * Handles POST requests to /api/projects and returns a list of all projects stored in the ArangoDB database.
 * 
 * @returns list of all projects
 * @throws HTTPError
 */
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

