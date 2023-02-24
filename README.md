# 🚨 Aiden Watch 🚨

Aiden Watch is more than just a script. It's a tribute to one of the most badass characters in the gaming world. As a fan of Watch Dogs, I named this script after Aiden, the vigilante hacker who fights against corruption in Chicago. But instead of fighting crime, Aiden Watch helps you fight website downtime. With Aiden Watch, you can monitor your HTTP endpoints and get notified via email, discord, whatsapp, or other channels when something goes wrong. It's like having Aiden's vigilance protecting your website, without all the danger. 

It's not as thrilling as being a vigilante hacker, but it's just as important. With Aiden Watch, you can rest easy knowing your website is being watched over, just like Aiden watches over Chicago.

## 📦 Prerequisites

- Python 3.x
- Requests library

## 🚀 Getting Started

### Prerequisites

Before running the script, make sure you have the following installed:

- Python 3.x
- requests library

### Installation

1. Clone the repository or download the script file.

2. Install the Requests library with the command `pip3 install -r requirements.txt`.

3. Update `endpoints.js` with endpoints you would like to keep an eye.

4. Update `.env` with your credentials, notification channels, and monitored status codes.

## 🛠️ Configuration

- `.env` file contains the following configurations:
    - CHECK_FREQUENCY_SECONDS:          Number of seconds to ping the requests again.
    - NOTIFICATIONS_FREQUENCY_HOURS:    Number of hours to send a notification, so you wil not receive notification everytime you got the same error.
    - MONITOR_STATUS_CODES:             A list of status codes to monitor, such as 404, 500, etc..
    - NOTIFY_CHANNELS:                  Select the channels you want to be notified (email, whatsapp or discord)
    
    Note: The other settings are channel-related, self-explanatory.

- `endpoints`: a list of endpoints to monitor, each with a name, URL, HTTP method, and a list of status codes to monitor.

## 💻 Usage

1. Run the script:
    ```
    python main.py
    ```

2. The script will check the status code of the specified endpoints and send notifications to the configured channels if any monitored status codes are returned.

3. For now, the script just have -v flag that give more detail about endpoints as debug. Type -h to get more info.


## 🌐 Contributing

Contributions to AidenWatch are welcome! To contribute, please fork the repository and submit a pull request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
