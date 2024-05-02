# Worker Drone

This drone is a worker for our CrOSSD Celery task queue. It utilises our [metrics](https://github.com/FH-CrOSSD/metrics) library.

The `retrieve*` tasks get GitHub repository data and store them in the ArangoDB.
The ``do_metrics` task retrieves the data from the db, calculates the metrics and stores them also in the db.
