#!/bin/sh
set -eo pipefail
source ./scripts/common.sh
echo "Entering ${CONTAINER_NAME} ..."
docker exec -it $CONTAINER_NAME /bin/bash
