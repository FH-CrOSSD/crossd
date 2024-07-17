# CrOSSD
## Project Pages
- [Health Monitor](https://health.crossd.tech)
- [Blog](https://crossd.tech)
- [Documentation](https://fh-crossd.github.io) 

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

### Features

- Different crawlers for retrieving data about repositories and calculating our metrics
- Web UI for presenting calculated metrics for projects
- API endpoints to query the collected projects and metrics (see [here](https://fh-crossd.github.io/components/api/api.html))
- Resource definitions for running components in a Kubernetes cluster
- Setup script for MicroK8s

## Quick Start Guide

- Clone this repository
- Install requirements buildah, microk8s (see [requirements](https://fh-crossd.github.io/installation/requirements.html))
- Create the secrets (see [secrets](https://fh-crossd.github.io/installation/secrets.html))
- Create ingress files if needed (see [ingress](https://fh-crossd.github.io/installation/ingress.html))
- Modify `ORIGIN` env variable in `frontend.yaml` (see [origin](https://fh-crossd.github.io/installation/frontend_origin.html))
- Execute `./setup.sh`

For detailed setup instructions as well as information about the components of our project check out our [documentation](https://fh-crossd.github.io).

## Known issues and limitations

- This project was tested with microk8s using a single node cluster
- This project is currently only intended for use with GitHub repositories
- The CPU needs to support AVX as this is a requirement of ArangoDB
- All Kubernetes resources currently use the default namespace

## Acknowledgements

The financial support from Internetstiftung/Netidee is gratefully acknowledged. The mission of Netidee is to support development of open-source tools for more accessible and versatile use of the Internet in Austria.
