#!/bin/bash
#
# Source - https://stackoverflow.com/a
# Posted by kometen, modified by community. See post 'Timeline' for change history
# Retrieved 2025-12-03, License - CC BY-SA 4.0

sudo microk8s refresh-certs -e ca.crt
microk8s config > ~/.kube/config

