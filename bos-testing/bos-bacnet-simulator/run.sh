#!/bin/bash

docker run -it -p 47808:47808 --network host --rm --name bos-bacnet-server bos-bacnet-server:latest
