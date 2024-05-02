# -*- coding=utf-8 -*-
import json
import os
import os.path
import time
from datetime import date, timedelta

import pyArango
from celery import Celery, Task
from mdi_thesis.base_data_miner import DataMinePipeline
from mdi_thesis.metrics_pipeline import MetricsPipeline
from rich.console import Console

# for logging
console = Console(force_terminal=True)
err_console = Console(stderr=True, style="bold red")

# paths used for cleaning up result files
OUT_PATH = "/home/collector-drone/thesis_metrics-main/outputs"
DATA_PATH = os.path.join(OUT_PATH, "data")
LOGS_PATH = os.path.join(OUT_PATH, "logs")
RESULT_FILE_PATH = os.path.join(OUT_PATH, "results/csv_metrics.json")


class BaseTask(Task):
    """Class for Celery Tasks defining basic behaviour in case of success/failure.
    Provides singleton-like instance of the necessary datbase collection.
    """

    _collection = None

    @staticmethod
    def _get_collection(name: str):
        """Retrieves an instance of a ArangoDB database collection or creates it, if not existing."""
        col = None
        try:
            # get collection
            col = app.backend.db[name]
        except KeyError:
            try:
                # create collection (as it does not exist)
                col = app.backend.db.createCollection(name=name)
            except pyArango.theExceptions.CreationError as ce:
                # might arise if db has been create by another worker in the meantime
                if not app.backend.db.hasCollection(name):
                    # raise other errors
                    err_console.print(ce)
                    raise ce
                else:
                    # retrieve collecitons anew and use the new collection
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
    def on_success(self, retval, task_id, args, kwargs):
        super().on_success(retval, task_id, args, kwargs)
        console.print(f"[green]successfully completed task bak_tasks[/]")


app = Celery(
    "collect",
    broker="redis://:{}@redis-service:6379/0?ssl_cert_reqs=required".format(
        os.environ.get("RAUTH", "")
    ),
    backend="arangodb://{}:@arangodb-cluster-internal:8529/crossd/task_results".format(
        os.environ.get("WORKER_USER", "root")
    ),
    broker_connection_retry_on_startup=True,
    arangodb_backend_settings={
        "http_protocol": "https",
        "username": os.environ.get("WORKER_USER", "root"),
        "password": os.environ.get("WORKER_PASSWORD", ""),
        "verify": True,
    },
)

app.conf.task_routes = {
    "bak_tasks": {"queue": "bak", "routing_key": "bak"},
}
# include eg. task arguments in results
app.conf.result_extended = True


@app.task(
    name="bak_tasks",
    base=CollectTask,
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=10 * 60,
    max_retries=5,
    retry_backoff_max=3500 * 60,
    retry_jitter=True,
)
def bak_tasks(self, owner: str, name: str, scan: str):
    """Retrieves data from a github repository, calculates metrics based on that data and stores the results inside ArangoDB.

    Args:
        owner: Owner of the github repository.
        name: Name of the github repository.
        scan: ArangoDB ID of the according scan entry (in the scan collection).

    """
    # retrieve repository data (stores results in files)
    DataMinePipeline(
        language="csv",
        filter_date=date.today(),
        repo_nr=0,
        get_existing_repos=False,
        repo_list=[f"{owner}/{name}"],
    )

    # read result files and store them in ArangoDB
    data = {}
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".json"):
            data[filename.removesuffix(".json")] = json.loads(
                open(os.path.join(DATA_PATH, filename)).read()
            )

    data["task_id"] = self.request.id
    data["timestamp"] = time.time()
    data["scan_id"] = scan
    data["identity"] = {
        "name": name,
        "owner": owner,
        "name_with_owner": f"{owner}/{name}",
    }
    self._get_collection("bak_repos").createDocument(initDict=data).save()

    # calculate metrics based on repository data and store them in db
    MetricsPipeline(filter_date=date.today() - timedelta(days=1)).run_metrics_to_json()
    res = json.loads(open(RESULT_FILE_PATH).read())
    res["task_id"] = self.request.id
    res["timestamp"] = time.time()
    res["scan_id"] = scan
    res["identity"] = {
        "name": name,
        "owner": owner,
        "name_with_owner": f"{owner}/{name}",
    }
    doc = self.collection.createDocument(initDict=res).save()

    # clean up files created by the task
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".json"):
            os.remove(os.path.join(DATA_PATH, filename))
    for filename in os.listdir(LOGS_PATH):
        if filename.endswith(".log"):
            os.remove(os.path.join(LOGS_PATH, filename))
    os.remove(RESULT_FILE_PATH)

    return res
