import { db } from "$hook.server";
import { repoRegex } from "$lib/util.js";
import { error, json } from '@sveltejs/kit';
import { aql } from "arangojs";

const collection = db.collection("projects");

/** @type {import('./$types').RequestHandler} */
/**
 * Handles POST requests to /search/count and returns the number of search results.
 * 
 * @param request - contains term (part of a valid github owner/name) inside the json body.
 * @returns count of search results
 * @throws HTTPError
 */
export async function POST({ request }) {
    let body;
    try {
        body = (await request.json());
    } catch (err: any) {
        console.log(err);
        if (err instanceof SyntaxError) {
            error(400, { message: "Body could not be parsed as json" });
        }
    }
    const { term } = body;
    if (!term.match(repoRegex)) {
        error(422, { message: "Only alphanumeric characters and -_./ allowed" });
    }

    // add % for wildcard
    const sterm = '%' + term + '%';

    try {
        // Go through projects and check if search term is contained in name and return count
        const res = await db.query(aql`
        FOR doc IN ${collection}
        FILTER LOWER(doc.identifier) LIKE LOWER(${sterm})
        LET result_available  = (
            FOR metric IN metrics
            FILTER LOWER(doc.identifier) LIKE LOWER(metric.identity.name_with_owner)
            LIMIT 1
            RETURN metric
        )
        FILTER LENGTH(result_available)>0
        COLLECT WITH COUNT INTO len
        RETURN {length: len}
        `);

        let all = await res.all();
        return json(all[0]);
    } catch (err: any) {
        console.error(err.message);
    }
}
