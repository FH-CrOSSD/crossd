# -*- coding=utf-8 -*-
import os
import re
import time

import pyArango
from celery import Celery, Task
from crossd_metrics.constants import readmes
from crossd_metrics.metrics import get_metrics
from crossd_metrics.Repository import Repository
from crossd_metrics.utils import get_readme_index
from rich.console import Console

# for logging

console = Console(force_terminal=True)
err_console = Console(stderr=True, style="bold red")


class BaseTask(Task):
    """Class for Celery Tasks defining basic behaviour in case of success/failure.
    Provides singleton-like instance of the necessary datbase collection.
    """

    _repos = None
    _metrics = None

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
    def repos(self):
        if self._repos is None:
            self._repos = self._get_collection("repositories")
        return self._repos

    @property
    def metrics(self):
        if self._metrics is None:
            self._metrics = self._get_collection("metrics")
        return self._metrics

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        err_console.print(f"failed to execute task {task_id}")
        err_console.print(einfo)

    def on_success(self, retval, task_id, args, kwargs):
        console.print(f"[green]successfully completed task {task_id}[/]")


class CollectTask(BaseTask):

    def on_success(self, retval, task_id, args, kwargs):
        super().on_success(retval, task_id, args, kwargs)
        console.print("launched task [dodger_blue1]do_metrics[/]")
        app.send_task("do_metrics", (retval,))


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
    "retrieve_github": {"queue": "collect", "routing_key": "collect"},
    "retrieve_github_url": {"queue": "collect", "routing_key": "collect"},
    "do_metrics": {"queue": "metric", "routing_key": "metric"},
}

# include eg. task arguments in results
app.conf.result_extended = True


@app.task(
    name="retrieve_github",
    base=CollectTask,
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=10 * 60,
    max_retries=5,
    retry_backoff_max=3500 * 60,
    retry_jitter=True,
)
def retrieve_github(self, owner: str, name: str, scan: str, sub: bool = False):
    """Retrieves data from a github repository and stores the results inside ArangoDB.

    Args:
        owner: Owner of the github repository.
        name: Name of the github repository.
        scan: ArangoDB ID of the according scan entry (in the scan collection).
        sub: Is called from another method as part of the same task.
    """

    if not sub:
        console.print("starting task [dodger_blue1]retrieve_github[/]")
    console.print("collecting repository data from github")
    # retrieve github data
    res = Repository(owner, name).ask_all().execute()
    res["task_id"] = self.request.id
    res["timestamp"] = time.time()
    res["scan_id"] = scan
    res["repository"]["readmes"] = {}
    for readme in readmes:
        res["repository"]["readmes"][get_readme_index(readme)] = res["repository"][
            get_readme_index(readme)
        ]
        del res["repository"][get_readme_index(readme)]
    console.print("storing repository data in database")
    doc = self.repos.createDocument(initDict=res)
    self.repos.ensurePersistentIndex(["scan_id"], unique=False)
    doc.save()
    res = {"repository_key": doc._key, "scan_id": scan}
    return res


@app.task(
    name="retrieve_github_url",
    base=CollectTask,
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=10 * 60,
    max_retries=5,
    retry_backoff_max=3500 * 60,
    retry_jitter=True,
)
def retrieve_github_url(self, url: str, scan: str):
    """Retrieves data from a github repository and stores the results inside ArangoDB.

    Args:
        url: github URL of the repository.
        scan: ArangoDB ID of the according scan entry (in the scan collection).
    """
    console.print("starting task [dodger_blue1]retrieve_github_url[/]")
    # extract owner and name per regex
    parts = re.match(r"(?:http[s]*://)*github\.com/([^/]*)/([^/]*)", url).groups()
    return retrieve_github(*parts, scan, sub=True)


@app.task(name="do_metrics", bind=True, base=BaseTask)
def do_metrics(self, retval: str):
    """Uses the retrieved repository data to calculate metrics.

    Args:
        retval: data collected by retrieve_github task.
    """
    console.print("starting task [dodger_blue1]do_metrics[/]")
    console.print("calculating metrics")
    # retrieve repo data from db and calculate metrics
    res = get_metrics(
        app.backend.db["repositories"].fetchDocument(retval["repository_key"])
    )
    res["task_id"] = self.request.id
    res["timestamp"] = time.time()
    res["scan_id"] = retval["scan_id"]
    console.print("storing metric data in database")
    self.metrics.createDocument(initDict=res).save()
    self.metrics.ensurePersistentIndex(["scan_id"], unique=False)
    return res
