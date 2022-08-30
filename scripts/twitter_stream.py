import os
import tweepy
import pymongo
import json
import time
import configparser


parser = configparser.ConfigParser()
parser.read("config.cfg")

CONSUMER_KEY = parser.get("twitter_api_credentials", "CONSUMER_KEY")
CONSUMER_SECRET = parser.get("twitter_api_credentials", "CONSUMER_SECRET")
ACCESS_TOKEN = parser.get("twitter_api_credentials", "ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = parser.get("twitter_api_credentials", "ACCESS_TOKEN_SECRET")


TWITTER_API_TRACK = [parser.get("twitter_api_credentials", "TWITTER_API_TRACK")]
TWITTER_API_LANGUAGE = ["es"]


class TwitterListener(tweepy.Stream):
    def on_connect(self):
        print("Conexión establecida")
        self.connected = True

    def on_status(self, status):
        tuit = status._json
        col.insert_one(tuit)
        print(status.text)

    def on_request_error(self, status):
        if status == 420:
            return False

    def on_connection_error(self):
        print("Conexión fallida")


if __name__ == "__main__":

    client = pymongo.MongoClient("mongodb://admin:password@localhost:27017")
    db = client.tw
    col = db.tweets

    stream = TwitterListener(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    )

    stream.filter(track=TWITTER_API_TRACK, languages=TWITTER_API_LANGUAGE)
