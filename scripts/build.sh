#!/bin/sh
VER="v1"

docker build -f docker/Dockerfile -t tou7and/video-content-analysis:$VER .

