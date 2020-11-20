#!/bin/sh
set -eo pipefail
source ./scripts/common.sh

docker tag $LOCAL_IMAGE $AWS_IMAGE
docker push $AWS_IMAGE
