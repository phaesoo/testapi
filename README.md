# TestAPI

[![Build Status](https://www.travis-ci.com/phaesoo/testapi.svg?branch=main)](https://www.travis-ci.com/phaesoo/testapi)

TestAPI is a web application server for the purpose of testing and prototyping.
It is implemented based on the flask web framework.

## Run with docker container
```bash
$ docker build --force-rm -t phaesoo/testapi .  # build
$ docker run --rm -it --name testapi -p 80:8080 phaesoo/testapi  # run
```

## Run with kubernetes
```bash
$ kustomize apply -k k8s
```

## Run test
```bash
$ make test
```