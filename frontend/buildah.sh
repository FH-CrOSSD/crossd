#!/bin/bash

buildah build -t frontend . 
buildah push --tls-verify=false frontend localhost:32000/frontend
