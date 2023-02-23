import os
import time
import json
import sys
import datetime
import concurrent.futures
from check_status import check_status_code
from dotenv import load_dotenv

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

# Set up the initial time for the last notification
last_notification_time = datetime.datetime.now()

# Define the sleep time between checks (in seconds)
sleep_time = int(os.getenv('SLEEP_TIME'))

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
        time.sleep(sleep_time)
