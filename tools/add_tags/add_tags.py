#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import argparse

import pyArango.connection
import pyArango.theExceptions


def main(args):

    conn = pyArango.connection.Connection(
        arangoURL=args.arango_url,
        username=args.user,
        password=args.password,
        verify=True,
    )

    if not conn["crossd"].hasCollection("projects"):
        conn["crossd"].createCollection(name="projects")

    conn["crossd"]["projects"].ensurePersistentIndex(["identifier"], unique=True)

    if not conn["crossd"].hasCollection("tags"):
        conn["crossd"].createCollection(name="tags")

    tags_coll = conn["crossd"]["tags"]
    tags_coll.ensurePersistentIndex(["identifier", "tag"], unique=True)
    tags_coll.ensurePersistentIndex(["identifier"], unique=False)
    tags_coll.ensurePersistentIndex(["tag"], unique=False)

    for entry in args.owner_with_name:
        try:
            owner, name = entry.strip().split("/")
        except ValueError:
            print("invalid repository identifier {}".format(entry))
            continue

        identifier = owner + "/" + name

        # insert project if not exists
        proj_coll = conn["crossd"]["projects"]
        doc = proj_coll.createDocument({"identifier": identifier, "scans": []})
        try:
            doc.save()
        except pyArango.theExceptions.UniqueConstrainViolation:
            pass  # already exists

        # insert one tag document per tag, ignoring duplicates
        for tag in args.tag:
            tag_doc = tags_coll.createDocument({"identifier": identifier, "tag": tag})
            try:
                tag_doc.save()
            except pyArango.theExceptions.UniqueConstrainViolation:
                pass  # already exists

        print("{}: added tags={}".format(identifier, args.tag))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a repository to the queue")
    parser.add_argument(
        metavar="owner/name",
        help="owner of the repository",
        dest="owner_with_name",
        nargs="+",
    )
    parser.add_argument("--user", help="arangodb username", default="worker")
    parser.add_argument("--password", help="arangodb password", default="worker")
    parser.add_argument(
        "--arango-url",
        help="arangodb URL",
        default="https://arangodb-cluster-internal:8529",
    )
    parser.add_argument(
        "-t", "--tag", action="append", help="Set a tag for the scan", default=[]
    )
    args = parser.parse_args()
    main(args)
