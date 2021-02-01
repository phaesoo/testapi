#!/bin/bash

# change current directory
MODULE_PATH=$( cd "$(dirname "$0")" ; pwd )
cd ${MODULE_PATH}
cd ..

# build & run
docker build --rm -t testapi .
docker run  -p 80:8080 testapi