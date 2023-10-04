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
                               

usage: gcp-pubsub-receive.py [-h] [-v] [-p PROJECT] [-s SUB] [-d DEVICE] [-g GATEWAY] [-f FOLDER] [-y TYPE] [-t TIMEOUT]

options:
  -h, --help            show this help message and exit
  -v, --verbose         increase the verbosity level
  -p PROJECT, --project PROJECT
                        GCP project id (required)
  -s SUB, --sub SUB     GCP PubSub subscription (required)
  -d DEVICE, --device DEVICE
                        device name or abbreviation (optional, if not specified shows all devices)
  -g GATEWAY, --gateway GATEWAY
                        filter for the gatewayId attribute (optional)
  -f FOLDER, --folder FOLDER
                        filter for the subFolder attribute (optional, if not specified shows messages in all folders)
  -y TYPE, --type TYPE  filter for the subType attribute (optional)
  -t TIMEOUT, --timeout TIMEOUT
                        time interval in seconds for which to receive messages (optional, default=60 seconds)
```

### Example: get pointset values for a specific device for 1 hour

```
python3 gcp-pubsub-receive.py -p PROJECT_NAME -s SUBSCRIPTION_NAME -d DEVICE_NAME -f pointset -t 3600
```

### Example: get state values for a specific device for 1 hour

```
python3 gcp-pubsub-receive.py -p PROJECT_NAME -s SUBSCRIPTION_NAME -d DEVICE_NAME -f system -y state -t 3600
```