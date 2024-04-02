import { Database, aql } from "arangojs";
import { env } from '$env/dynamic/private';
import { dev } from '$app/environment';
console.log("development: "+ dev);

export const db = new Database({
    url: env.ARANGO_URL,
    databaseName: "crossd",
    auth: { username: env.FRONTEND_USER ?? "", password: env.FRONTEND_PASSWORD },
    agentOptions: {
        rejectUnauthorized: dev ? false : true
    },
});