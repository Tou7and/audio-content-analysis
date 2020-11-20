#!/bin/sh
source ./scripts/common.sh

echo "Building image ${IMAGE_NAME} ${VER} ..."
docker build -f docker/Dockerfile -t "${IMAGE_NAME}:${VER}" .


