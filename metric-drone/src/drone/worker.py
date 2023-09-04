# -*- coding=utf-8 -*-
from celery import Celery, Task
from celery.result import AsyncResult
import re
from crossd_metrics.Repository import Repository
from crossd_metrics.metrics import get_metrics
from celery.backends.arangodb import ArangoDbBackend

# metric_app = Celery(
#     "metric",
#     broker="redis://redis-service:6379/0",
#     # backend="arangodb://root:@arangodb-cluster-internal:8529/crossd/task-results",
#     broker_connection_retry_on_startup=True,
# )

# class CollectTask(Task):
#     # def on_failure(self, exc, task_id, args, kwargs, einfo):
#     #     print('{0!r} failed: {1!r}'.format(task_id, exc))

#     def on_success(self, retval, task_id, args, kwargs):
#         metric_app.send_task("do_metrics", (task_id,))


metric_app = Celery(
    "metric",
    broker="redis://redis-service:6379/1",
    backend="arangodb://root:@arangodb-cluster-internal:8529/crossd/metric_results",
    broker_connection_retry_on_startup=True,
    arangodb_backend_settings={
        "http_protocol": "https",
        "username": "root",
        "password": "",
        # "database": "crossd",
    },
)


@metric_app.task(name="do_metrics")
def do_metrics(task_id: str):
    # app = Celery(
    #     "collect",
    #     broker="redis://redis-service:6379/0",
    #     backend="arangodb://root:@arangodb-cluster-internal:8529/crossd/task_results",
    #     broker_connection_retry_on_startup=True,
    #     arangodb_backend_settings={
    #         "http_protocol": "https",
    #         "username": "root",
    #         "password": "",
    #         # "database": "crossd",
    #     },
    # )
    # arango = ArangoDbBackend(
    #     url="arangodb://root:@arangodb-cluster-internal:8529/crossd/task_results",
    #     **{
    #         "http_protocol": "https",
    #         "username": "root",
    #         "password": "",
    #         # "database": "crossd",
    #     }
    # )
    # res = AsyncResult(task_id, backend=app.backend).get()
    return get_metrics(task_id)


# @app.task(name="retrieve_github", base=CollectTask)
# def retrieve_github(owner: str, name: str):
#     return Repository(owner, name).ask_all().execute()


# @app.task(name="retrieve_github_url", base=CollectTask)
# def retrieve_github_url(url: str):
#     parts = re.match(r"(?:http[s]*://)*github\.com/([^/]*)/([^/]*)", url).groups()
#     return retrieve_github(*parts)
