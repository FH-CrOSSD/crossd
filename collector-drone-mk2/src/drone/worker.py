# -*- coding=utf-8 -*-
from celery import Celery, Task
import re
from crossd_metrics.Repository import Repository


class CollectTask(Task):
    # def on_failure(self, exc, task_id, args, kwargs, einfo):
    #     print('{0!r} failed: {1!r}'.format(task_id, exc))
    metric_app = Celery(
        "metric",
        broker="redis://redis-service:6379/1",
        # backend="arangodb://root:@arangodb-cluster-internal:8529/crossd/task-results",
        broker_connection_retry_on_startup=True,
    )

    def on_success(self, retval, task_id, args, kwargs):
       self.metric_app.send_task("do_metrics", (retval,))


app = Celery(
    "collect",
    broker="redis://redis-service:6379/0",
    backend="arangodb://root:@arangodb-cluster-internal:8529/crossd/task_results",
    broker_connection_retry_on_startup=True,
    arangodb_backend_settings={
        "http_protocol": "https",
        "username": "root",
        "password": "",
        # "database": "crossd",
    },
)


@app.task(name="retrieve_github", base=CollectTask)
def retrieve_github(owner: str, name: str):
    return Repository(owner, name).ask_all().execute()
    # return (Repository(owner, name)
    #         # .ask_dependencies()
    #         .ask_funding_links()
    #         .ask_security_policy()
    #         .ask_contributing()
    #         .ask_feature_requests()
    #         .ask_closed_feature_requests()
    #         .ask_dependents()
    #         .ask_pull_requests()
    #         .ask_readme()
    #         .ask_workflows()
    #         .execute())


@app.task(name="retrieve_github_url", base=CollectTask)
def retrieve_github_url(url: str):
    parts = re.match(r"(?:http[s]*://)*github\.com/([^/]*)/([^/]*)", url).groups()
    return retrieve_github(*parts)
