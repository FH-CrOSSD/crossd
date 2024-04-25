import { Database, aql } from "arangojs";
import { json } from '@sveltejs/kit';
import { error } from '@sveltejs/kit';
import { db } from "$hook.server";
import { PER_PAGE,repoRegex } from '$lib/util';

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
    let { page } = body;
    if (!term.match(repoRegex)) {
        error(422, { message: "Only alphanumeric characters and -_./ allowed" });
    }
    const sterm = '%' + term + '%';

    // null, undefined, 0 result in page = 1
    page = Number(page);
    if (!page || page < 1) {
        page = 1;
    }

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
            LIMIT ${(page - 1) * PER_PAGE}, ${PER_PAGE}
            RETURN {"name":doc.identifier,"timestamp":timestamp[0],"repository":info[0]}
        `);

        let all = await res.all();
        return json(all);
    } catch (err: any) {
        console.error(err.message);
    }
}