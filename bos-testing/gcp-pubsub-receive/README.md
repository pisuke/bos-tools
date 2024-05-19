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
                               

usage: gcp-pubsub-receive.py [-h] [-v] [-p PROJECT] [-s SUB] [-d DEVICE] [-g GATEWAY] [-f FOLDER] [-y TYPE] [-n POINTNAME] [-r] [-t TIMEOUT]

optional arguments:
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
  -n POINTNAME, --pointname POINTNAME
                        filter for the point name (optional)
  -r, --regex           filter device or gateway by regex (default is false)
  -t TIMEOUT, --timeout TIMEOUT
                        time interval in seconds for which to receive messages (optional, default=3600 seconds)
```

### Example: get pointset values for any DDC device for 30 minutes 

```
python3 gcp-pubsub-receive.py -p PROJECT_NAME -s SUBSCRIPTION_NAME -d DDC -f pointset -t 1800
```

### Example: get pointset values for a specific device DDC-12 for 1 hour

```
python3 gcp-pubsub-receive.py -p PROJECT_NAME -s SUBSCRIPTION_NAME -d DDC-12$ -r -f pointset -t 3600
```

### Example: get a the point value "temperature_sensor" for a specific device DDC-12 for 1 hour

```
python3 gcp-pubsub-receive.py -p PROJECT_NAME -s SUBSCRIPTION_NAME -d DDC-12$ -r -f pointset -t 3600 -n temperature_sensor
```

### Example: get state values for a specific device DDC-12 for 1 hour

```
python3 gcp-pubsub-receive.py -p PROJECT_NAME -s SUBSCRIPTION_NAME -d DDC-12$ -r -f system -y state -t 3600
```

## Example output

### Output for a single point from different devices

```
% ./gcp-pubsub-receive.py -p PROJECT_NAME -s SUBSCRIPTION_NAME -t 3600 -f pointset -n zone_air_control_temperature_sensor
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


Listening for messages from all devices on projects/PROJECT_NAME/subscriptions/SUBSCRIPTION_NAME

---------------------------  ---------  ----------  ---------  ----  -----------------------------------  -----------
Timestamp                    Device ID  Gateway ID  Subfolder  Type  Point name                           Point value
2024-05-19T20:16:29.125880Z  TRHC-20    DDC-108     pointset         zone_air_control_temperature_sensor  25.11
---------------------------  ---------  ----------  ---------  ----  -----------------------------------  -----------
---------------------------  ---------  ----------  ---------  ----  -----------------------------------  -----------
Timestamp                    Device ID  Gateway ID  Subfolder  Type  Point name                           Point value
2024-05-19T20:16:31.255162Z  TRH-69     DDC-83      pointset         zone_air_control_temperature_sensor  21.0
---------------------------  ---------  ----------  ---------  ----  -----------------------------------  -----------
---------------------------  ---------  ----------  ---------  ----  -----------------------------------  -----------
Timestamp                    Device ID  Gateway ID  Subfolder  Type  Point name                           Point value
2024-05-19T20:16:45.410108Z  TRHC-54    DDC-133     pointset         zone_air_control_temperature_sensor  25.61
---------------------------  ---------  ----------  ---------  ----  -----------------------------------  -----------
```

### Output for all payloadds from a single device

```
% ./gcp-pubsub-receive.py -p PROJECT_NAME -s SUBSCRIPTION_NAME -t 3600 -f pointset -d FCU-2$ -r
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


Listening for messages from FCU-2$ on projects/PROJECT_NAME/subscriptions/SUBSCRIPTION_NAME

---------------------------  ---------  ----------  ---------  ----
Timestamp                    Device ID  Gateway ID  Subfolder  Type
2024-05-19T20:22:58.669342Z  FCU-2      DDC-98      pointset
---------------------------  ---------  ----------  ---------  ----
Message {
  data: b'{"version": "1.4.1", "timestamp": "2024-05-19T20:2...'
  ordering_key: ''
  attributes: {
    "deviceId": "FCU-2",
    "deviceNumId": "2611104595835312",
    "deviceRegistryId": "REGISTRY_NAME",
    "deviceRegistryLocation": "us-central1",
    "gatewayId": "DDC-98",
    "projectId": "PROJECT_NAME",
    "source": "clearblade-iot-core",
    "subFolder": "pointset",
    "subType": ""
  }
}
b'{"version": "1.4.1", "timestamp": "2024-05-19T20:22:58.669342Z", "points": {"cooling_water_valve_percentage_command": {"present_value": 0.0}, "cooling_water_valve_percentage_sensor": {"present_value": 0.0}, "discharge_air_temperature_sensor": {"present_value": 24.27}, "discharge_fan_fault_status": {"present_value": "inactive"}, "discharge_fan_percentage_command": {"present_value": 0.0}, "fabric_protection_status": {"present_value": "inactive"}, "filter_differential_pressure_sensor": {"present_value": 0.24}, "filter_dirty_alarm": {"present_value": "inactive"}, "fire_alarm_status": {"present_value": "active"}, "heating_water_valve_percentage_command": {"present_value": 0.0}, "heating_water_valve_percentage_sensor": {"present_value": 0.0}, "occupancy_status": {"present_value": "inactive"}, "optimum_start_status": {"present_value": "inactive"}, "return_air_cooling_temperature_setpoint": {"present_value": 23.5}, "return_air_heating_temperature_setpoint": {"present_value": 21.5}, "return_air_temperature_alarm": {"present_value": "inactive"}, "return_air_temperature_sensor": {"present_value": 24.04}, "zone_air_temperature_high_alarm": {"present_value": "inactive"}, "zone_air_temperature_low_alarm": {"present_value": "inactive"}}}'
----------------------------------------------------------------------
```