const users = require('@arangodb/users');
const DB_NAME = "crossd";
try {
    db._createDatabase(DB_NAME);
    if (process.env.FRONTEND_USER && process.env.FRONTEND_PASSWORD) {
        users.save(process.env.FRONTEND_USER, process.env.FRONTEND_PASSWORD);
        users.grantDatabase(process.env.FRONTEND_USER, DB_NAME, 'ro');
    }
    if (process.env.WORKER_USER && process.env.WORKER_PASSWORD) {
        users.save(process.env.WORKER_USER, process.env.WORKER_PASSWORD);
        users.grantDatabase(process.env.WORKER_USER, DB_NAME, 'rw');

    }
} catch (ArangoError) { };
try {
    db._useDatabase(DB_NAME);
    db._createDocumentCollection("task_results");
    db._createDocumentCollection("projects");
    db._createDocumentCollection("scans");
    db._createDocumentCollection("bak_metrics");
    db._createDocumentCollection("bak_repos");
    db._createDocumentCollection("metrics");
    db._createDocumentCollection("repositories");
}
catch (ArangoError) { };