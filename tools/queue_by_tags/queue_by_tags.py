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
    "do_metrics": {"queue": "metric", "routing_key": "metric"},
}

DEFAULT_TASK = "retrieve_github"


def parse_queue_mapping(value):
    parts = value.split("=", 1)
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(
            "queue mapping must be in the form tag=queue_name"
        )
    return parts[0], parts[1]


def main(args):
    queue_map = {tag: queue for tag, queue in (args.queue or [])}

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

    if not conn["crossd"].hasCollection("scans"):
        conn["crossd"].createCollection(name="scans")
    if not conn["crossd"].hasCollection("projects"):
        conn["crossd"].createCollection(name="projects")

    conn["crossd"]["projects"].ensurePersistentIndex(["identifier"], unique=True)
    scans_coll = conn["crossd"]["scans"]

    # retrieve unique projects that have at least one of the specified tags
    aql = """
        LET matched_ids = (
            FOR doc IN tags
                FILTER doc.tag IN @tags
                RETURN DISTINCT doc.identifier
        )

        FOR doc IN tags
            FILTER doc.identifier IN matched_ids
            COLLECT identifier = doc.identifier INTO groups
            RETURN {
                identifier,
                all_tags: groups[*].doc.tag
            }
    """
    results = conn["crossd"].AQLQuery(aql, bindVars={"tags": args.tags}, rawResults=True)

    for entry in results:
        identifier = entry["identifier"]
        all_tags = entry["all_tags"]
        owner, name = identifier.split("/", 1)

        # use queue of first matched tag that has a mapping, otherwise let routing handle it
        queue = next((queue_map[t] for t in all_tags if t in queue_map), None)

        # create scan document
        doc = scans_coll.createDocument(
            {
                "issuedAt": time.time(),
                "tasks": {
                    DEFAULT_TASK: [owner, name],
                },
                "tags": list(set(all_tags) | set(args.extra_tags)),
            }
        )
        doc.save()
        print(doc._id)

        # add scan id to projects collection
        upsert_aql = """UPSERT { identifier: @identifier }
                    INSERT { identifier: @identifier, scans: [@scanid] }
                    UPDATE { scans: APPEND(OLD.scans, @scanid) }
                    IN projects
        """
        conn["crossd"].AQLQuery(
            upsert_aql,
            bindVars={"identifier": identifier, "scanid": doc._id},
        )

        # send celery task
        if queue:
            app.send_task(DEFAULT_TASK, (owner, name, doc._id), queue=queue, routing_key=queue)
        else:
            app.send_task(DEFAULT_TASK, (owner, name, doc._id))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Queue retrieve_github tasks for all projects matching specified tags"
    )
    parser.add_argument(
        "tags",
        metavar="tag",
        nargs="+",
        help="One or more tags to filter projects by",
    )
    parser.add_argument(
        "--queue",
        action="append",
        type=parse_queue_mapping,
        metavar="tag=queue_name",
        help="Map a tag to a specific queue (e.g. --queue mytag=collect). Can be specified multiple times.",
    )
    parser.add_argument(
        "-t", "--extra-tag",
        action="append",
        dest="extra_tags",
        default=[],
        metavar="tag",
        help="Additional tag added to the scan document only, not used for project filtering. Can be specified multiple times.",
    )
    parser.add_argument("--user", help="arangodb username", default="worker")
    parser.add_argument("--password", help="arangodb password", default="worker")
    args = parser.parse_args()
    main(args)
