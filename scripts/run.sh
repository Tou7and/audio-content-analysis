#!/bin/sh
NAME="vca"
PORT=127.0.0.1:5566
VER="v1"
echo "Start running the service in detached mode on port $PORT"
docker rm -f $NAME || true
docker run -d -p $PORT:5000 --name $NAME tou7and/video-content-analysis:$VER python3 app.py

