#!/usr/bin/env python3
"""
  gcp-pubsub-receive.py

  Read data stream for specific devices.

  [Usage] 
  python3 gcp-pubsub-receive.py -p PROJECT_ID -s SUBSCRIPTION_ID -d TARGET_DEVICE -t TIMEOUT 
"""

__author__ = "Francesco Anselmo"
__copyright__ = "Copyright 2023"
__credits__ = ["Francesco Anselmo"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Francesco Anselmo"
__email__ = "francesco.anselmo@gmail.com"
__status__ = "Dev"

from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import json
import base64
import argparse
from pyfiglet import *

TARGET_DEVICE_ID = ""

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    global TARGET_DEVICE_ID
    #print(message.attributes)
    #print(dir(message.attributes))
    #print(base64.b64decode(message))
    #attributes = json.loads(base64.b64decode(message))['attributes']
    device_id = message.attributes['deviceId']
    #print(device_id)
    if TARGET_DEVICE_ID!="all" and TARGET_DEVICE_ID in device_id:
       print(f"Received {message}.")
       #body = base64.b64decode(message.data)
       body = message.data
       print(body)
    elif TARGET_DEVICE_ID=="all":
       print(f"Received {message}.")
       body = message.data
       print(body)
    message.ack()


def show_title():
  """Show the program title
  """
  f1 = Figlet(font='standard')
  print(f1.renderText('gcp-pubsub'))
  print(f1.renderText('receive'))

def main():
  global TARGET_DEVICE_ID
      
  show_title()

  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-v", "--verbose", action="store_true", default=False, help="increase the verbosity level")  
  parser.add_argument("-p","--project", default="", help="GCP project id (required)")
  parser.add_argument("-s","--sub", default="", help="GCP PubSub subscription (required)")
  parser.add_argument("-d", "--device",  default="", help="device name or abbreviation (required, for all devices use \"all\")")
  parser.add_argument("-t","--timeout", default="60", help="time interval in seconds for which to receive messages (optional, default=60 seconds)")

  args = parser.parse_args()

  if args.verbose:
    print("program arguments:")
    print(args)


  if args.project!="" and args.sub!="" and args.device!="":
    PROJECT_ID = args.project
    SUBSCRIPTION_ID = args.sub
    TARGET_DEVICE_ID = args.device

    # Number of seconds the subscriber should listen for messages
    TIMEOUT = 60.0

    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_id}`
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

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
