#!/bin/bash

buildah build -t collector-drone .
buildah push --tls-verify=false collector-drone localhost:32000/collector-drone