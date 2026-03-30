#!/bin/bash

buildah build --net=host --secret id=ghtoken,src=secrets/ghtoken -t llm-drone . 
buildah push --tls-verify=false llm-drone localhost:32000/llm-drone
