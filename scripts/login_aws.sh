#!/bin/sh
aws --region us-east-1 ecr get-login-password | docker login --username AWS --password-stdin 036881290942.dkr.ecr.us-east-1.amazonaws.com
