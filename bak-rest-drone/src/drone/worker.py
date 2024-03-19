# -*- coding=utf-8 -*-
from celery import Celery, Task
import re

# from crossd_metrics.Repository import Repository
# from crossd_metrics.metrics import get_metrics
# from crossd_metrics.constants import readmes
# from crossd_metrics.utils import get_readme_index
import mdi_thesis.base.base as base
from mdi_thesis.base_data_miner import DataMinePipeline
from mdi_thesis.metrics_pipeline import MetricsPipeline
import pyArango
from rich.console import Console
import time
import json
from datetime import date, timedelta
import os

console = Console(force_terminal=True)
err_console = Console(stderr=True, style="bold red")

# from arango import ArangoClient

# client = ArangoClient(hosts='https://arangodb-cluster-internal:8529',verify_override=False)

# db = client.db('crossd', username='root', password='')

# # Create a new collection if it does not exist.
# # This returns an API wrapper for the collection.
# if db.has_collection('health'):
#     col = db.collection('health')
# else:
#     col = db.create_collection('health')


class BaseTask(Task):
    _collection = None

    @staticmethod
    def _get_collection(name: str):
        col = None
        try:
            col = app.backend.db[name]
        except KeyError:
            try:
                col = app.backend.db.createCollection(name=name)
            except pyArango.theExceptions.CreationError as ce:
                if not app.backend.db.hasCollection(name):
                    err_console.print(ce)
                    raise ce
                else:
                    app.backend.db.reloadCollections()
                    col = app.backend.db[name]
        return col

    @property
    def collection(self):
        if self._collection is None:
            self._collection = self._get_collection("bak_metrics")
        return self._collection

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        err_console.print(f"failed to execute task {task_id}")
        err_console.print(einfo)

    def on_success(self, retval, task_id, args, kwargs):
        console.print(f"[green]successfully completed task {task_id}[/]")


class CollectTask(BaseTask):
    # def on_failure(self, exc, task_id, args, kwargs, einfo):
    #     print('{0!r} failed: {1!r}'.format(task_id, exc))
    # metric_app = Celery(
    #     "metric",
    #     broker="redis://redis-service:6379/0",
    #     # backend="arangodb://root:@arangodb-cluster-internal:8529/crossd/task-results",
    #     broker_connection_retry_on_startup=True,
    # )

    def on_success(self, retval, task_id, args, kwargs):
        super().on_success(retval, task_id, args, kwargs)
        # console.print(f"[green]successfully completed task{task_id}[/]")
        console.print("launched task [dodger_blue1]do_metrics[/]")
        # app.send_task("do_metrics", (retval,))


app = Celery(
    "collect",
    broker="redis://redis-service:6379/0",
    backend="arangodb://{}:@arangodb-cluster-internal:8529/crossd/task_results".format(
        os.environ.get("WORKER_USER", "root")
    ),
    broker_connection_retry_on_startup=True,
    arangodb_backend_settings={
        "http_protocol": "https",
        "username": os.environ.get("WORKER_USER", "root"),
        "password": os.environ.get("WORKER_PASSWORD", ""),
        # "database": "crossd",
    },
)

app.conf.task_routes = {
    "bak_tasks": {"queue": "bak", "routing_key": "bak"},
}


@app.task(name="bak_tasks", base=CollectTask, bind=True)
def bak_tasks(self, owner: str, name: str, scan: str, sub: bool = False):
    DataMinePipeline(
        language="csv",
        filter_date=date.today(),
        repo_nr=0,
        get_existing_repos=False,
        repo_list=[f"{owner}/{name}"],
    )
    MetricsPipeline(filter_date=date.today() - timedelta(days=1)).run_metrics_to_json()
    res = json.loads(
        open(
            "/home/collector-drone/thesis_metrics-main/outputs/results/csv_metrics.json"
        ).read()
    )
    res["task_id"] = self.request.id
    res["timestamp"] = time.time()
    res["scan_id"] = scan
    res["identity"] = {
        "name": name,
        "owner": owner,
        "name_with_owner": f"{owner}/{name}",
    }
    doc = self.collection.createDocument(initDict=res).save()

    # pipeline.run_metrics_to_json()
    return res


# @app.task(name="retrieve_github", base=CollectTask, bind=True)
# def retrieve_github(self, owner: str, name: str, sub: bool = False):
#     if not sub:
#         console.print("starting task [dodger_blue1]retrieve_github[/]")
#     console.print("collecting repository data from github")
#     res = Repository(owner, name).ask_all().execute()
#     res["task_id"] = self.request.id
#     res["timestamp"] = time.time()
#     res["repository"]["readmes"] = {}
#     for readme in readmes:
#         res["repository"]["readmes"][get_readme_index(readme)] = res["repository"][
#             get_readme_index(readme)
#         ]
#         del res["repository"][get_readme_index(readme)]
#     console.print("storing repository data in database")
#     doc = self.repos.createDocument(initDict=res)
#     doc.save()
#     res = {"repository_key": doc._key}
#     return res
#     # return (Repository(owner, name)
#     #         # .ask_dependencies()
#     #         .ask_funding_links()
#     #         .ask_security_policy()
#     #         .ask_contributing()
#     #         .ask_feature_requests()
#     #         .ask_closed_feature_requests()
#     #         .ask_dependents()
#     #         .ask_pull_requests()
#     #         .ask_readme()
#     #         .ask_workflows()
#     #         .execute())


# @app.task(name="retrieve_github_url", base=CollectTask, bind=True)
# def retrieve_github_url(self, url: str):
#     console.print("starting task [dodger_blue1]retrieve_github_url[/]")
#     parts = re.match(r"(?:http[s]*://)*github\.com/([^/]*)/([^/]*)", url).groups()
#     return retrieve_github(*parts, sub=True)


# @app.task(name="do_metrics", bind=True, base=BaseTask)
# def do_metrics(self, retval: str):
#     self.repos
#     console.print("starting task [dodger_blue1]do_metrics[/]")
#     console.print("calculating metrics")
#     res = get_metrics(
#         app.backend.db["repositories"].fetchDocument(retval["repository_key"])
#     )
#     res["task_id"] = self.request.id
#     res["timestamp"] = time.time()
#     console.print("storing metric data in database")
#     self.metrics.createDocument(initDict=res).save()
#     return res