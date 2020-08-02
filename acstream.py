import tweepy
import time
import json
from credentials import *
import re
import random

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

users = ['1187987797405249536', '892826509622353920', '3101588527']

replies = ['Just incredible!', 'Check this out 😱',
           'T h i s   i s   a w e s o m e  ! ', 'its just like dreaming..', 'Nothing to say']


def reply(raw_data):
    data = json.loads(raw_data)
    # print(data)
    if "delete" not in data and "retweeted_status" not in data and data["in_reply_to_screen_name"] == None and "@owoifybot" not in data["text"] and data["user"]["id_str"] in users:
        try:
            api.update_status(status=random.choice(
                replies) + data["entities"]["url"])
        except tweepy.TweepError as e:
            print(e.reason)


class MaxListener(tweepy.StreamListener):
    def on_data(self, raw_data):
        self.process_data(raw_data)

        return True

    def process_data(self, raw_data):
        reply(raw_data)

    def on_error(self, status_code):
        if status_code == 420:
            print("Ratelimited, waiting 15 minutes.")
            time.sleep(60 * 15)


class MaxStream():
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start(self, id):
        self.stream.filter(follow=id)  # user ID for random account


if __name__ == "__main__":
    listener = MaxListener()
    auth = api.auth
    stream = MaxStream(auth, listener)
    stream.start(users)
