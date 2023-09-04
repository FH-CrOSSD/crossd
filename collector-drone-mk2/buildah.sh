#!/bin/bash

buildah build --secret id=ghtoken,src=secrets/ghtoken -t collector-drone-mk2 . 
buildah push --tls-verify=false collector-drone-mk2 localhost:32000/collector-drone-mk2