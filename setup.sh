#!/bin/bash

SCRIPTPATH=$(dirname "$(realpath "$0")")

addons="registry dns hostpath-storage ingress cert-manager"

for item in $addons; do
    microk8s enable $item
done

microk8s kubectl apply -f arango-setup/arango-crd.yaml
microk8s kubectl apply -f arango-setup/arango-deployment.yaml
microk8s kubectl apply -f arango-setup/arango-storage.yaml

cd $SCRIPTPATH/worker-drone
sudo ./buildah.sh
cd $SCRIPTPATH/bak-rest-drone
sudo ./buildah.sh
# cd $SCRIPTPATH/frontend
# sudo ./buildah.sh
cd $SCRIPTPATH

# microk8s kubectl apply -f secrets/ghtoken.yaml
# microk8s kubectl apply -f secrets/arango-root-pwd.yaml
# microk8s kubectl apply -f secrets/arango-frontend-pwd.yaml
# microk8s kubectl apply -f secrets/arango-worker-pwd.yaml
microk8s kubectl apply -f secrets
microk8s kubectl create configmap arango-init --from-file arango-init/arango_init.js

microk8s kubectl apply -f .
