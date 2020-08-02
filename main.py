import tweepy
import logging
import time
import json
import re
import random
import threading
from credentials import *

toFollowData = {}
toFollowData["screen_name"] = []

# reply string list
replyList = ['Thank you for your giveaway!!!', "ty for the giveway", "ty hope i win!", "hope i win!!!!",
             "goodluck everyone, hope i win!", "if i win i'll do nothing lol", "ty bro, gl everyone"]

# user to mention list
userList = ['kaesangp', 'fijighost', 'fairyqtae', 'TheTrueAMG', 'FruitfulFlips', 'Iightningnotify', 'kvmmysxsamusic', 'mickaeIIa_', 'hvangrj', 'izzyvoiceover', 'abhijeet5911', 'Number1DadPG', 'wxvennnn_', 'ShinninpearlYT', 'NinpoeTV', 'GiveawaySquadd', 'cali_ediblez', 'adoreyoufishy', 'lbharrys', 'lilythegrape', 'AlphaPC_CA', 'InstantGamingEN', 'Black28Jackk', 'BonkToken', 'cryptofhm', 'baeinvelvet', 'ImmortalSnipezY', 'iTzFeith', 'appeachiesz', 'imexiujah', 'BlinkersGroup',
            'DreamAIO_', 't3k_io', 'ahiddensociety', 'EveAIO', 'Spectre_AIO', 'KiloSoftware', 'aycdio', 'Winnie1871', 'NRGexclusive', 'westbrookemusic', 'GeorgeAnthonyO1', 'lundquist_marla', 'kefi_ph', 'Dhezsssy', 'GWayneLive', 'eNshittyyyy', 'CryptoMichNL', 'sharm888', 'oneplus', 'UnboxTherapy', 'ShinX14744367', 'ashley20196', 'luckyannie_777', 'osvaldospellman', '_Sofia24', 'GoldQueenie4', 'satyapaljain_86', 'ChiizDotCom', 'SDas03347757', 'SJ_0016', 'ParallaxSystems', 'pierrel50508326']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# dump "to follow" users to .json file every 5 minutes
def dumpdata():
    threading.Timer(60 * 5, dumpdata).start()
    with open('data.json', 'w') as outfile:
        json.dump(toFollowData, outfile)


def process(raw_data):
    data = json.loads(raw_data)
    # print(data)
    if "retweeted_status" in data:
        data = data["retweeted_status"]
    user = data["user"]
    twtId = data["id"]
    randomizer = random.choice(replyList)

    if "extended_tweet" in data:
        content = data["extended_tweet"]["full_text"]
    else:
        content = data["text"]

    # like
    if "like" in content.lower():
        try:
            api.create_favorite(twtId)
        except tweepy.TweepError as e:
            print(e.reason)
    # retweet
    if "retweet" or "🔁" or "♻️" or "rt" in content.lower():
        try:
            api.retweet(twtId)
        except tweepy.TweepError as e:
            print(e.reason)
    # follow user (just appending users to list, following them later to avoid being banned)
    if "follow" or "foll" or "following" in content.lower():
        # append user to "to follow" list
        toFollowData["screen_name"].append(user["screen_name"])
        if "user_mentions" in data["entities"]:
            for i in data["entities"]["user_mentions"]:
                # append user to "to follow" list
                toFollowData["screen_name"].append(i["screen_name"])

    # reply
    def reply():
        # users to mention
        mentions = re.search(r'\d', content).group(0)
        string = ""
        for i in range(mentions):
            string = string + f" @{random.choice(userList)}"
        return string
    if "comment" or "tag" in content.lower():
        try:
            api.update_status(in_reply_to_status_id=twtId, status=f"@" + user["screen_name"] + " " + randomizer +
                              reply())
        except tweepy.TweepError as e:
            print(e.reason)


class MaxListener(tweepy.StreamListener):
    def on_data(self, raw_data):
        self.process_data(raw_data)

        return True

    def process_data(self, raw_data):
        process(raw_data)
        time.sleep(216)

    def on_error(self, status_code):
        if status_code == 420:
            print("Ratelimited, waiting 15 minutes.")
            time.sleep(60 * 15)


class MaxStream():
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(
            auth=auth, listener=listener, tweet_mode="extended")

    def start(self, word):
        self.stream.filter(track=word)  # user ID for random account


if __name__ == "__main__":
    dumpdata()
    listener = MaxListener()
    auth = api.auth
    stream = MaxStream(auth, listener)
    stream.start(['concours', 'giveaway', 'concour'])
