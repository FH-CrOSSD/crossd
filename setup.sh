#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root." >&2
    exit 1
fi

SCRIPTPATH=$(dirname "$(realpath "$0")")

addons="registry dns hostpath-storage ingress cert-manager rbac"

for item in $addons; do
    microk8s enable $item
done

mkdir -p secrets
chown root:root secrets -R
chmod o-r-w-x secrets -R

microk8s helm repo add cert-manager https://charts.jetstack.io
microk8s helm repo add stakater https://stakater.github.io/stakater-charts
microk8s helm repo update

microk8s helm install stakater/reloader --generate-name
microk8s helm install trust-manager cert-manager/trust-manager

microk8s kubectl apply -f certificates/clusterIssuer.yaml -f certificates/CAIssuer.yaml -f certificates/CACertificate.yaml
microk8s kubectl apply -f certificates/trustBundle.yaml -f certificates/redisCertificate
microk8s kubectl apply -f certificates/serviceAccount.yaml -f certificates/arangoCARole.yaml -f certificates/roleBinding.yaml -f certificates/updateArangoCA.yaml
sleep 2
microk8s kubectl create secret generic arango-ca --from-literal=ca.crt="$(microk8s kubectl get secret root-secret --namespace=cert-manager -o jsonpath="{.data['ca\.crt']}" | base64 -d)" --from-literal=ca.key="$(microk8s kubectl get secret root-secret --namespace=cert-manager -o jsonpath="{.data['tls\.key']}" | base64 -d)"

microk8s kubectl apply -f arango-setup/arango-crd.yaml
microk8s kubectl apply -f arango-setup/arango-deployment.yaml
microk8s kubectl apply -f arango-setup/arango-storage.yaml
microk8s kubectl apply -f arango-setup/arango-storage-role.yaml
microk8s kubectl apply -f arango-setup/arango-storage-rb.yaml

microk8s kubectl apply -f arango

#cd $SCRIPTPATH/tools/add_task
#sudo ./buildah.sh
#cd $SCRIPTPATH/worker-drone
#sudo ./buildah.sh
#cd $SCRIPTPATH/bak-rest-drone
#sudo ./buildah.sh
#cd $SCRIPTPATH/frontend
#sudo ./buildah.sh
#cd $SCRIPTPATH

microk8s kubectl apply -f secrets
microk8s kubectl create configmap arango-init --from-file arango-init/arango_init.js

microk8s kubectl apply -f .
