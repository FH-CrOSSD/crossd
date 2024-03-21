#!/bin/bash

buildah build -t add-task . 
buildah push --tls-verify=false add-task localhost:32000/add-task
