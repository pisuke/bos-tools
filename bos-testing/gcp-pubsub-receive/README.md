# gcp-pubsub-receive

This command line program allows to see the message stream of a specific devices or class of devices with a common abbreviation.

## Installation

`python3 -m pip install -r requirements.txt`

## Usage

```
$ gcloud auth login
$ gcloud auth application-default login
$ ./gcp-pubsub-receive.py -h
                                    _               _     
  __ _  ___ _ __        _ __  _   _| |__  ___ _   _| |__  
 / _` |/ __| '_ \ _____| '_ \| | | | '_ \/ __| | | | '_ \ 
| (_| | (__| |_) |_____| |_) | |_| | |_) \__ \ |_| | |_) |
 \__, |\___| .__/      | .__/ \__,_|_.__/|___/\__,_|_.__/ 
 |___/     |_|         |_|                                

                   _           
 _ __ ___  ___ ___(_)_   _____ 
| '__/ _ \/ __/ _ \ \ \ / / _ \
| | |  __/ (_|  __/ |\ V /  __/
|_|  \___|\___\___|_| \_/ \___|
                               

usage: gcp-pubsub-receive.py [-h] [-v] [-p PROJECT] [-s SUB] [-d DEVICE] [-t TIMEOUT]

options:
  -h, --help            show this help message and exit
  -v, --verbose         increase the verbosity level
  -p PROJECT, --project PROJECT
                        GCP project id (required)
  -s SUB, --sub SUB     GCP PubSub subscription (required)
  -d DEVICE, --device DEVICE
                        device name or abbreviation (required, for all devices use "all")
  -t TIMEOUT, --timeout TIMEOUT
                        time interval in seconds for which to receive messages (optional, default=60 seconds)
```
