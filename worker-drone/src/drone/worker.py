# -*- coding=utf-8 -*-
import datetime
import importlib.metadata
import os
import re
import time

import gql.transport.exceptions  # type: ignore[import]
import pyArango
import requests
import urllib3
from celery import Celery, Task
from crossd_metrics.constants import readmes
from crossd_metrics.metrics import get_metrics
from crossd_metrics.MultiUser import MultiUser
from crossd_metrics.Repository import Repository
from crossd_metrics.utils import get_past, get_readme_index, merge_dicts
from dateutil.relativedelta import relativedelta
from pyArango.theExceptions import DocumentNotFoundError
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
    _commits = None

    @staticmethod
    def chunks(lst, size):
        for i in range(0, len(lst), size):
            yield lst[i : i + size]

    @staticmethod
    def chunks_reversed(lst, size):
        for i in range(len(lst), 0, -size):
            yield lst[max(0, i - size) : i]

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

app.backend.connection.timeout = 200
app.backend.connection.resetSession(
    username=os.environ.get("WORKER_USER", "root"),
    password=os.environ.get("WORKER_PASSWORD", ""),
    verify=True,
)


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
    # commits = None
    # commit_query = None

    # get current identifier (e.g. username might have changed and redirects now, e.g. google/jax to jax-ml/jax)
    repo = Repository(owner, name)
    res = repo.ask_identifiers().execute()

    # get datetimes of last commits
    query = """
        FOR c IN commits
        FILTER c.identifier == @ident
        LIMIT 1
        RETURN {identifier: c.identifier, gql: c.gql[0].node.committedDate, clone: c.clone[0].committed_iso}
        """
    vars = {
        "ident": res["repository"]["nameWithOwner"],
    }
    qres = app.backend.db.AQLQuery(query, rawResults=True, bindVars=vars)
    if qres:
        if qres[0]["gql"]:
            commits_since = (
                (datetime.datetime.fromisoformat(qres[0]["gql"]) + datetime.timedelta(seconds=1))
                # .replace(hour=0, minute=0, second=0, microsecond=0)
                .isoformat()
            )

        if qres[0]["clone"]:
            commits_since_clone = datetime.datetime.fromisoformat(
                qres[0]["clone"]
            ) + datetime.timedelta(seconds=1)

    repo = Repository(owner, name)
    count_res = (
        repo.ask_repo_empty()
        .ask_commits_count(
            commits_since_clone.isoformat()
            if commits_since_clone
            else get_past(relativedelta(months=12))
            # .replace(hour=0, minute=0, second=0, microsecond=0)
            .isoformat()
        )
        .execute()
    )
    # print(f"count_res {count_res}")

    try:
        count = count_res["repository"]["defaultBranchRef"]["last_commit"]["history"]["totalCount"]
    except TypeError:
        # in case of an empty repository
        count = 0

    clone_opts = {
        "bare": True,
        "depth": count
        + 1,  # might need the previous commit to calc the diff even if it is not in the time range
        # "filter": "blob:none",
    }

    print(count)
    repo = Repository(owner=owner, name=name)
    # c_available = repo.contributors_available()
    c_available = False
    res = None

    def ask_stuff():
        repo.ask_identifiers()

        if c_available:
            repo.clone_opts = clone_opts
            # github contributors rest api seems to be unreliable
            # e.g. Ebazhanov/linkedin-skill-assessments-quizzes
            # website shows 1606 contributors
            # rest api call results in 459 contributors
            repo.ask_contributors()
            repo.ask_commits_clone()  # defaults to last 12 month
        else:
            repo.clone_opts = clone_opts
            console.log("get commits")
            repo.ask_commits(details=False, diff=False, since=commits_since)
            # if count > 0:
            print(
                commits_since_clone
                or get_past(
                    relativedelta(months=12)
                )  # .replace(hour=0, minute=0, second=0, microsecond=0)
            )
            repo.ask_commits_clone(
                since=commits_since_clone
                or get_past(
                    relativedelta(months=12)
                )  # .replace(hour=0, minute=0, second=0, microsecond=0)
            )
        (
            repo.ask_dependencies_sbom()
            # .ask_dependencies_crawl()
            # .ask_dependencies()
            .ask_repo_empty()
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
            # .ask_contributors()
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
            .ask_homepage_url()
            .ask_pull_request_templates()
            .ask_issue_templates()
            .ask_code_of_conduct()
            .ask_contributing_guidelines()
            .ask_issue_template_folder()
        )

    for page_size in (100, 70, 50, 30):
        console.log(f"using page size {page_size}")
        repo = Repository(owner=owner, name=name, page_size=page_size)
        ask_stuff()
        try:
            # retrieve github data
            res = repo.execute(rate_limit=True, verbose=True)
            break
        except requests.exceptions.RetryError as rre:
            if rre.args and isinstance(rre.args[0], urllib3.exceptions.MaxRetryError):
                if rre.args[0].reason and isinstance(
                    rre.args[0].reason, urllib3.exceptions.ResponseError
                ):
                    if rre.args[0].reason.args and any(
                        (x in rre.args[0].reason.args[0] for x in ("502", "504"))
                    ):
                        console.log("page size too large, queries timed out")
                        continue
                        # repo = Repository(
                        #     owner=owner, name=name, page_size=page_size
                        # )  # , clone_opts=clone_opts)
                        # ask_stuff()
                        # res = repo.execute(rate_limit=True, verbose=True)
            raise rre
    else:
        console.log("attempts with reduced page sizes failed")
        console.log("aborting")
        raise RuntimeError("Github is taking too long to answer graphql queries")
    # handle repos without any commits
    try:
        res["repository"]["defaultBranchRef"]["last_commit"]["history"]["edges"]
    except TypeError:
        res["repository"]["defaultBranchRef"] = {"last_commit": {"history": {"edges": []}}}

    # store new commits
    if not count_res["repository"]["isEmpty"]:
        if "commits" not in res:
            res["commits"] = []
        comms = res["commits"]

        query = """
        UPSERT {identifier: @ident}
        INSERT {identifier: @ident, clone: @clone, gql: @gql}
        UPDATE {clone: APPEND(@clone, OLD.clone), gql: APPEND(@gql, OLD.gql)}
        IN commits
        """
        vars = {
            "ident": res["repository"]["nameWithOwner"],
            "clone": comms[-10000:],
            "gql": res["repository"]["defaultBranchRef"]["last_commit"]["history"]["edges"][
                -10000:
            ],
        }
        app.backend.db.AQLQuery(query, rawResults=True, bindVars=vars)

        query = """
            FOR c IN commits
            FILTER c.identifier == @ident
            UPDATE { _key: c._key, gql: APPEND(@gql , c.gql ) } IN commits
            """
        for chunk in self.chunks_reversed(
            res["repository"]["defaultBranchRef"]["last_commit"]["history"]["edges"][:-10000], 10000
        ):
            vars = {
                "ident": res["repository"]["nameWithOwner"],
                "gql": chunk,
            }
            app.backend.db.AQLQuery(query, rawResults=True, bindVars=vars)

        query = """
            FOR c IN commits
            FILTER c.identifier == @ident
            UPDATE { _key: c._key, clone: APPEND(@clone , c.clone ) } IN commits
            """
        for chunk in self.chunks_reversed(comms[:-10000], 10000):
            vars = {
                "ident": res["repository"]["nameWithOwner"],
                "clone": chunk,
            }
            app.backend.db.AQLQuery(query, rawResults=True, bindVars=vars)

    if not c_available:
        query = """
            FOR c IN commits
            FILTER c.identifier == @ident
            FOR u IN c.gql
            LET x = u.node.author.user.login OR u.node.committer.user.login
            FILTER x //remove none
            COLLECT r = x WITH COUNT INTO length
            RETURN {login: r, contributions: length}
            """
        vars = {
            "ident": res["repository"]["nameWithOwner"],
        }
        qres = app.backend.db.AQLQuery(query, rawResults=True, bindVars=vars)
        res["contributors"] = {"users": list(qres)}
        # if commits:
        #     res["repository"]["defaultBranchRef"]["last_commit"]["history"]["edges"] = (
        #         res["repository"]["defaultBranchRef"]["last_commit"]["history"]["edges"]
        #         + commits["gql"]
        #     )

        # users = {}

        # # if "defaultBranchRef" in res["repository"]:
        # # did ask for commits
        # if not count_res["repository"]["isEmpty"]:
        #     for commit in res["repository"]["defaultBranchRef"]["last_commit"]["history"]["edges"]:
        #         user = commit["node"]["author"]["user"]
        #         if not user:
        #             user = commit["node"]["committer"]["user"]
        #             if not user:
        #                 continue
        #         if user["login"] not in users:
        #             users[user["login"]] = 0
        #         users[user["login"]] += 1
        # res["contributors"] = {"users": [{"login": x, "contributions": users[x]} for x in users]}

    # res = Repository(owner, name).ask_all().execute()

    # users = []
    tmp = {}

    # ~ 400 users failed quite often
    # therefore split to requests of 200 users
    groups = [[]]
    index = 0
    for user in res["contributors"]["users"]:
        # if "[bot]" not in user["login"]:
        if all(x not in user["login"] for x in ("[bot]",)) and all(
            x != user["login"] for x in ("Copilot",)
        ):
            # users.append(user["login"])
            if len(groups[index]) >= 200:
                index += 1
                groups.append([])
            groups[index].append(user["login"])

    index = 0
    while index < len(groups):
        try:
            gql_users = MultiUser(login=groups[index]).ask_organizations().execute(rate_limit=True)
            index += 1
            tmp = merge_dicts(tmp, gql_users)
        except gql.transport.exceptions.TransportQueryError as tqe:
            if (
                tqe.errors
                and tqe.errors[0]["type"] == "NOT_FOUND"
                and (
                    match := re.match(
                        r"Could not resolve to a User with the login of '(.+)'.",
                        tqe.errors[0]["message"],
                    )
                )
            ):
                user = match.groups()[0]
                groups[index].remove(user)
                console.log(f"Github GQL could not find user {user} - removed")
            elif tqe.errors and tqe.errors[0]["type"] == "RESOURCE_LIMITS_EXCEEDED":
                console.log("RESOURCE_LIMITS_EXCEEDED - trying with smaller group size")
                orig = groups[index]
                groups[index] = orig[0 : len(orig) // 2]
                groups.insert(index + 1, orig[len(orig) // 2 : len(orig)])
            else:
                raise tqe

    # for user in res["contributors"]["users"]:
    #     # if "[bot]" not in user["login"]:
    #     if all(x not in user["login"] for x in ("[bot]",)) and all(
    #         x != user["login"] for x in ("Copilot",)
    #     ):
    #         users.append(user["login"])
    #     if len(users) % 200 == 0:
    #         gql_users = {}
    #         try:
    #             gql_users = MultiUser(login=users).ask_organizations().execute(rate_limit=True)
    #         except gql.transport.exceptions.TransportQueryError as tqe:
    #             if tqe.errors and tqe.errors[0]["type"] == "RESOURCE_LIMITS_EXCEEDED":
    #                 console.log("RESOURCE_LIMITS_EXCEEDED - trying with smaller group size")
    #                 gql_users = merge_dicts(
    #                     MultiUser(login=users[:100]).ask_organizations().execute(rate_limit=True),
    #                     MultiUser(login=users[100:]).ask_organizations().execute(rate_limit=True),
    #                 )
    #             else:
    #                 gql_users = {key: value for key, value in tqe.data.items() if value is not None}
    #         tmp = merge_dicts(tmp, gql_users)
    #         users = []
    # else:
    #     # tmp = merge_dicts(tmp, MultiUser(login=users).ask_organizations().execute(rate_limit=True))
    #     try:
    #         gql_users = MultiUser(login=users).ask_organizations().execute(rate_limit=True)
    #     except gql.transport.exceptions.TransportQueryError as tqe:
    #         gql_users = {key: value for key, value in tqe.data.items() if value is not None}
    #     tmp = merge_dicts(tmp, gql_users)

    # console.log(res)
    res["organizations"] = tmp

    res["task_id"] = self.request.id
    res["timestamp"] = time.time()
    res["scan_id"] = scan
    res["version"] = importlib.metadata.version("crossd_metrics")
    res["repository"]["readmes"] = {}

    res["repository"]["defaultBranchRef"]["last_commit"]["history"]["edges"] = []

    res["commits"] = []

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
    query = """
        FOR c IN commits
        FILTER c.identifier == @ident
        RETURN c.clone
        """
    vars = {
        "ident": res["repository"]["nameWithOwner"],
    }
    qres = app.backend.db.AQLQuery(query, rawResults=True, bindVars=vars)
    try:
        res["commits"] = qres[0]
    except IndexError:
        console.log("no commits found")
        pass
    # try:
    #     # commits = self.commits.fetchDocument(res["repository"]["nameWithOwner"], rawResults=True)
    #     commits = self.commits.fetchFirstExample(
    #         {"identifier": res["repository"]["nameWithOwner"]}, rawResults=True
    #     )
    #     if len(commits) > 0:
    #         res["repository"]["defaultBranchRef"]["last_commit"]["history"]["edges"] = commits[0][
    #             "gql"
    #         ]
    #         res["commits"] = commits[0]["clone"]
    # except DocumentNotFoundError:
    #     pass

    # console.print(len(res["commits"]))
    # console.print(len(res["repository"]["defaultBranchRef"]["last_commit"]["history"]["edges"]))
    res = get_metrics(res)

    res["task_id"] = self.request.id
    res["timestamp"] = time.time()
    res["scan_id"] = retval["scan_id"]
    res["version"] = importlib.metadata.version("crossd_metrics")
    console.print("storing metric data in database")
    self.metrics.createDocument(initDict=res).save()
    self.metrics.ensurePersistentIndex(["scan_id"], unique=False)
    return res
