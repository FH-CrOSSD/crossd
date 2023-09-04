
#!/bin/bash

buildah from --name collector-drone python:3.11-alpine
buildah config --workingdir /home/collector-drone collector-drone
buildah copy collector-drone . .
buildah run collector-drone pip3 install -r requirements.txt
buildah run collector-drone pip3 install -e MDI_Thesis
buildah config --user 1337:1337 collector-drone
buildah config --entrypoint '["python3","test.py"]' collector-drone
buildah config --cmd "" collector-drone
buildah commit collector-drone collector-drone
buildah push --tls-verify=false collector-drone localhost:32000/collector-drone