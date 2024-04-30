#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import datetime
import getpass
from urllib.parse import urlparse
from pprint import pprint

import pyArango.connection


def URL(arg):
    url = urlparse(arg)
    if not all([url.scheme, url.netloc]):
        raise ValueError("not a valid url")
    return url


def duration(conn, args):
    # lists only completed
    query = """
    LET x =(FOR scan IN scans
    LET y = (
        FOR tag in @tags
        return tag in scan.tags
    )
    FILTER !(false in y)
    FOR doc IN task_results
    FILTER CONTAINS(doc.task, CONCAT(scan._id))
    LET task = JSON_PARSE(doc.task)
    SORT task.date_done
    FILTER task.date_done
    RETURN task.date_done)
    RETURN [first(x), last(x)]
    """

    vars = {"tags": args.tags}
    res = conn["crossd"].AQLQuery(query, rawResults=True, bindVars=vars)
    if res[0] == [None, None]:
        print("No results found")
        exit()

    print(res[0])
    start = datetime.datetime.fromisoformat(res[0][0])
    end = datetime.datetime.fromisoformat(res[0][1])
    print(end - start)


def tags(conn, args):
    query = """
    for scan in scans
    filter scan.tags != null
    return distinct scan.tags
    """
    res = conn["crossd"].AQLQuery(query, rawResults=True)
    for i, elem in enumerate(res):
        print(str(i) + ": " + " ".join(repr(tag) for tag in elem))


def get_not_found(conn, args):
    query = """
    FOR doc IN task_results
    FILTER doc.task LIKE '%FAILURE%'
    LET task=JSON_PARSE(doc.task)
    FILTER task.result.exc_type == "TransportQueryError"
    FILTER task.result.exc_message[0] LIKE "%NOT_FOUND%"
    RETURN DISTINCT CONCAT(task.args[0],"/",task.args[1])
    """
    res = conn["crossd"].AQLQuery(query, rawResults=True)
    for elem in res:
        print(elem)


def main(args):
    if any([args.password in [None, "-"]]):
        args.password = getpass.getpass("Arango Password: ")
    conn = pyArango.connection.Connection(
        arangoURL=args.url.geturl(),
        username=args.user,
        password=args.password,
        verify=True,
    )
    args.func(conn, args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ArangoDB helper tools")
    parser.add_argument("--user", help="arangodb username", default="root")
    parser.add_argument(
        "--url", help="arangodb username", type=URL, default="http://127.0.0.1"
    )
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        help="arangodb password",
        nargs="?",
        required=True,
    )

    subparsers = parser.add_subparsers(required=True)

    parser_duration = subparsers.add_parser(
        "duration", description="Get the duration of a scan"
    )
    parser_duration.add_argument(help="task to search for", dest="tags", nargs="+")
    parser_duration.set_defaults(func=duration)

    parser_tags = subparsers.add_parser(
        "tags", description="Get all tags from the database"
    )
    parser_tags.set_defaults(func=tags)

    parser_tags = subparsers.add_parser(
        "notfound", description="Get all repositories that were not found"
    )
    parser_tags.set_defaults(func=get_not_found)

    args = parser.parse_args()
    main(args)
