import { aql } from "arangojs";
import { json } from '@sveltejs/kit';
import { error } from '@sveltejs/kit';
import { db } from "$hook.server";
import { repoRegex } from "$lib/util.js";

const collection = db.collection("projects");
/** @type {import('./$types').RequestHandler} */
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
    const sterm = '%' + term + '%';

    try {
        const res = await db.query(aql`
        FOR doc IN ${collection}
        FILTER LOWER(doc.identifier) LIKE LOWER(${sterm})
        LET timestamp = (
            FOR scan IN scans 
            FILTER scan._id == LAST(doc.scans)
            LIMIT 1
            RETURN scan.issuedAt
        )
        LET info = 
        (FOR repo IN repositories
            FILTER LAST(doc.scans) == repo.scan_id
            RETURN {"nameWithOwner":repo.repository.nameWithOwner,"description":repo.repository.description, "readmes":repo.repository.readmes}
        )
            SORT doc.identifier
            COLLECT WITH COUNT INTO len
            RETURN {length: len}
        `);

        let all = await res.all();
        return json(all[0]);
    } catch (err: any) {
        console.error(err.message);
    }
}
