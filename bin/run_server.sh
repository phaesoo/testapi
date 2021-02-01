#!/bin/bash

# change current directory
MODULE_PATH=$( cd "$(dirname "$0")" ; pwd )
cd ${MODULE_PATH}
cd ..

# build & run
docker build --rm -t testapi .
docker run  -d -p 8080:8080 testapi