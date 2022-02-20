import os
import traceback

import tweepy
from dotenv import load_dotenv
from textblob import TextBlob as tb

load_dotenv()


def get_config():
    try:
        CONSUMER_KEY = os.getenv("CONSUMER_KEY")
        CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
        ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
        ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

        auth = tweepy.OAuthHandler(
            str(CONSUMER_KEY).strip(), str(CONSUMER_SECRET).strip()
        )
        auth.set_access_token(
            str(ACCESS_TOKEN).strip(), str(ACCESS_TOKEN_SECRET).strip()
        )
        api = tweepy.API(auth)
        print("Config successful")
        return api
    except Exception as e:
        print(traceback.print_exc())
        os.exit()


def fetch_user_tweets(api, user_handle):
    tweet_list = []
    tweets = api.user_timeline(
        screen_name=user_handle,
        # 200 is the maximum allowed count
        count=200,
        include_rts=True,
        # Necessary to keep full_text
        # otherwise only the first 140 words are extracted
        tweet_mode="extended",
    )
    for tweet in tweets:
        tweet_list.append(tweet._json["full_text"])
    return tweet_list


def filter_by_word(word, tweet_list):
    res = [tweet_ for tweet_ in tweet_list if word.lower() in tweet_.lower()]
    return res


def get_sentiment(filtered_tweets):
    sentiments = []
    for tweet_ in filtered_tweets:
        analysis = tb(tweet_)
        polarity = analysis.sentiment.polarity
        output = "Positive"
        if polarity < 0:
            output = "Negative"
        elif 0 <= polarity <= 0.2:
            output = "Neutral"

        sentiments.append(output)

    pos = sentiments.count("Positive")
    neg = sentiments.count("Negative")
    neu = sentiments.count("Neutral")
    total = len(filtered_tweets)
    per_pos = round(float(pos / total * 100), 3)
    per_neg = round(float(neg / total * 100), 3)
    per_neu = round(float(neu / total * 100), 3)
    return {
        "data": {"positive": per_pos, "negative": per_neg, "neutral": per_neu},
        "status": "success",
    }


def main(user_handle, filter_word=""):
    api = get_config()
    all_tweets = fetch_user_tweets(api, user_handle)
    if filter_word:
        filtered_tweets = filter_by_word(filter_word, all_tweets)
    else:
        filtered_tweets = all_tweets
    if len(filtered_tweets) == 0:
        return {
            "data": {"positive": 0, "negative": 0, "neutral": 0},
            "status": "failure",
            "message": f"No response found for {filter_word}",
        }
    res = get_sentiment(filtered_tweets)
    return res


if __name__ == "__main__":
    USER_HANDLE = os.getenv("USER_HANDLE")
    print(main(filter_word="crypto", user_handle=USER_HANDLE))
