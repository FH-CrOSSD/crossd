import { Database, aql } from "arangojs";

export const db = new Database({
    url: "https://172.23.101.111:30529",
    databaseName: "crossd",
    auth: { username: "root", password: "" },
    agentOptions: {
        rejectUnauthorized: false
    },
});