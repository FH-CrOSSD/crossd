#!/usr/bin/env python3
# -*- coding=utf-8 -*-
from celery import Celery
import pyArango.connection
import time
import argparse

app = Celery(
    "collect",
    broker="redis://redis-service:6379/0",
    # backend="arangodb://root:@arangodb-cluster-internal:8529/crossd/task-results",
    broker_connection_retry_on_startup=True,
)

app.conf.task_routes = {
    "retrieve_github": {"queue": "collect", "routing_key": "collect"},
    "retrieve_github_url": {"queue": "collect", "routing_key": "collect"},
    "do_metrics": {"queue": "metric", "routing_key": "metric"},
    "bak_tasks": {"queue": "bak", "routing_key": "bak"},
}

# app.send_task(
#    "retrieve_github",
#    #("laurent22", "joplin")
#    ("FH-CrOSSD", "crossd.tech")
#    # , queue="collect", routing_key="collect"
# )

# tasks = [("sveltejs", "kit")]

# for task in tasks:
#    app.send_task("bak_tasks", task)
#    app.send_task("retrieve_github", task)
# app.send_task(
#    "bak_tasks",
# ("laurent22", "joplin")
# ("keeweb", "keeweb")
#    ("sveltejs", "kit")
# ("FH-CrOSSD", "crossd.tech")
# , queue="collect", routing_key="collect"
# )


def main(args):
    conn = pyArango.connection.Connection(
        arangoURL="https://arangodb-cluster-internal:8529",
        username=args.user,
        password=args.password,
        verify=False,
    )
    if not conn["crossd"].hasCollection("scans"):
        conn["crossd"].createCollection(name="scans")
    coll = conn["crossd"]["scans"]
    # coll = db.createCollection(name="scans")
    doc = coll.createDocument(
        {
            "issuedAt": time.time(),
            "tasks": {
                "bak_tasks": (args.owner, args.name),
                "retrieve_github": (args.owner, args.name),
            },
        }
    )
    doc.save()
    print(doc._id)
    if not conn["crossd"].hasCollection("projects"):
        conn["crossd"].createCollection(name="projects")
        conn["crossd"]["projects"].ensurePersistentIndex(["identifier"], unique=True)
    aql = """UPSERT { identifier: @identifier }
                INSERT { identifier: @identifier, scans: [@scanid] }
                UPDATE { scans: APPEND(OLD.scans, @scanid) }
                IN projects
        """
    queryResult = conn["crossd"].AQLQuery(
        aql,
        bindVars={"identifier": args.owner + "/" + args.name, "scanid": doc._id},
    )

    if not args.only:
        app.send_task("bak_tasks", (args.owner, args.name, doc._id))
        app.send_task("retrieve_github", (args.owner, args.name, doc._id))
    else:
        if args.only == "bak":
            app.send_task("bak_tasks", (args.owner, args.name, doc._id))
        elif args.only == "metric":
            app.send_task("retrieve_github", (args.owner, args.name, doc._id))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a repository to the queue")
    parser.add_argument("owner", help="owner of the repository")
    parser.add_argument("name", help="name of the repository")
    parser.add_argument(
        "--only", choices=["bak", "metric"], help="limit execution to a single task"
    )
    parser.add_argument(
        "--user", help="arangodb username", default="worker"
    )
    parser.add_argument(
        "--password", help="arangodb password", default="worker"
    )
    args = parser.parse_args()
    main(args)
