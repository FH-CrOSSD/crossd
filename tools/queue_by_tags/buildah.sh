#!/bin/bash

buildah build -t queue-by-tags . 
buildah push --tls-verify=false queue-by-tags localhost:32000/queue-by-tags
