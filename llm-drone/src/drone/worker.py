# -*- coding=utf-8 -*-
import datetime
import importlib.metadata
import os
import re
import time

import pyArango
import requests
import json
import urllib3
from celery import Celery, Task

# from crossd_metrics.constants import readmes
# from crossd_metrics.metrics import get_metrics
# from crossd_metrics.MultiUser import MultiUser
# from crossd_metrics.Repository import Repository
# from crossd_metrics.utils import get_past, get_readme_index, merge_dicts
from dateutil.relativedelta import relativedelta
from pyArango.theExceptions import DocumentNotFoundError
from rich.console import Console
from llm_metrics.main import select_metrics, print_report
from llm_metrics.graph import analyse_repo
from llm_metrics.config import MetricDefinition
from dateutil.relativedelta import relativedelta
import datetime
from typing import Callable

# for logging

console = Console(force_terminal=True)
err_console = Console(stderr=True, style="bold red")

METRICS: list[MetricDefinition] = [
    # ── Simple single-agent metrics ──────────────────────────────────────
    MetricDefinition(
        name="friendliness",
        display_name="Developer Friendliness",
        description="How friendly and welcoming are the developers in issues and comments?",
        prompt=(
            "Evaluate how friendly and welcoming the repository developers are "
            "when interacting with contributors and users in issues and comments. "
            "Consider tone, responsiveness, helpfulness, and encouragement. "
            "Give a score from {min} to {max} where {min} is hostile/unwelcoming "
            "and {max} is exceptionally friendly and supportive."
        ),
        pipeline="single",
        data_keys=["issues", "community_profile"],
    ),
    MetricDefinition(
        name="documentation_quality",
        display_name="Documentation Quality",
        description="Quality and professionalism of documentation, READMEs, and guides.",
        prompt=(
            "Analyse the quality of documentation in this repository. Consider the "
            "README structure, whether there are contributing guides, code of conduct, "
            "issue/PR templates, and external docs links. "
            "Give a score from {min} to {max} where {min} is poor and {max} is excellent."
        ),
        pipeline="single",
        data_keys=["community_profile", "readme", "contributing"],
    ),
    # ── Multi-agent debate metrics (using default analyst + reviewer) ────
    MetricDefinition(
        name="development_efficiency",
        display_name="Development Efficiency",
        description="How efficiently is development conducted? Issue turnaround, branching, PRs, releases.",
        prompt=(
            "Evaluate how efficiently development is conducted in this repository. "
            "Consider issue resolution time, PR turnaround, branching strategy, "
            "release cadence, commit activity, and contributor productivity. "
            "Give a score from {min} to {max} where {min} is very inefficient "
            "and {max} is highly efficient."
        ),
        pipeline="single",
        data_keys=[
            "issues",
            "pulls",
            "branches",
            "releases",
            "commits",
            "contributors",
        ],
    ),
    # ── Multi-agent debate with custom agents ────────────────────────────
    MetricDefinition(
        name="project_maturity",
        display_name="Project Maturity",
        description="Overall maturity of the project considering governance, processes, and community.",
        scale=(1, 100),
        prompt=(
            "Evaluate the overall maturity of this open-source project. "
            "Score holistically across ALL of the following dimensions — "
            "no single dimension should dominate:\n"
            "  • Governance: code of conduct, contributing guide, issue/PR templates\n"
            "  • Community: contributor count, bus-factor, PR activity, issue responsiveness\n"
            "  • Release & versioning: release history, cadence, tagging\n"
            "  • Documentation: README quality, external docs, changelogs\n"
            "  • CI/CD & automation: automated tests, build pipelines\n"
            "  • Security posture: security policy presence, advisory count/severity, "
            "patch responsiveness — treat this as ONE of the six dimensions above, "
            "not a veto over the others\n\n"
            "Give a score from {min} to {max} in increments of 0.1 where {min} is very immature "
            "and {max} is a fully mature project."
        ),
        pipeline="single",
        data_keys=[
            "issues",
            "pulls",
            "branches",
            "releases",
            "commits",
            "contributors",
            "community_profile",
            "dependencies",
            "advisories",
        ],
    ),
]


def date_filter(
    data: list[dict],
    selector: Callable[[dict], str],
    since: datetime.datetime | relativedelta,
) -> list[dict]:
    """
    Filter a list of dictionaries based on a date.

    Args:
        data: list[dict]: The list of dictionaries to be filtered.
        selector: Callable: A function that takes a dictionary and returns a date ISO8601 string.
        since: datetime.datetime | datetime.timedelta: The date or time duration to filter the data. (Default value = datetime.timedelta(days=30 * 6))
    Returns:
        list[dict]: A list of dictionaries that match the date filter.
    """
    if type(since) == datetime.datetime:
        # if since is a datetime object, use it as is
        past = since
    elif type(since) == relativedelta:
        # if since is a timedelta object, use it to calculate the past date
        past = datetime.datetime.now(datetime.UTC) - since
    else:
        raise TypeError(
            "since not of type datetime.datetime, dateutil.relativedelta.relativedelta"
        )

    res = []
    for elem in data:
        if datetime.datetime.fromisoformat(selector(elem)) > past:
            res.append(elem)
    return res


