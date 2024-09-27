#!/bin/bash

sudo docker build -t bos-bacnet-server -f Dockerfile.i386 .
sudo docker images
