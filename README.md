# S3do

[![Build Status](https://github.com/robvanderleek/s3do/workflows/CICD/badge.svg)](https://github.com/robvanderleek/s3do/actions)
[![DockerHub image pulls](https://img.shields.io/docker/pulls/robvanderleek/s3do)](https://hub.docker.com/repository/docker/robvanderleek/s3do)

A collection of S3 commands.

* [Installation](#installation)
* [Usage](#usage)

# Installation

Pull the image from DockerHub and run the container:

```shell
$ docker run robvanderleek/s3do
``` 

You can also clone this repository, install the dependencies (using virtualenv) 
and run the Python scripts:

```shell
$ git clone https://github.com/robvanderleek/s3do.git
$ cd s3do
$ virtualenv -p python3 venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ ./s3do.py
```

# Usage

## Create an inventory file

From a complete bucket:

```shell
$ docker run -v /Users/rob/.aws:/root/.aws s3do inventory archpi.dabase.com 
```

From a bucket and prefix:

```shell
$ docker run -v /Users/rob/.aws:/root/.aws s3do inventory archpi.dabase.com images
```
