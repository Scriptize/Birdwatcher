import os
import asyncio
import telegram
import tweepy
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Twitter Bearer Token from environment
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
if not TWITTER_BEARER_TOKEN:
    raise ValueError("Twitter Bearer Token not found in environment variables")

# Get Telegram API Key from environment
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
if not TELEGRAM_API_KEY:
    raise ValueError("Telegram API Key not found in environment variables")

TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
if not TELEGRAM_CHAT_ID:
    raise ValueError("Telegram Chat ID not found in environment variables")

USERS_TO_MONITOR = os.getenv('USERS_TO_MONITOR')
if not USERS_TO_MONITOR:
    raise ValueError("Users to monitor not found in environment variables")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Set up Twitter API
TW_CLIENT = tweepy.Client(TWITTER_BEARER_TOKEN)

# Set up Telegram API
TG_BOT = telegram.Bot(TELEGRAM_API_KEY)

async def send_telegram_message(message: str):
    try:
        await TG_BOT.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except telegram.error.TelegramError as e:
        logger.error(f"Error sending message to Telegram: {e}")


async def check_tweets(user_ids, last_tweet_ids, start_time):
    for user_id in user_ids:
        try:
            response = TW_CLIENT.get_users_tweets(
                id=user_id,
                since_id=last_tweet_ids.get(user_id),
                max_results=5,
                tweet_fields=['id', 'text', 'author_id', 'created_at'],
                expansions=['author_id'],
                start_time=start_time
            )
            new_tweets_found = False
            if response.data:
                for tweet in reversed(response.data):
                    message = f"New tweet posted by user ID {user_id}:\n\n{tweet.text}"
                    await send_telegram_message(message)
                    last_tweet_ids[user_id] = tweet.id
                    new_tweets_found = True
            if new_tweets_found:
                logger.info(f"New tweets found and processed for user ID {user_id} ✅")
            else:
                logger.info(f"No new tweets found for user ID {user_id} ❌")
            logger.info(f"Fetched tweets for user ID {user_id} 🔄")
        except tweepy.TooManyRequests:
            logger.info("Rate limit exceeded. Waiting before retrying... ⏳")
            await asyncio.sleep(900)  # Wait for 15 minutes
        except Exception as e:
            logger.error(f"Error fetching tweets for user ID {user_id}: {e}")
            if isinstance(e, tweepy.TweepyException):
                logger.error(f"Error message: {e}")
                logger.error(f"Error stack: {e.__traceback__}")
                error_response = e.response
                if error_response:
                    logger.error(f"Error response data: {error_response.json()}")
                    logger.error(f"Error response status: {error_response.status_code}")
                    logger.error(f"Error response headers: {error_response.headers}")
                else:
                    logger.error(f"Full error object: {e}")
    return last_tweet_ids

async def main():
    usernames = USERS_TO_MONITOR.split(",")
    user_ids = []
    
    # Get user IDs to monitor
    for username in usernames:
        try:
            user = TW_CLIENT.get_user(username=username.strip())
            if not user.data:
                raise ValueError(f"User not found: {username}")
            user_ids.append(user.data.id)
            logger.info(f"🆔 Fetched user ID for {username}")
        except Exception as e:
            logger.error(f"Error fetching user ID for {username}: {e}")

    # Initialize lastTweetIds with the latest tweet IDs
    last_tweet_ids = {}
    start_time = datetime.isoformat() + "Z"

    for user_id in user_ids:
        try:
            response = TW_CLIENT.get_users_tweets(id=user_id, max_results=5)
            if response.data:
                last_tweet_ids[user_id] = response.data[0].id
                logger.info(f"🔍 Initialized last tweet ID for user ID {user_id}")
            else:
                last_tweet_ids[user_id] = None
                logger.warning(f"⚠️ No initial tweets found for user ID {user_id}")
        except Exception as e:
            logger.error(f"Error fetching initial tweets for user ID {user_id}: {e}")

    logger.info("🚀 Bot is up and running!")

    # Continuous monitoring
    while True:
        await check_tweets(user_ids, last_tweet_ids, start_time)
        logger.info("⏳ Waiting for the next fetch cycle")
        await asyncio.sleep(120)  # Wait for 2 minutes

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
