#!/usr/bin/python3

import os
import datetime
import requests
import logging
from notifications import send_notification

# Define the channels
notify_channels = os.getenv('NOTIFY_CHANNELS').split(',')

# Define the status codes to monitor
monitor_status_codes_str = os.getenv('MONITOR_STATUS_CODES')
if monitor_status_codes_str is not None:
    monitor_status_codes = [int(code) for code in monitor_status_codes_str.split(',')]
else:
    monitor_status_codes = []

# Define the number of hours between notifications
notification_frequency_hours = int(os.getenv('NOTIFICATIONS_FREQUENCY_HOURS'))

# Define a function to check if notifications should be sent
def should_notify(status_code, current_time, last_notification_time):
    return status_code in monitor_status_codes and \
           (current_time - last_notification_time) >= datetime.timedelta(hours=notification_frequency_hours)

# Define a function to check the status code of an endpoint
def check_status_code(name, endpoint, last_notification_time):
    url, method = endpoint['url'], endpoint['method']
    data = endpoint.get('data', None)
    try:
        response = requests.request(method, url, data=data)
        status_code = response.status_code
        current_time = datetime.datetime.now()
        dt_formatted = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        logging.info(f"[{dt_formatted}] {status_code} - {method} - {url}")
        
        if data is not None:
            logging.debug(f'{data}')

        if status_code in monitor_status_codes and should_notify(status_code, current_time, last_notification_time):
            message = f"{name} endpoint returned {status_code} status code"
            last_notification_time=current_time
            for channel in notify_channels:
                send_notification(channel, message)
            
    except Exception as e:
        logging.error(f"Error: {name} endpoint failed - {e}")

