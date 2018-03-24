
import tweepy
import json
import pprint
import requests
import ast
import os
import datetime
from app.sentiment_analysis_gcp import *

a = "w8wTyX6YE1m7jHaLUMc3KBrTD 2n5atA2f3gPGt6eh61MCuH8Q6JiMMvtCUICir6GfzBtrainzXEOPMp6 2554172456-MYpTOd2us50KXr2pKKUGxuFYr5PCBZ7k0TsEgeU nuH3nTUR5bCYeSBjEIUuJF4sKZ9f2TL5r7pSwhAUMj7ae".split()
b = "TTsNCElaiISmdDZzkuKaxNpMG	MzYJ2ZTQDMABFrqEyhqt4x9TOvJTwtx0VrIT8L2tfodglmKAQK	123203658-NT7wMpJGaRErU5WHdUXy9eBZJKtU9Gm0wFjsP5rs	pMr1qEAQNfmK9zEEAGtUKY0eEd6cIvfw9IOiOwjwamflj".split()
c = "dhYBvkx61EsGW4Eeo7ceqssIa	0nINHv4YGqDNfxx0QCAiEw9oTgxHRZ73PdUb5Hbb35UdAdmLbT	1289042472-UCQm2WVUZq7RcNtxIGCQ3Gu6GvQlo8QokPGiWpf	4DQfFRVknDZsb9J3ddS5jUfieimxOfB3Fl3aaB9pmkYXH".split()
d = "Qp9EgWIXWy0GXJ0lwzROLqxhi	3zopoQPw8K0ifWtIO6ZYV7d7SXIQtWhLwmmXpiRKGuscTmdBqn	937763457700528129-UcjSPAOXWfIJBN2HPuwR0oVnwWkM77c fdycfvHndFgGw72JKlY1gpceAxdGjayTh2r8nWcpl3O59".split()
tok = [a,b,c,d]
idx = 3
consumer_key = tok[idx][0]
consumer_secret = tok[idx][1]
access_token = tok[idx][2]
access_token_secret = tok[idx][3]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

def get_user(username):
    return api.get_user(username)

def get_followers(username):
    pages = []
    for page in tweepy.Cursor(api.followers, screen_name=username).pages():
        pages.extend([p._json for p in page] )
    return pages

def get_tweet_stats(url):
    return api.get_status(url.split('/')[-1])._json

# # Get Demographic Distribution 
# def get_demo_dist(username):
#     user = api.get_user(username)
#     ids = []
#     for page in tweepy.Cursor(api.followers_ids, screen_name=username).pages():
#         ids.extend(page)

def get_user_basic(screen_name):
    user = api.get_user(screen_name)
    return {
        "followers": user.followers_count, 
        "following": user.friends_count,
        "description": user.description,
        "name": user.name,
        "image": user.profile_background_image_url
    }

def get_user_following_count(screen_name):
    user = api.get_user(screen_name)
    return user.friends_count

def get_mentions_received_count(username):
    count = 0
    for mentions in tweepy.Cursor(api.search, q='@'+username).items():
        count += 1
    return count

def get_retweets_mentions_sent_count(username):
    RTsent = 0
    RTreceived = 0
    countMentions = 0
    sentiment = [0, 0, 0, 0]
    top_tweets = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=username).items(20):
        score = int((analyze_text(tweet.text) + 100) // 2) # normalize
        if (datetime.datetime.now() - tweet.created_at).days > 60:
            break
        if "retweeted_status" in tweet._json:
            RTsent += 1
        else:
            RTreceived += tweet.retweet_count
            tweet = {
                "text": tweet.text,
                "retweet_count": tweet.retweet_count,
                "favorite_count": tweet.favorite_count,
                "created_at": str(tweet.created_at.utcnow())
            }
            top_tweets.append(tweet)
            sentiment[score//25] += 1
            mentionsSplit = tweet["text"].split()
            countMentions += mentionsSplit.count('@')

    top_tweets = list(sorted(top_tweets, key=lambda x: -x["retweet_count"] - x["favorite_count"]))[:5]
    return {    "retweets_sent": RTsent,
                "mentions_sent": countMentions,
                "retweets_received": RTreceived,
                "sentiment_dist": sentiment,
                "top_tweets": top_tweets
    }

def get_tweets_count(username):
    user = api.get_user(username)
    return user.statuses_count

import os.path
def get_user_stats(username):
    fname = "app/cache/{}_username".format(username)
    if os.path.isfile(fname):
        f = open(fname, "r")
        line = f.read().strip()
        f.close()
        ret = ast.literal_eval(line)
        return ret
    else:
        temp = get_user_basic(username)
        follower_count = temp["followers"]
        following_count = temp["following"]
        name = temp["name"]
        description = temp["description"]
        image = temp["image"]
        mentions_received = get_mentions_received_count(username)
        temp = get_retweets_mentions_sent_count(username)
        mentions_sent = temp["mentions_sent"]
        retweets_sent = temp["retweets_sent"]
        retweets_received = temp["retweets_received"]
        sentiment_dist = temp["sentiment_dist"]
        top_tweets = temp["top_tweets"]
        tweets = get_tweets_count(username)
        weights = list(map(float, open("app/weights.txt", "r").readline()[0].strip().split()))
        ret = [follower_count,following_count,mentions_received,retweets_received,mentions_sent,retweets_sent,tweets,sentiment_dist,top_tweets,name,description,image]
        influence = sum([ret[i] * weights[i] for i in range(len(weights))])
        ret.append(influence)
        f = open(fname, "w")
        f.write(str(ret))
        f.close()
        return ret

def get_follower_stats(username):
    #print("follower_count,following_count,mentions_received,retweets_received,mentions_sent,retweets_sent,posts")
    i = 0
    stats = []
    # cache wokohono
    fname = "app/cache/{}_follower_stats".format(username)
    if os.path.isfile(fname):
        f = open(fname, "r")
        a = f.readlines()
        followers = [ast.literal_eval(i) for i in a]
        f.close()
    else:
        f = open(fname, "w")
        followers = get_followers(username)
        f.write("\n".join([str(f) for f in followers]))
        f.close()
    fname = "app/cache/{}_scrape_data".format(username)
    #if os.path.isfile(fname):
    #    f = open(fname, "r").readlines()
    #    stats = ast.literal_eval(f)
    #else:
    f = open(fname, "w")
    for follower in followers:
        if follower['protected'] == False:
            name = follower["screen_name"]
            stats.append(get_user_stats(name))
            f.write(",".join(map(str,stats[-1])) + "\n")
    f.close()

    stats = list(sorted(stats, key=lambda x : x[-1]))
    return stats

if __name__=="__main__":
    get_follower_stats("BogartsBentelog")