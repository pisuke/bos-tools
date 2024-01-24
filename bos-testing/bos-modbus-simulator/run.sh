#!/bin/bash

docker run -it -p 502:502 --network host --rm --name bos-modbus-server bos-modbus-server:latest
