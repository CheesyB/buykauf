#!/usr/bin/env bash

docker run --rm -d \
  --name buykauf \
  --env TOKEN=$TOKEN \
  --mount source=buykauf_db,target=$(pwd)/db \
  buykauf:latest
