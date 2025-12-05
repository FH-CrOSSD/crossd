#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import argparse
import os
import time

import pyArango.connection
from celery import Celery


routes = {
        "retrieve_github": {"queue": "collect", "routing_key": "collect"},
        "retrieve_github_url": {"queue": "collect", "routing_key": "collect"},
        "do_metrics": {"queue": "metric", "routing_key": "metric"}
    }


def main(args):

    app = Celery(
    "collect",
    broker="rediss://:{}@redis-service:6379/0?ssl_cert_reqs=required".format(
        os.environ.get("RAUTH", "")
    ),
    broker_connection_retry_on_startup=True,
    )

    app.conf.task_routes = routes

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

        # issue worker tasks based on CLI options
        for task in args.task:
            if args.queue:
                app.send_task(task, (owner, name, doc._id), queue=args.queue, routing_key=args.queue)
            else:
                app.send_task(task, (owner, name, doc._id))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a repository to the queue")
    parser.add_argument(
        metavar="owner/name",
        help="owner of the repository",
        dest="owner_with_name",
        nargs="+",
    )
    parser.add_argument(
        "--task",
        action="append",
        choices=list(routes.keys()),
        default=["retrieve_github"],
        help="Specify which task(s) to run. Can be used multiple times. Defaults to retrieve_github.",
    )
    parser.add_argument(
        "--queue",
        help="Override the default queue for all tasks",
    )
    parser.add_argument("--user", help="arangodb username", default="worker")
    parser.add_argument("--password", help="arangodb password", default="worker")
    parser.add_argument(
        "-t", "--tag", action="append", help="Set a tag for the scan", default=[]
    )
    args = parser.parse_args()
    main(args)
