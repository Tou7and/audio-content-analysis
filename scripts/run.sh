#!/bin/sh
set -eo pipefail

source ./scripts/common.sh

echo "Start running the service in detached mode on port $PORT, with container name ${CONTAINER_NAME}"
docker rm -f $CONTAINER_NAME || true
docker run -d -p $PORT:5000 --name $CONTAINER_NAME $LOCAL_IMAGE python3 app.py
