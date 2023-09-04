#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from mdi_thesis.base.base import *
from arango import ArangoClient
import time
import requests
requests.packages.urllib3.disable_warnings()

def main():
    """
    Main in progress
    """

    # repo_ids_path = "mdi_thesis/preselected_repos.txt"
    # repo_ids = utils.__get_ids_from_txt__(path=repo_ids_path)
    selected_repos = Request()
    # Statement for selecting number of queried repositories
    # selected_repos.select_repos(repo_nr=1, order="desc")
    # Statement for selecting repositories according to list (for developing)
    selected_repos.select_repos(repo_list=[123458551])

    # print(selected_repos.selected_repos_dict)

    # print(selected_repos.get_single_object(feature="issue_comments"))

    # health = selected_repos.get_repo_request(["community_health"])
    health = selected_repos.query_repository(["community_health"], {})
    print(health)
    # "forks" 1914 pages
    # .get("community_health")  # .get(191113739))
    # print(len(selected_repos.get_repo_request(["community_health"])))
    # .get("community_health")  # .get(191113739)))

        # Initialize the ArangoDB client.
    client = ArangoClient(hosts='https://arangodb-cluster-internal:8529',verify_override=False)

    # Connect to "_system" database as root user.
    # This returns an API wrapper for "_system" database.
    sys_db = client.db('_system', username='root', password='')

    # Create a new database named "test" if it does not exist.
    if not sys_db.has_database('test'):
        sys_db.create_database('test')

    # Connect to "test" database as root user.
    # This returns an API wrapper for "test" database.
    db = client.db('test', username='root', password='')

    # Create a new collection if it does not exist.
    # This returns an API wrapper for the collection.
    if db.has_collection('health'):
        col = db.collection('health')
    else:
        col = db.create_collection('health')

    # Add a hash index to the collection.
    # col.add_hash_index(fields=['name'], unique=False)

    # Truncate the collection.
    # col.truncate()

    # Insert new documents into the collection.
    col.insert({**health, "time":time.time()})
    # col.insert({'name': 'josh', 'age': 18})
    # col.insert({'name': 'jake', 'age': 21})

    # Execute an AQL query. This returns a result cursor.
    cursor = db.aql.execute('FOR doc IN health RETURN doc')

    # Iterate through the cursor to retrieve the documents.
    docs = [document for document in cursor]
    print(str(len(docs)))

if __name__ == "__main__":
    main()
