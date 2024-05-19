#!/usr/bin/env python3
"""
  gcp-pubsub-receive.py

  Read data stream for specific devices.

  [Usage] 
  python3 gcp-pubsub-receive.py -p PROJECT_ID -s SUBSCRIPTION_ID [options]
"""

__author__ = "Francesco Anselmo"
__copyright__ = "Copyright 2023"
__credits__ = ["Francesco Anselmo"]
__license__ = "MIT"
__version__ = "0.2"
__maintainer__ = "Francesco Anselmo"
__email__ = "francesco.anselmo@gmail.com"
__status__ = "Dev"

from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import argparse
import json
from tabulate import tabulate
from pyfiglet import *

TARGET_DEVICE_ID = ""
TARGET_GATEWAY_ID = ""
TARGET_SUBFOLDER = ""
TARGET_TYPE = ""
TARGET_POINT_NAME = ""

def print_message(message, pointname):
  body = message.data
  device_id = message.attributes['deviceId']
  gateway_id = message.attributes['gatewayId']
  sub_folder = message.attributes['subFolder']
  type = message.attributes['subType']
  timestamp = json.loads(body)['timestamp']
  
  if pointname != "":
    pointset = json.loads(body)['points']
    try:
      filtered_data = {key: pointset[key] for key in [pointname]}
      point_value = filtered_data[pointname]['present_value']
      print(tabulate([["Timestamp", "Device ID", "Gateway ID", "Subfolder", "Type", "Point name", "Point value"],
                      [timestamp, device_id, gateway_id, sub_folder, type, pointname, point_value]]))
    except:
      pass
  else:
    print(tabulate([["Timestamp", "Device ID", "Gateway ID", "Subfolder", "Type"],
                      [timestamp, device_id, gateway_id, sub_folder, type]]))
    print(message)
    print(body)
    print(70*"-")
    

def message_callback(message: pubsub_v1.subscriber.message.Message) -> None:
    global TARGET_DEVICE_ID, TARGET_GATEWAY_ID, TARGET_SUBFOLDER, TARGET_TYPE, TARGET_POINT_NAME

    device_id = message.attributes['deviceId']
    gateway_id = message.attributes['gatewayId']
    sub_folder = message.attributes['subFolder']
    type = message.attributes['subType']
    
    
    if TARGET_DEVICE_ID in device_id:
      if gateway_id in TARGET_GATEWAY_ID:
        if sub_folder == TARGET_SUBFOLDER and TARGET_SUBFOLDER != "":
          if type == TARGET_TYPE:
            print_message(message, TARGET_POINT_NAME)
        elif TARGET_SUBFOLDER == "" and TARGET_TYPE == "":
          print_message(message, TARGET_POINT_NAME)
      elif TARGET_GATEWAY_ID == "":
        if sub_folder == TARGET_SUBFOLDER and TARGET_SUBFOLDER != "":
          if type == TARGET_TYPE:
            print_message(message, TARGET_POINT_NAME)
        elif TARGET_SUBFOLDER == "" and TARGET_TYPE == "":
          print_message(message, TARGET_POINT_NAME)
    elif TARGET_DEVICE_ID == "":
      if gateway_id in TARGET_GATEWAY_ID:
        if sub_folder == TARGET_SUBFOLDER and TARGET_SUBFOLDER != "":
          if type == TARGET_TYPE:
            print_message(message, TARGET_POINT_NAME)
        elif TARGET_SUBFOLDER == "" and TARGET_TYPE == "":
          print_message(message, TARGET_POINT_NAME)
      elif TARGET_GATEWAY_ID == "":
        if sub_folder == TARGET_SUBFOLDER and TARGET_SUBFOLDER != "":
          if type == TARGET_TYPE:
            print_message(message, TARGET_POINT_NAME)
        elif TARGET_SUBFOLDER == "" and TARGET_TYPE == "":
          print_message(message, TARGET_POINT_NAME)
    message.ack()


def show_title():
  """Show the program title
  """
  f1 = Figlet(font='standard')
  print(f1.renderText('gcp-pubsub'))
  print(f1.renderText('receive'))

def main():
  global TARGET_DEVICE_ID, TARGET_GATEWAY_ID, TARGET_SUBFOLDER, TARGET_TYPE, TARGET_POINT_NAME
      
  show_title()

  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-v", "--verbose", action="store_true", default=False, help="increase the verbosity level")  
  parser.add_argument("-p", "--project", default="", help="GCP project id (required)")
  parser.add_argument("-s", "--sub", default="", help="GCP PubSub subscription (required)")
  parser.add_argument("-d", "--device",  default="", help="device name or abbreviation (optional, if not specified shows all devices)")
  parser.add_argument("-g", "--gateway", default="", help="filter for the gatewayId attribute (optional)")
  parser.add_argument("-f", "--folder", default="", help="filter for the subFolder attribute (optional, if not specified shows messages in all folders)")
  parser.add_argument("-y", "--type", default="", help="filter for the subType attribute (optional)")
  parser.add_argument("-n", "--pointname", default="", help="filter for the point name (optional)")
  parser.add_argument("-t", "--timeout", default="60", help="time interval in seconds for which to receive messages (optional, default=60 seconds)")

  args = parser.parse_args()

  if args.verbose:
    print("program arguments:")
    print(args)


  if args.project!="" and args.sub!="":
    PROJECT_ID = args.project
    SUBSCRIPTION_ID = args.sub
    TARGET_DEVICE_ID = args.device
    TARGET_GATEWAY_ID = args.gateway
    TARGET_SUBFOLDER = args.folder
    TARGET_TYPE = args.type
    TARGET_POINT_NAME = args.pointname

    # Number of seconds the subscriber should listen for messages
    TIMEOUT = int(args.timeout)

    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_id}`
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=message_callback)
    if TARGET_DEVICE_ID == "":
      print(f"Listening for messages from all devices on {subscription_path}\n")
    else:
      print(f"Listening for messages from {TARGET_DEVICE_ID} on {subscription_path}\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=TIMEOUT)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.

  else:
    print("Please run ""%s -h"" to see the program options" % sys.argv[0])

if __name__ == "__main__":
  main()
