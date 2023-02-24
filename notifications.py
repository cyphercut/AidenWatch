#!/usr/bin/python3

import os
import requests
import logging
from dotenv import load_dotenv

# Load all variables from .env file
load_dotenv()

def send_email_notification(message):
    """
    Sends an email notification with the given message.
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Set up the SMTP server
    email           = os.getenv('EMAIL')
    password        = os.getenv('EMAIL_PASSWORD')
    send_to_email   = os.getenv('SEND_TO_EMAIL')
    smtp_server     = os.getenv('EMAIL_SMTP_SERVER')
    smtp_port       = os.getenv('EMAIL_SMTP_PORT')

    # Set up the email
    subject = 'Endpoint Monitoring Alert'
    msg = MIMEMultipart()
    msg['From']     = email
    msg['To']       = send_to_email
    msg['Subject']  = subject

    msg.attach(MIMEText(message, 'plain'))
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()

    logging.info(f"Email notification sent: {message}")


def send_discord_notification(message):
    """
    Sends a Discord notification with the given message.
    """
    discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    payload = {'content': message}
    headers = {'Content-type': 'application/json'}
    response = requests.post(discord_webhook_url, json=payload, headers=headers)
    if response.status_code == 204:
        logging.info(f"Discord notification sent: {message}")
    else:
        logging.error(f"Error sending Discord notification: {message}. Status code {response.status_code}")


def send_whatsapp_notification(message):
    """
    Sends a WhatsApp notification with the given message.
    """
    from twilio.rest import Client

    twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_whatsapp_from = os.getenv('TWILIO_WHATSAPP_FROM')
    twilio_whatsapp_to = os.getenv('TWILIO_WHATSAPP_TO')
    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages \
                    .create(
                        body=message,
                        from_='whatsapp:' + twilio_whatsapp_from,
                        to='whatsapp:' + twilio_whatsapp_to
                    )

    logging.info(f"WhatsApp notification sent: {message}")

def send_notification(channel, message):
    """
    Sends a notification to the specified channel with the given message.
    """
    if channel == 'email':
        # send email notification
        send_email_notification(message)
    elif channel == 'discord':
        # send Discord notification
        send_discord_notification(message)
    elif channel == 'whatsapp':
        # send WhatsApp notification
        send_whatsapp_notification(message)
    else:
        logging.error(f"Error: Invalid channel {channel}")
        return