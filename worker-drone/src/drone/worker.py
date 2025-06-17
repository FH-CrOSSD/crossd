# -*- coding=utf-8 -*-
import datetime
import importlib.metadata
import os
import re
import time

import pyArango
from celery import Celery, Task
from crossd_metrics.constants import readmes
from crossd_metrics.metrics import get_metrics
from crossd_metrics.MultiUser import MultiUser
from crossd_metrics.Repository import Repository
from crossd_metrics.utils import get_readme_index, merge_dicts, get_past
from dateutil.relativedelta import relativedelta
from rich.console import Console
from pyArango.theExceptions import DocumentNotFoundError

# for logging

console = Console(force_terminal=True)
err_console = Console(stderr=True, style="bold red")


class BaseTask(Task):
    """Class for Celery Tasks defining basic behaviour in case of success/failure.
    Provides singleton-like instance of the necessary datbase collection.
    """

    _repos = None
    _metrics = None
    _commits = None

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

    @property
    def commits(self):
        if self._commits is None:
            self._commits = self._get_collection("commits")
        return self._commits

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

    commits_since = None
    commits_since_clone = None
    commits=None
    try:
        commits = self.commits.fetchDocument(f"{owner}/{name}", rawResults=True)
    except DocumentNotFoundError:
        pass

    if commits:
        try:
            commits_since = commits["gql"]["repository"]["defaultBranchRef"]["last_commit"][
                "history"
            ]["edges"][0]["node"]["committedDate"]
            commits_since = (
                datetime.datetime.fromisoformat(commits_since) + datetime.timedelta(seconds=1)
            ).isoformat()
        except KeyError:
            pass
        try:
            commits_since_clone = datetime.datetime.fromisoformat(
                commits["clone"]["commits"][0]["committed_iso"]
            ) + datetime.timedelta(seconds=1)

        except KeyError:
            pass

    print("commits_since_clone")
    print(commits_since_clone)
    repo = Repository(owner, name)
    count_res = repo.ask_commits_count(
        commits_since_clone
        if commits_since_clone
        else get_past(relativedelta(months=12)).isoformat()
    ).execute()
    print(f"count_res {count_res}")

    clone_opts = {
        "bare": True,
        "depth": count_res["repository"]["defaultBranchRef"]["last_commit"]["history"][
            "totalCount"
        ],
        # "filter": "blob:none",
    }
    repo = Repository(owner=owner, name=name)

    repo.ask_identifiers()
    # c_available = repo.contributors_available()
    c_available = False

    if c_available:
        repo.clone_opts = clone_opts
        repo.ask_contributors()
        repo.ask_commits_clone()  # defaults to last 12 month
    else:
        repo.clone_opts = clone_opts
        print("store commits")
        repo.ask_commits(details=False, diff=False, since=commits_since)
        repo.ask_commits_clone(since=commits_since_clone or relativedelta(months=12))
    (
        repo.ask_dependencies_sbom()
        # .ask_dependencies_crawl()
        # .ask_dependencies()
        .ask_funding_links()
        .ask_security_policy()
        .ask_contributing()
        .ask_feature_requests()
        .ask_closed_feature_requests()
        .ask_dependents()
        .ask_pull_requests()
        .ask_readme()
        .ask_workflows()
        .ask_identifiers()
        .ask_description()
        .ask_license()
        .ask_dates()
        .ask_subscribers()
        .ask_community_profile()
        .ask_contributors()
        .ask_releases()
        # .ask_releases_crawl()
        .ask_security_advisories()
        .ask_issues()
        .ask_forks()
        # .ask_workflow_runs()
        # .ask_dependabot_alerts()
        # .ask_commits_clone()
        # .ask_commits()
        # .ask_commit_files()
        # .ask_commit_details()
        .ask_branches()
    )

    # retrieve github data
    res = repo.execute(rate_limit=True, verbose=True)
    if not c_available:
        res["repository"]["defaultBranchRef"]["last_commit"]["history"]["edges"] = ["repository"][
            "defaultBranchRef"
        ]["last_commit"]["history"]["edges"] + commits["gql"]["repository"]["defaultBranchRef"][
            "last_commit"
        ][
            "history"
        ][
            "edges"
        ]

        users = {}

        for commit in res["repository"]["defaultBranchRef"]["last_commit"]["history"]["edges"]:
            user = commit["node"]["author"]["user"]
            if not user:
                user = commit["node"]["committer"]["user"]
                if not user:
                    continue
            if user["login"] not in users:
                users[user["login"]] = 0
            users[user["login"]] += 1
        res["contributors"] = {"users": [{"login": x, "contributions": users[x]} for x in users]}

    # res = Repository(owner, name).ask_all().execute()

    users = []
    tmp = {}

    # ~ 400 users failed quite often
    # therefore split to requests of 200 users

    for user in res["contributors"]["users"]:
        if "[bot]" not in user["login"]:
            users.append(user["login"])
        if len(users) % 200 == 0:
            tmp = merge_dicts(
                tmp, MultiUser(login=users).ask_organizations().execute(rate_limit=True)
            )
            users = []
    else:
        tmp = merge_dicts(tmp, MultiUser(login=users).ask_organizations().execute(rate_limit=True))

    console.log(res)
    res["organizations"] = tmp

    res["task_id"] = self.request.id
    res["timestamp"] = time.time()
    res["scan_id"] = scan
    res["version"] = importlib.metadata.version("crossd_metrics")
    res["repository"]["readmes"] = {}
    # for readme in readmes:
    #     res["repository"]["readmes"][get_readme_index(readme)] = res["repository"][
    #         get_readme_index(readme)
    #     ]
    #     del res["repository"][get_readme_index(readme)]
    cm = {
        "_key": f"{owner}/{name}",
        "identifier": f"{owner}/{name}",
        "clone": res["commits"] + commits["clone"],
        "gql": res["repository"]["defaultBranchRef"]["last_commit"]["history"]["edges"], # already contains the new items
    }
    cdoc = self.commits.createDocument(initDict=cm).save()
    cdoc.save()
    # _key should already have an index
    # self.repos.ensurePersistentIndex(["scan_id"], unique=False)

    res["repository"]["defaultBranchRef"]["last_commit"]["history"]["edges"] = []

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

    # this doc is mandatory
    res = app.backend.db["repositories"].fetchDocument(retval["repository_key"], rawResults=True)
    # commits are not mandatory (to be stored separatedly)
    try:
        commits = self.commits.fetchDocument(res["repository"]["nameWithOwner"], rawResults=True)
        res["repository"]["defaultBranchRef"]["last_commit"]["history"]["edges"] = commits["gql"]
        res["commits"] = commits["clone"]
    except DocumentNotFoundError:
        pass

    res = get_metrics(res)

    res["task_id"] = self.request.id
    res["timestamp"] = time.time()
    res["scan_id"] = retval["scan_id"]
    res["version"] = importlib.metadata.version("crossd_metrics")
    console.print("storing metric data in database")
    self.metrics.createDocument(initDict=res).save()
    self.metrics.ensurePersistentIndex(["scan_id"], unique=False)
    return res
