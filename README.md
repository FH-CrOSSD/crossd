# CrOSSD

## About The Project
The Critical Open-Source Software Database (CrOSSD) is an open-source software (OSS) project
meant to assist a variety of stakeholders to make informed decisions about which OSS projects to
use, assist or support.

By collecting and continuously monitoring a growing catalogue of OSS projects according to a
selection of curated metrics, CrOSSD gives a comprehensive overview of the state of the observed
projects: How stable are they? How often are they updated? How many active contributors are
there? Do they come from different organisations? The answers to these questions (and more)
allow lay users and software developers to decide which projects they want to include in their
own codebase and which projects might benefit from their involvement and assistance as well as
funding agencies or companies to allocate funding or support to critically important OSS
projects in need of help.


## Features

- Different crawlers for retrieving data about repositories and calculating our metrics
- Web UI for presenting calculated metrics for projects
- Resource definitions for running components in a Kubernetes cluster
- Setup script for MicroK8s 

## Installation

### Requirements
Our project needs following requirements:

- Buildah
    - Build Docker images and push them to local registry
- MicroK8s
    - orchestrate the cluster

On Ubuntu you can install requirements as follows:
```bash
apt install buildah
snap install microk8s --classic
```

Microk8s needs the following plugins (enabled inside the setup script):
- registry
- dns 
- hostpath-storage
- ingress
- cert-manager

### Secrets

The project needs several secrets (passwords and users) in order to enable the services to interact securely.

The folder `secret_templates` contains all necessary templates.
Copy it with `cp -r secret_templates secrets` and replace all placeholders (`<username>`, `<password>`, `<github token>`) with the base64 encoded corresponding values. 

You can encode your values with e.g.:
```bash
echo -n "replace-me" | base64 -w0
```

The project needs following secrets:

#### arango-frontend-pwd

This user is utilised by the frontend web application and has only read permissions.

Properties:
- username
- password

#### arango-root-pwd

The super user for the Arango database used to create other users and collections.

Properties:
- username
- password

#### arango-worker-pwd

This user is utilised by the crawlers and has only read/write permissions.

Properties:
- username
- password

#### flower-basic-auth

This secret contains the user and password (HTTP Basic Authentication) in the format `user:password` for the flower web interface for the task queue.

Properties:
- AUTH


#### ghtoken

The GitHub token used by the workers to crawl the data about the repositories.

> The token can be generated github.com via `Settings` - `Developer settings` - `Personal access tokens` - `Tokens (classic)` - `Generate new token` - `Generate new token (classic)`.

The token needs the scopes:
- read:org
- read:user
- repo

Properties:
- GH_TOKEN

#### redis-auth

Used by containers that need to interact with the task queue broker (Redis).

Properties:
- RAUTH

**All** secrets inside the yaml files need to be **base64** encoded.  
**Ensure the file permissions are set accordingly** (although they are also set in the setup script.)   
`setup.sh` sets following permissions:
```bash
chown root:root secrets -R
chmod o-r-w-x secrets -R
```

After being applied (either by `setup.sh` or manually), the secret files can be deleted as they are stored in microk8s.

### Setup

This project contains the setup script `setup.sh`, which performs the necessary steps:

- Enable MicroK8s plugins
- Setup permissions for secrets folder
- Install Kubernetes plugins `cert-manager` and `trust-manager`
- Apply Kubernetes resources for generating self-signed certificates (used for internal TLS)
- Set up Arango Kubernetes resources
- Build necessary container images
- Apply secrets
- Create all other Pods, Deployments, Services, etc.
    - Arango database
    - Redis
    - Workers
    - Frontend
    - Flower

