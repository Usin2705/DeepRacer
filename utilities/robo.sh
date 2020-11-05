#!/usr/bin/env bash

# quick script to auto show the log of robomaker

ID=$(docker ps -aqf "name=robomaker")
docker logs -f --tail 300 $ID
