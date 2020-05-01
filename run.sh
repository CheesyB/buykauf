#!/usr/bin/env bash

docker run --rm -d \
  --name buykauf \
  --env TOKEN=$TOKEN \
  --mount source=buykauf_db,target=/buykauf/db/buykauf.sqlite3 \
  buykauf:latest
