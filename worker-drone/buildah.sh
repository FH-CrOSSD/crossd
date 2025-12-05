#!/bin/bash

buildah build --net=host --secret id=ghtoken,src=secrets/ghtoken -t worker-drone . 
buildah push --tls-verify=false worker-drone localhost:32000/worker-drone
