import os
import re
import time
import traceback
from pprint import pp

import nltk
import tweepy
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob as tb

load_dotenv()


def get_config():
    """Get the credentials and configs needed to initialize the tweepy API"""
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
        return api
    except Exception as e:
        print(traceback.print_exc())
        os.exit()


def remove_emoji(text):
    """Remove emojis and symbols"""
    regrex_pattern = re.compile(
        pattern="["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
    return regrex_pattern.sub(r"", text)


def clean_texts(text):
    """Cleans stopwords and unwanted texts

    Parameters
    ----------
    text: text to be cleaned
    """
    # remove urls
    text = re.sub(r"http\S+", "", text)
    text = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ", text)

    text = remove_emoji(text)

    tokens = word_tokenize(text)
    stp_wrd = stopwords.words("english")
    stp_wrd.extend(
        ["join", "di", "io", "thing", "sa", "co", "ph", "us", "rt", "it's", "it"]
    )

    token_list = [token for token in tokens if token not in stp_wrd]
    return token_list


def fetch_user_tweets(api, user_handle: str):
    """Fetches user timeline (tweets and retweets)

    Parameters
    ----------
    api: tweepy api config returned fron the get_config function
    user_handle: twitter username/handle
    """
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
    """Filters tweets by a specific text

    Parameters
    ----------
    word: text that will be used for filtering
    tweet_list: all tweets retrieved
    """
    res = [tweet_ for tweet_ in tweet_list if word.lower() in tweet_.lower()]
    return res


def get_sentiment(filtered_tweets):
    """Calculates the sentiment analysis on the tweets

    Parameters
    ----------
    filtered_tweets: all tweets retrieved
    """
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
    """Runs main logic for sentiment_analysis flow

    Parameters
    ----------
    user_handle: twitter username/handle
    filter_word: text that will be used for filtering
    """
    api = get_config()
    all_tweets = fetch_user_tweets(api, user_handle)

    if filter_word:
        filtered_tweets = filter_by_word(filter_word, all_tweets)
    else:
        filtered_tweets = all_tweets
    cleaned_tweet = []
    for tw in filtered_tweets:
        tw = clean_texts(tw)
        cleaned_tweet.append(" ".join(tw))
    if len(cleaned_tweet) == 0:
        return {
            "data": {"positive": 0, "negative": 0, "neutral": 0},
            "status": "failure",
            "message": f"No response found for {filter_word}",
        }
    res = get_sentiment(cleaned_tweet)
    return res


if __name__ == "__main__":
    nltk.download("stopwords")
    nltk.download("punkt")
    nltk.download("webtext")
    time.sleep(2)
    print()
    print()
    USER_HANDLE = os.getenv("USER_HANDLE")
    pp(main(filter_word="crypto", user_handle=USER_HANDLE))
