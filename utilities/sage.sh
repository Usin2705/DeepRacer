#!/usr/bin/env bash

# quick script to auto show the log of sagemaker
# IT DOESN'T ALWAYS WORK. ACCIDENTALLY DELETED THE WORKING VERSION >.<

ID=$(docker ps -aqf "name=sagemaker")
docker logs -f --tail 300 $ID
