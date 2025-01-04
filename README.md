# Birdwatcher 🐦

### Birdwatcher is a bot that monitors specific Twitter users' tweets and sends alerts to a Telegram channel whenever a new tweet is posted. This bot uses the Twitter API to fetch the latest tweets from users, and it sends notifications to a specified Telegram channel. It continuously checks for new tweets, making sure you're always up to date on your favorite accounts.

## Features 🚀
* Monitor multiple users: Set up a list of usernames, and Birdwatcher will track tweets from all of them.
* Instant notifications: When a new tweet is posted by any monitored user, Birdwatcher will send a message to your Telegram channel.
* Flexible configuration: Customize which users to monitor, and provide your Telegram chat ID for alerts.
* Automatic updates: The bot automatically fetches the latest tweets every few minutes.

## Prerequisites 🛠️

###  Before running this bot, ensure that you have the following:

* Python 3.7+
* Twitter Developer Account (for access to the Twitter API)
* Telegram Bot (for sending alerts to your channel)

# Installation 🧑‍💻
1. Clone the repository:
```
git clone https://github.com/yourusername/birdwatcher.git
cd birdwatcher
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Create a .env file: Add your environment variables to the .env file as follows:

```
TWITTER_BEARER_TOKEN=<Your_Twitter_Bearer_Token>
TELEGRAM_API_KEY=<Your_Telegram_Bot_API_Key>
TELEGRAM_CHAT_ID=<Your_Telegram_Chat_ID>
USERS_TO_MONITOR=<Comma_separated_list_of_Twitter_usernames>
```

# Configuration ⚙️
In the .env file, make sure to include the following details:
* TWITTER_BEARER_TOKEN: Your Bearer Token obtained from your Twitter Developer account.
* TELEGRAM_API_KEY: The API key for your Telegram bot.
* TELEGRAM_CHAT_ID: The chat ID of the Telegram channel where you want to send the alerts.
* USERS_TO_MONITOR: A comma-separated list of Twitter usernames whose tweets you want to monitor.

# Usage 🚶‍♂️
Run the bot:
```
python birdwatcher.py
```

The bot will continuously monitor the users you’ve specified and send alerts to your Telegram channel whenever a new tweet is posted.

# How it Works 🔍

User Monitoring: The bot fetches the user IDs for the specified usernames.
Tweet Fetching: It then fetches the latest tweets from these users, keeping track of the most recent tweet.
Notification: When a new tweet is found, it sends a message to the Telegram channel with the tweet content.
Repeat: The bot checks for new tweets at regular intervals (every 2 minutes by default).
Error Handling ⚠️
If the rate limit is exceeded by Twitter, the bot will wait for 15 minutes before retrying.
If there’s an issue fetching a user or their tweets, the bot logs the error and continues to monitor other users.


# License 📄
This project is open-source and available under the MIT License