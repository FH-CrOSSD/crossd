import { aql } from "arangojs";
import { json } from '@sveltejs/kit';
import { error } from '@sveltejs/kit';
import { db } from "$hook.server";
import { repoRegex } from "$lib/util";

const projectsColl = db.collection("projects");
const scansColl = db.collection("scans");

/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
    let term;
    try {
        term = (await request.json()).term;
    } catch (err: any) {
        console.log(err);
        if (err instanceof SyntaxError) {
            error(400, { message: "Body could not be parsed as json" });
        }
    }

    if (!term || !term.match(repoRegex)) {
        error(422, { message: "Body needs to contain term of alphanumeric characters and -_./" });
    }

    try {
        const res = await db.query(aql`
        FOR doc IN ${projectsColl}
        FILTER doc.identifier == ${term}
        LET ts = (
            FOR scan IN doc.scans
            FOR entry IN ${scansColl}
            FILTER scan == entry._id
            SORT entry.issuedAt
            RETURN entry.issuedAt
        )
        RETURN ts
    `);
        let all = await res.all();
        return json(all?.[0] ?? []);
    } catch (err: any) {
        console.error(err.message);
    }
}

