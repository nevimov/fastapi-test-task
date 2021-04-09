#!/bin/bash

# This script shows local build context that's being sent to the Docker daemon.
# Requires Docker v17.05 or higher.

IMAGE_TAG=temp-build-context

echo "Building a temporary image '$IMAGE_TAG'..."
docker build -t "$IMAGE_TAG" --quiet . -f-<<EOF
FROM busybox
RUN mkdir /ctx
ADD . /ctx/
EOF

echo
echo '**************************** Build context *****************************'
# `docker run` (docker v18.03) separates new lines with <CR> instead of <LF>.
# Using command substitution with the echo command seems to solve the problem.
echo "$(docker run --rm -it $IMAGE_TAG find /ctx -print)" \
    | tail -n +2 | sed "s|^/ctx/||"
echo '************************************************************************'
echo

echo 'Cleaning up...'
docker image rm "$IMAGE_TAG"
