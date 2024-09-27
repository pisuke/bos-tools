#!/bin/bash

sudo docker build -t bos-bacnet-server -f Dockerfile.rpi .
sudo docker images
