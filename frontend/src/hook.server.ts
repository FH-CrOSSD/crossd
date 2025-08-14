import { dev } from '$app/environment';
import { env } from '$env/dynamic/private';
if(dev){
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";}
import { Database, aql } from "arangojs";

export const db = new Database({
    url: env.ARANGO_URL,
    databaseName: "crossd",
    auth: { username: env.FRONTEND_USER ?? "", password: env.FRONTEND_PASSWORD },
    agentOptions: {
        // disable https hostname verification in development environment
        rejectUnauthorized: dev ? false : true
    },
    rejectUnauthorized: dev ? false : true
});