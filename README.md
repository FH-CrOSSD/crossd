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

The projects needs several secrets (passwords and users) in order to enable the services to interact securely.

The folder `secret_templates` contains all necessary templates.
Copy it with `cp -r secret_templates secrets` and replace all placeholders (`<username>`, `<password>`, `github token`) with the base64 encoded corresponding values. 

You can encode your values with e.g.:
```bash
echo -n "replace-me" | base64 -w0
```

The project need following secrets:

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
<insert image>

### ArangoDB
### Celery Task Queue (+ Redis)
### Flower
### Crawlers
### Metrics
### Frontend



## Known issues and limitations

- This projects was tested with microk8s using a single node cluster
- This project is currently only intended for use with GitHub repositories
- The CPU needs to support AVX as this is a requirement of ArangoDB
- All Kubernetes resources use currently the default namespace

## Acknowledgements

The financial support from Internetstiftung/Netidee is gratefully acknowledged. The mission of Netidee is to support development of open-source tools for more accessible and versatile use of the Internet in Austria.