You need to:
- create the secrets (see [secrets](#secrets))
- create ingress files if needed (see [ingress](#ingress))
- execute `./setup.sh`

### Ingress

Per default all Kubernetes services are can only be used inside the cluster. In order to be able to access the web interfaces from the Internet, we have to make them available via Ingress. 
Our Ingress resources redirect incoming HTTPS traffic to the corresponding pods (determined by domain main) and automatically retrieve the [Let's Encrypt](https://letsencrypt.org/de/) certificates for the TLS connection.

The folder `ingress_templates` contains all necessary templates.
Copy it with `cp -r ingress_templates ingress` and replace all placeholders (`<domain>`, `<email>`) with the according values.

> The configuration of the templates uses different domain names for each service. Therefore, you should register different subdomains. 

### Adding tasks

Adding tasks (repositories to scan) works currently via Kubernetes [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) or [CronJobs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/).

`add_task_job.yaml` defines an example of such a Kubernetes job.
It uses to tool located in `tools/add_task` to interact with the task queue and the ArangoDB. As the secure connection requires the Kubernetes secrets and the self-signed TLS certificates, we build an image for a pod that can in turn be used by the Kubernetes Job.

`tools/add_task/add_task.py` can be used as follows:

```txt
usage: add_task.py [-h] [--only {bak,metric}] [--user USER] [--password PASSWORD] [-t TAG] owner/name [owner/name ...]

Add a repository to the queue

positional arguments:
  owner/name           owner of the repository

options:
  -h, --help           show this help message and exit
  --only {bak,metric}  limit execution to a single task
  --user USER          arangodb username
  --password PASSWORD  arangodb password
  -t TAG, --tag TAG    Set a tag for the scan
```

## Components
![cluster](https://github.com/FH-CrOSSD/crossd/assets/20456596/3b1e8458-9dc6-465e-a7bb-8be67de3dfcd)

Our project uses [MicroK8s](https://microk8s.io/) and in turn various components which are realised as Kubernetes Pods, Deployments, etc. 

Pod can interact with each other only via defined interfaces (so-called Services) and use TLS to encrypt the traffic. Specifically, connections to ArangoDB and Redis are encrypted via TLS using self-signed certificates created with [cert-manager](https://cert-manager.io/).

> ArangoDB creates self-signed certificates for the agents, coordinators and db-servers. ArangoDB handles issuing the certificates itself and is therefore provided with the CA certificate and key from cert-manager.

The containers establishing a connection to ArangoDB or Redis are provided with the CA certificate using trust bundles of [trust-manager](https://cert-manager.io/docs/trust/trust-manager/).


### ArangoDB
[ArangoDB](https://arangodb.com/) is used as a persistent storage for data such as repository information and calculated metrics. We utilise the [ArangoDB Kubernetes Operator](https://arangodb.github.io/kube-arangodb/docs/using-the-operator) for deploying a database cluster.

Collections inside the `crossd` database:
- task_results
  - Stores Celery task results, statuses, errors, ...

- scans
  - Stores information about the scans such as tasks for the repository, tags and connects other documents via the scan id
- projects
  - Contains owner/name of all scanned projects and the corresponding scan ids
- repositories
  - Stores information about repositories collected by c-drone
- metrics
  - Stores results of calculated metrics provided by m-drone
- bak_repos
  - Stores information about repositories collected by bak-rest-drone
- bak_metrics
  - Stores results of calculated metrics provided by bak-rest-drone

Secrets:
- arango-frontend-pwd
- arango-worker-pwd
- arango-root-pwd

Services:
- arango-cluster-internal:8529 (internal)
- arango-cluster-exposed:30529 (optional, external, dev)

Ingress:
- arangodb-ingress:443 (optional, external)

Interacting Components:
- Frontend
- Add Task Job
- m-drone
- c-drone
- bak-rest-drone
- Arango Init Job

### Redis (Celery Task Queue)
[Redis](https://redis.io/) acts as the broker for our [Celery Task Queue](https://docs.celeryq.dev/en/stable/#). It stores and distributes the tasks for our workers.

Secrets:
- redis-auth

Services:
- redis-service:6379 (internal)

Interacting Components:
- Flower
- Add Task Job
- m-drone
- c-drone
- bak-rest-drone

> We did not provide a (development) external service for Redis, as we deemed it not necessary. If you need to inspect the Redis database, get into the pod, establish a TLS connection and authenticate to Redis.
```bash
# connect into pod
microk8s kubectl exec -it <pod name> -- sh
# connect to redis
redis-cli --tls --cacert /tls/ca.crt
# authenticate inside redis
127.0.0.1:6379> auth <password in redis-auth>
```

### Flower
[Flower](https://flower.readthedocs.io/en/latest/) is used to monitor our Celery workers and tasks. It uses HTTP basic authentication.

Secrets:
- flower-basic-auth

Services:
- flower-service:5555 (internal)
- flower-service-exposed:30555 (optional, external, dev)

Ingress:
- flower-ingress:443 (optional, external)

Interacting Components:
- Redis

### Crawlers & Metrics

These pods retrieve the necessary information about repositories and calculate our [defined metrics](https://health.crossd.tech/doc) for assessing the health of OSS projects. 

Secrets:
- arango-worker-pwd
- redis-auth
- ghtoken

Interacting Components:
- Redis
- ArangoDB

#### c-drone

A Python [Celery](https://docs.celeryq.dev/en/stable/#) worker that queries GitHub mostly via GraphQL, but also via REST API and crawls the github.com repository pages.

Stores the results in the `repositories` collection in ArangoDB and calls the subsequent task for calculating the metrics processed by m-drone.

#### m-drone

A Python [Celery](https://docs.celeryq.dev/en/stable/#) worker that receives the results from c-drone and calculates metrics.

Stores the results in the `metrics` collection in ArangoDB.

#### bak-rest-drone

A Python [Celery](https://docs.celeryq.dev/en/stable/#) worker that queries GitHub mostly REST API, but also crawls the github.com repository pages.

Stores the data about the repositories in the `bak_repos` and the calculated metrics in the `bak_metrics` collection in ArangoDB.

We mostly use the [source code](https://github.com/JacquelineSchmatz/MDI_Thesis) developed by Jacqueline Schmatz for her master thesis (with some modifications). The metrics Jacqueline Schmatz chose are listed [here](https://health.crossd.tech/doc). 

### Frontend

Our web interface uses [Svelte](https://svelte.dev/) and [Svelte Kit](https://kit.svelte.dev/) and provides access to the metrics of OSS projects. It also contains a list of the metrics.

Our public instance is available [here](https://health.crossd.tech).

Secrets:
- arango-frontend-pwd

Services:
- frontend-service:3000 (internal)
- frontend-service-exposed:30380 (optional, external, dev)

Ingress:
- frontend-ingress:443 (optional, external)

Interacting Components:
- ArangoDB

### Add Task Job

[Kubernetes Job](https://kubernetes.io/docs/concepts/workloads/controllers/job/) for adding tasks to our Celery task queue as well as creating `scans` and `projects` entries in ArangoDB.

> We decided to use jobs and therefore separate pods and container images for adding tasks, because we need the certificates for the TLS connections to Redis and ArangoDB (stored inside Kubernetes secrets) and also users and passwords (also stored in Kubernetes secrets). 

> Additionally, we did not want to require NodePort services (opening the ports on the node) as this cannot be limited to localhost.

> Connecting to ClusterIP services (internal) would work, but the IPs are dynamic and we did not want to require changes to the DNS resolver on the host.

Our example `add_task_job.yaml` uses repositories owner/name arguments provided inside the yaml file, but they could also be provided e.g. via a Kubernetes [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/).

Secrets:
- arango-worker-pwd
- redis-auth

Interacting Components:
- ArangoDB
- Redis

### Arango Init Job
This [Job](https://kubernetes.io/docs/concepts/workloads/controllers/job/) waits for ArangoDB to be up and running and runs the script `arango-init/arango_init.js`, which creates the `crossd` database, all necessary collections and additional users for the frontend (readonly) and the workers (read/write).

The script `arango-init/arango_init.js` is mounted as a [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/).

Secrets:
- arango-root-pwd
- arango-worker-pwd
- arango-frontend-pwd

Interacting Components:
- ArangoDB

### External Services

All external services (Kubernetes type [NodePort](https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport)) are optional and should only be used in development environment. They open up ports on the node, which can be used to connect to the service from outside the cluster.

We defined external service for:
- ArangoDB
  - arangodb-cluster-exposed:30529
- Frontend
  - frontend-service-exposed:30380
- Flower
  - flower-service-exposed:30555

### Ingress

[Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) acts a reverse proxy and load balancer and provides access to service from the outside. It is also able to terminate TLS connections and request Let's Encrypt certificates. As we use MicroK8s `ingress` plugin, `nginx` acts as our [Ingress Controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/).

The ClusterIssuer `lets-encrypt` retrieves the Let's Encrypt certificates for our cluster. It is optional and the template is located at `ingress_templates/cluster-issuer.yaml`.

We defined templates for ingress endpoints for:
- ArangoDB
  - `ingress_templates/arangodb-ingress.yaml`
- Frontend
  - `ingress_templates/frontend-ingress.yaml`
- Flower
  - `ingress_templates/flower-ingress.yaml`

> All ingress endpoints use TCP port 443 for providing HTTPS connections.

## Known issues and limitations

- This project was tested with microk8s using a single node cluster
- This project is currently only intended for use with GitHub repositories
- The CPU needs to support AVX as this is a requirement of ArangoDB
- All Kubernetes resources currently use the default namespace

## Acknowledgements

The financial support from Internetstiftung/Netidee is gratefully acknowledged. The mission of Netidee is to support development of open-source tools for more accessible and versatile use of the Internet in Austria.




