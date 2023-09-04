#!/bin/bash

buildah build --secret id=ghtoken,src=secrets/ghtoken -t metric-drone . 
buildah push --tls-verify=false metric-drone localhost:32000/metric-drone