import tweepy
import os
from dotenv import load_dotenv
import schedule
import time


load_dotenv()

API_KEY = os.getenv("ApiKey")
API_SECRET = os.getenv("ApiSecret")
ACCESS_TOKEN = os.getenv("Acess_token")
ACCESS_SECRET = os.getenv("Acess_token_secret")
BEARER_TOKEN = os.getenv("Bearer_token")

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET,
)

# post a tweet


def post_tweet(text):
    """Post tweet"""

    try:
        response = client.create_tweet(text=text)
        print(f"Tweet posted Successfully!")
        print(f"Tweet Id:{response.data['id']}")
        return response
    except Exception as e:
        print(f"Error posting tweet:", {e})
        return None


# get tweet
def get_tweet(max_result=5):
    """Get my tweets"""
    try:
        # get authenticated user id
        me = client.get_me()
        user_id = me.data.id

        # get tweets
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=max_result,
            tweet_fields=["created_at", "public_metrics"],
        )

        if tweets.data:
            print(f"Your last {len(tweets.data)} tweets:\n")
            for tweet in tweets.data:
                metrics = tweet.public_metrics
                print(f"Tweet: {tweet.text}")
                print(
                    f"❤️Likes:{metrics['Like_count']} | 🔁 Retweets: {metrics['retweet_count']}"
                )
                print(f"Created at: {tweet.created_at}\n")

        else:
            print("no tweet found")

    except Exception as e:
        print("Error with getting tweets", e)


tweets = [
    "You can't find an smart way without working hard first.",
    "aren't you tried of celebrating other people win? when are you clebrating yours?",
    "A man need stronger reason than himself to work on his dream, family, lover or god.",
    "Who am i to judge? when I myself chase perfection",
]

tweet_index = 0


def job():
    global tweet_index
    if tweet_index < len(tweets):
        post_tweet(tweets[tweet_index])
        tweet_index += 1

    else:
        print("All scheduled tweets have been posted")


tweet_time = ["14:00", "16:00", "18:00", "20:00"]

for i, t in enumerate(tweet_time):
    schedule.every().day.at(t).do(lambda text=tweets[i]: post_tweet(text))


print("📅 Tweet scheduler started...")
while True:
    schedule.run_pending()
    time.sleep(60)
