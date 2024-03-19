#!/bin/bash

buildah build --secret id=ghtoken,src=secrets/ghtoken -t bak-rest-drone . 
buildah push --tls-verify=false bak-rest-drone localhost:32000/bak-rest-drone