# -*- coding=utf-8 -*-
from celery import Celery

app = Celery(
    "collect",
    broker="redis://redis-service:6379/0",
    # backend="arangodb://root:@arangodb-cluster-internal:8529/crossd/task-results",
    broker_connection_retry_on_startup=True,
)

app.conf.task_routes = {
    "retrieve_github": {"queue": "collect", "routing_key": "collect"},
    "retrieve_github_url": {"queue": "collect", "routing_key": "collect"},
    "do_metrics": {"queue": "metric", "routing_key": "metric"},
}

app.send_task(
    "retrieve_github",
    ("laurent22", "joplin")
    # , queue="collect", routing_key="collect"
)
