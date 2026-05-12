#!/bin/bash
helm install my-arcadedb ./arcadedb_helm/ -f arcadedb/database.yaml -f arcadedb/image.yaml -f arcadedb/volumes.yaml -f arcadedb/service.yaml
