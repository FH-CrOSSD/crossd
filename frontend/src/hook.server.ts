import { Database, aql } from "arangojs";
import { env } from '$env/dynamic/private';
import { dev } from '$app/environment';

export const db = new Database({
    url: env.ARANGO_URL,
    databaseName: "crossd",
    auth: { username: env.FRONTEND_USER ?? "", password: env.FRONTEND_PASSWORD },
    agentOptions: {
        // disable https hostname verification in development environment
        rejectUnauthorized: dev ? false : true
    },
});