class BaseTask(Task):
    """Class for Celery Tasks defining basic behaviour in case of success/failure.
    Provides singleton-like instance of the necessary datbase collection.
    """

    _repos = None

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
    def ai_metrics(self):
        if self._repos is None:
            self._repos = self._get_collection("ai_metrics")
        return self._repos

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        err_console.print(f"failed to execute task {task_id}")
        err_console.print(einfo)

    def on_success(self, retval, task_id, args, kwargs):
        console.print(f"[green]successfully completed task {task_id}[/]")


app = Celery(
    "collect",
    broker="rediss://:{}@redis-service:6379/0?ssl_cert_reqs=required".format(
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
    "do_llm_metrics": {"queue": "llm_metrics", "routing_key": "llm_metrics"},
}

# include eg. task arguments in results
app.conf.result_extended = True

app.backend.connection.timeout = 200
app.backend.connection.resetSession(
    username=os.environ.get("WORKER_USER", "root"),
    password=os.environ.get("WORKER_PASSWORD", ""),
    verify=True,
)


@app.task(
    name="do_llm_metrics",
    bind=True,
    base=BaseTask,
    autoretry_for=(Exception,),
    retry_backoff=10 * 60,
    max_retries=0,
    retry_backoff_max=3500 * 60,
    retry_jitter=True,
)
def do_llm_metrics(self, retval: str):
    """Uses the retrieved repository data to calculate metrics.

    Args:
        retval: data collected by retrieve_github task.
    """
    console.print("starting task [dodger_blue1]do_metrics[/]")
    console.print("calculating metrics")
    # retrieve repo data from db and calculate metrics

    # this doc is mandatory
    res = app.backend.db["repositories"].fetchDocument(
        retval["repository_key"], rawResults=True
    )
    print(retval)
    print(res)

    repo_data = res
    repo_slug = repo_data.get("repository", {}).get("nameWithOwner")

    snapshot_timestamp = None  # may still be None if auto-selected
    # If auto-selected, recover the timestamp from the returned data
    if snapshot_timestamp is None:
        snapshot_timestamp = repo_data.get("timestamp")

    # ── Select metrics ───────────────────────────────────────────────────
    metrics = METRICS
    repo_data = {"repository": repo_data}
    print(f"Evaluating {len(metrics)} metric(s): {[m.name for m in metrics]}\n")

    issues_data = date_filter(
        repo_data["repository"]["repository"]["issues"]["edges"],
        lambda x: x["node"]["updatedAt"],
        # datetime.timedelta(days=30 * 3),
        relativedelta(months=1),
    )
    print(f"   ℹ️  {len(issues_data)} issues updated in the last month.")

    numbers = tuple("issue" + str(x["node"]["number"]) for x in issues_data)
    repo_data["repository"]["repository"]["issues"]["edges"] = issues_data

    for key in list(repo_data["repository"]["repository"].keys()):
        if key != "issues" and key.startswith("issue") and key not in numbers:
            del repo_data["repository"]["repository"][key]
    repo_data["repository"]["organizations"] = [
        {
            "login": repo_data["repository"]["organizations"][u]["login"],
            "organizations": repo_data["repository"]["organizations"][u][
                "organizations"
            ]["nodes"],
        }
        for u in repo_data["repository"]["organizations"]
        if "login" in repo_data["repository"]["organizations"][u]
    ]

    repo_data["repository"]["repository"]["releases"]["edges"] = [
        e["node"] for e in repo_data["repository"]["repository"]["releases"]["edges"]
    ]

    repo_data["repository"]["repository"]["branches"]["edges"] = [
        e["branch"] for e in repo_data["repository"]["repository"]["branches"]["edges"]
    ]

    repo_data["repository"]["repository"]["pullRequests"]["edges"] = [
        e["node"]
        for e in repo_data["repository"]["repository"]["pullRequests"]["edges"]
    ]

    repo_data["repository"]["repository"]["issues"]["edges"] = [
        e["node"] for e in repo_data["repository"]["repository"]["issues"]["edges"]
    ]

    # ── Run pipeline ─────────────────────────────────────────────────────
    results = analyse_repo(
        repo_data,
        metrics,
        model=os.environ.get("LLM_MODEL", ""),
        llm_host=os.environ.get("LLM_HOST", ""),
        llm_auth_token=os.environ.get("LLM_AUTH_TOKEN", ""),
        repo_slug=repo_slug,
        snapshot_timestamp=snapshot_timestamp,
        log_dir=os.environ.get("LOG_DIR", ""),
    )

    # ── Output ───────────────────────────────────────────────────────────
    print_report(results)

    llm_res = {elem["name"]: elem for elem in results}

    ai_res = {}
    ai_res["task_id"] = self.request.id
    ai_res["timestamp"] = time.time()
    ai_res["scan_id"] = retval["scan_id"]
    ai_res["result"] = llm_res
    ai_res["identifier"] = res["repository"]["nameWithOwner"]

    console.print("storing ai metric data in database")
    self.ai_metrics.createDocument(initDict=ai_res).save()
    self.ai_metrics.ensurePersistentIndex(["scan_id"], unique=False)
    return ai_res
