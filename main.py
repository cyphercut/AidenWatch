#!/usr/bin/python3

import os
import time
import json
import sys
import datetime
import argparse
import logging
import concurrent.futures
from dotenv import load_dotenv
from check_status import check_status_code

def main():
    # Load all variables from .env file
    load_dotenv()

    # Load endpoints from external file
    try:
        with open('endpoints.json') as f:
            endpoints = json.load(f)
    except FileNotFoundError:
        print("Error: endpoints.json file not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: endpoints.json file is not in the correct format.")
        sys.exit(1)

    # Configure argument parser
    parser = argparse.ArgumentParser(description='Monitor endpoint status codes and notify if necessary.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    args = parser.parse_args()

    # Configure logging
    if args.verbose:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    # Set up the initial time for the last notification
    last_notification_time = datetime.datetime.now()

    # Define the sleep time between checks (in seconds)
    check_frequency_seconds = int(os.getenv('CHECK_FREQUENCY_SECONDS'))

    # Use a ThreadPoolExecutor to execute the requests to each endpoint in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            futures = {executor.submit(check_status_code, name, endpoint, last_notification_time): (name, endpoint) for name, endpoint in endpoints.items()}
            # Wait for all futures to complete, even if some raise exceptions
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"error: {e}")
            # Sleep before checking the endpoints again
            time.sleep(check_frequency_seconds)


if __name__ == '__main__':
    main()
