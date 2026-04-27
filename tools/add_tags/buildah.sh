#!/bin/bash

buildah build -t add-tags . 
buildah push --tls-verify=false add-tags localhost:32000/add-tags
