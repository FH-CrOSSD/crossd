#!/bin/bash

#!/bin/bash
set -e

# Base images
BASE_IMAGE="python:3.13-alpine"
BUILD_IMAGE=$(buildah from $BASE_IMAGE)
FINAL_IMAGE=$(buildah from $BASE_IMAGE)

# Common vars
BUILD_MNT=$(buildah mount $BUILD_IMAGE)
FINAL_MNT=$(buildah mount $FINAL_IMAGE)

# === Stage 1: Build ===
buildah config --workingdir /home/collector-drone $BUILD_IMAGE

# Set ARG
VERSION=2.3.0

# Download and extract source code
#buildah run $BUILD_IMAGE -- sh -c "apk add --no-cache wget unzip"
#buildah run $BUILD_IMAGE -- wget --version
buildah run $BUILD_IMAGE -- sh -c "wget https://github.com/FH-CrOSSD/metrics/archive/refs/tags/v${VERSION}.zip -O - | unzip - && mv metrics-${VERSION} metrics"

# Install PDM and dependencies
buildah run $BUILD_IMAGE -- pip install -U pip setuptools wheel --no-cache-dir
buildah run $BUILD_IMAGE -- pip install pdm --no-cache-dir

# Sync production dependencies
buildah config --workingdir /home/collector-drone/metrics $BUILD_IMAGE
buildah run $BUILD_IMAGE -- mkdir __pypackages__
buildah run $BUILD_IMAGE -- pdm sync --prod --no-editable

# === Stage 2: Final Image ===
buildah run $FINAL_IMAGE -- pip install pdm --no-cache-dir
buildah config --env PYTHONPATH=/project/pkgs $FINAL_IMAGE

# Copy __pypackages__ lib
buildah copy --from $BUILD_IMAGE $FINAL_IMAGE \
  /home/collector-drone/metrics/__pypackages__/3.13/lib /project/pkgs

# Copy executables from __pypackages__/bin
buildah copy --from $BUILD_IMAGE $FINAL_IMAGE \
  /home/collector-drone/metrics/__pypackages__/3.13/bin/. /bin/

# Set up working directory
buildah config --workingdir /home/collector-drone $FINAL_IMAGE

# Copy project source (assumes you are in project root)
buildah copy $FINAL_IMAGE . .

# Install dependencies for final image
buildah run $FINAL_IMAGE -- pdm install
buildah run $FINAL_IMAGE -- pdm cache clear
buildah run $FINAL_IMAGE -- apk add git --no-cache

# Set user and entrypoint
buildah config --user 1337:1337 $FINAL_IMAGE
buildah config --entrypoint '["pdm", "run", "worker"]' $FINAL_IMAGE

buildah config --cmd "" $FINAL_IMAGE
# Commit the image
#buildah commit $FINAL_IMAGE collector-drone:latest
buildah commit --format docker $FINAL_IMAGE collector-drone:latest
buildah push --tls-verify=false collector-drone localhost:32000/collector-drone

# Unmount images
buildah unmount $BUILD_IMAGE
buildah unmount $FINAL_IMAGE


