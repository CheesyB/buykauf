#!/usr/bin/env bash

docker run --rm -d \
  --name buykauf \
  --env TOKEN=$TOKEN \
  --env CONNECTION=$CONNECTION \
  --env LOGPATH=$LOGPATH \
  --env LOGNAME=$LOGNAME \
  --mount source=db,target=/persistance \
  buykauf:latest
