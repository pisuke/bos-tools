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
from pyfiglet import *

TARGET_DEVICE_ID = ""
TARGET_GATEWAY_ID = ""
TARGET_SUBFOLDER = ""
TARGET_TYPE = ""

def print_message(message):
  print(f"\nReceived {message}.")
  body = message.data
  print(body)
  

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    global TARGET_DEVICE_ID, TARGET_GATEWAY_ID, TARGET_SUBFOLDER, TARGET_TYPE

    device_id = message.attributes['deviceId']
    gateway_id = message.attributes['gatewayId']
    sub_folder = message.attributes['subFolder']
    type = message.attributes['subType']
    
    if TARGET_DEVICE_ID in device_id:
      if gateway_id in TARGET_GATEWAY_ID:
        if sub_folder == TARGET_SUBFOLDER and TARGET_SUBFOLDER != "":
          if type == TARGET_TYPE:
            print_message(message)
        elif TARGET_SUBFOLDER == "" and TARGET_TYPE == "":
          print_message(message)
      elif TARGET_GATEWAY_ID == "":
        if sub_folder == TARGET_SUBFOLDER and TARGET_SUBFOLDER != "":
          if type == TARGET_TYPE:
            print_message(message)
        elif TARGET_SUBFOLDER == "" and TARGET_TYPE == "":
          print_message(message)
    elif TARGET_DEVICE_ID=="":
      if gateway_id in TARGET_GATEWAY_ID:
        if sub_folder == TARGET_SUBFOLDER and TARGET_SUBFOLDER != "":
          if type == TARGET_TYPE:
            print_message(message)
        elif TARGET_SUBFOLDER == "" and TARGET_TYPE == "":
          print_message(message)
      elif TARGET_GATEWAY_ID == "":
        if sub_folder == TARGET_SUBFOLDER and TARGET_SUBFOLDER != "":
          if type == TARGET_TYPE:
            print_message(message)
        elif TARGET_SUBFOLDER == "" and TARGET_TYPE == "":
          print_message(message)
    message.ack()


def show_title():
  """Show the program title
  """
  f1 = Figlet(font='standard')
  print(f1.renderText('gcp-pubsub'))
  print(f1.renderText('receive'))

def main():
  global TARGET_DEVICE_ID, TARGET_GATEWAY_ID, TARGET_SUBFOLDER, TARGET_TYPE
      
  show_title()

  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-v", "--verbose", action="store_true", default=False, help="increase the verbosity level")  
  parser.add_argument("-p","--project", default="", help="GCP project id (required)")
  parser.add_argument("-s","--sub", default="", help="GCP PubSub subscription (required)")
  parser.add_argument("-d", "--device",  default="", help="device name or abbreviation (optional, if not specified shows all devices)")
  parser.add_argument("-g", "--gateway", default="", help="filter for the gatewayId attribute (optional)")
  parser.add_argument("-f", "--folder", default="", help="filter for the subFolder attribute (optional, if not specified shows messages in all folders)")
  parser.add_argument("-y", "--type", default="", help="filter for the subType attribute (optional)")
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

    # Number of seconds the subscriber should listen for messages
    TIMEOUT = int(args.timeout)

    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_id}`
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages from {TARGET_DEVICE_ID} on {subscription_path}.\n")

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
