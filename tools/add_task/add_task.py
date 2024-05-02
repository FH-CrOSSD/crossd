#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import argparse
import os
import time

import pyArango.connection
from celery import Celery

app = Celery(
    "collect",
    broker="redis://:{}@redis-service:6379/0?ssl_cert_reqs=required".format(
        os.environ.get("RAUTH", "")
    ),
    broker_connection_retry_on_startup=True,
)

app.conf.task_routes = {
    "retrieve_github": {"queue": "collect", "routing_key": "collect"},
    "retrieve_github_url": {"queue": "collect", "routing_key": "collect"},
    "do_metrics": {"queue": "metric", "routing_key": "metric"},
    "bak_tasks": {"queue": "bak", "routing_key": "bak"},
}


def main(args):
    conn = pyArango.connection.Connection(
        arangoURL="https://arangodb-cluster-internal:8529",
        username=args.user,
        password=args.password,
        verify=True,
    )

    # create collections if not exist
    if not conn["crossd"].hasCollection("scans"):
        conn["crossd"].createCollection(name="scans")

    if not conn["crossd"].hasCollection("projects"):
        conn["crossd"].createCollection(name="projects")
        conn["crossd"]["projects"].ensurePersistentIndex(["identifier"], unique=True)

    coll = conn["crossd"]["scans"]

    for entry in args.owner_with_name:
        try:
            owner, name = entry.strip().split("/")
        except ValueError:
            print("invalid repository identifier {}".format(entry))
            continue
        # create scan document for each owner/name
        doc = coll.createDocument(
            {
                "issuedAt": time.time(),
                "tasks": {
                    "bak_tasks": (owner, name),
                    "retrieve_github": (owner, name),
                },
                "tags": args.tag,
            }
        )
        doc.save()
        print(doc._id)

        # add scan id to entry in projects collection
        aql = """UPSERT { identifier: @identifier }
                    INSERT { identifier: @identifier, scans: [@scanid] }
                    UPDATE { scans: APPEND(OLD.scans, @scanid) }
                    IN projects
            """
        queryResult = conn["crossd"].AQLQuery(
            aql,
            bindVars={"identifier": owner + "/" + name, "scanid": doc._id},
        )

        # issue worker tasks
        if not args.only:
            app.send_task("bak_tasks", (owner, name, doc._id))
            app.send_task("retrieve_github", (owner, name, doc._id))
        else:
            if args.only == "bak":
                app.send_task("bak_tasks", (owner, name, doc._id))
            elif args.only == "metric":
                app.send_task("retrieve_github", (owner, name, doc._id))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a repository to the queue")
    parser.add_argument(
        metavar="owner/name",
        help="owner of the repository",
        dest="owner_with_name",
        nargs="+",
    )
    parser.add_argument(
        "--only", choices=["bak", "metric"], help="limit execution to a single task"
    )
    parser.add_argument("--user", help="arangodb username", default="worker")
    parser.add_argument("--password", help="arangodb password", default="worker")
    parser.add_argument(
        "-t", "--tag", action="append", help="Set a tag for the scan", default=[]
    )
    args = parser.parse_args()
    main(args)
