#!/bin/bash

# if [ "$(id -u)" -ne 0 ]; then
#     echo "Please run as root." >&2
#     exit 1
# fi

SCRIPTPATH=$(dirname "$(realpath "$0")")

addons="registry ingress ingress-dns"

for item in $addons; do
   minikube addons enable $item
done

mkdir -p secrets
sudo chown root:root secrets -R
chmod o-r-w-x secrets -R

helm repo add cert-manager https://charts.jetstack.io
helm repo add stakater https://stakater.github.io/stakater-charts
helm repo update

helm install stakater/reloader --generate-name
helm install \
             crossd cert-manager/cert-manager \
             --namespace cert-manager \
             --create-namespace \
             --set crds.enabled=true
helm install trust-manager cert-manager/trust-manager

kubectl apply -f certificates/clusterIssuer.yaml -f certificates/CAIssuer.yaml -f certificates/CACertificate.yaml
kubectl apply -f certificates/trustBundle.yaml -f certificates/redisCertificate
kubectl apply -f certificates/serviceAccount.yaml -f certificates/arangoCARole.yaml -f certificates/roleBinding.yaml -f certificates/updateArangoCA.yaml
sleep 2
kubectl create secret generic arango-ca --from-literal=ca.crt="$(kubectl get secret root-secret --namespace=cert-manager -o jsonpath="{.data['ca\.crt']}" | base64 -d)" --from-literal=ca.key="$(kubectl get secret root-secret --namespace=cert-manager -o jsonpath="{.data['tls\.key']}" | base64 -d)"

kubectl apply -f arango-setup/arango-crd.yaml
kubectl apply -f arango-setup/arango-deployment.yaml
kubectl apply -f arango-setup/arango-storage.yaml
kubectl apply -f arango-setup/arango-storage-role.yaml
kubectl apply -f arango-setup/arango-storage-rb.yaml

kubectl apply -f arango

sudo kubectl apply -f secrets
kubectl create configmap arango-init --from-file arango-init/arango_init.js

kubectl apply -f .
