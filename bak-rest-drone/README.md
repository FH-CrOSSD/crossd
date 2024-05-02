# Bak Rest Drone

This drone is a worker for our CrOSSD Celery task queue. It utilises a [modified version](https://github.com/FH-CrOSSD/thesis_metrics) of Jacqueline Schmatz's [source code](https://github.com/JacquelineSchmatz/MDI_Thesis) of her master thesis.

The data of a GitHub repository is retrieved, various metrics are calculated and subsequently stored in our Arangodb database.
