#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import datetime
import getpass
from urllib.parse import urlparse

import pyArango.connection


def URL(arg):
    url = urlparse(arg)
    if not all([url.scheme, url.netloc]):
        raise ValueError("not a valid url")
    return url


def main(args):
    if args.password == None:
        args.password = getpass.getpass("Arango Password: ")
    conn = pyArango.connection.Connection(
        arangoURL=args.url.geturl(),
        username=args.user,
        password=args.password,
        verify=True,
    )

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the duration of a scan")
    parser.add_argument(help="task to search for", dest="tags", nargs="+")
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
    args = parser.parse_args()
    main(args)
