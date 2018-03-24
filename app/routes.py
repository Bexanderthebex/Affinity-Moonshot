from flask import request
import json
import requests
from app import app
from app import twitter_functions as tf
from werkzeug import secure_filename
import subprocess
from flask_cors import CORS, cross_origin
from app import db
import json
@app.route("/")
def index():
    return "YEA"

@app.route('/api/get_stats/<username>')
def get_stats(username):
    labels = "follower_count,following_count,mentions_received,retweets_received,mentions_sent,retweets_sent,tweets,sentiment_dist,top_tweets,name,description,image,influence".split(",")
    values = tf.get_user_stats(username)
    mapp = {}
    for i in range(len(labels)):
        mapp[labels[i]] = values[i]
    return json.dumps(mapp)

@app.route('/api/get_follower_stats/<username>')
def get_followers_stats(username):
    result = tf.get_follower_stats(username)
    ret = []
    for r in result:
        labels = "follower_count,following_count,mentions_received,retweets_received,mentions_sent,retweets_sent,tweets,sentiment_dist,top_tweets,name,description,image,influence".split(",")
        values = r
        mapp = {}
        for i in range(len(labels)):
            mapp[labels[i]] = values[i]
        ret.append(mapp)
    return json.dumps(ret)

@app.route('/api/train', methods=["POST"])
def train_data():
    f = request.files['file']
    f.save('app/train.csv')
    subprocess.check_output(['ls','-l']) #all that is technically needed...
    out = subprocess.check_output(['ls','-l'])
    f.write('app/weights.txt')
    return json.dumps(out)

@app.route('/api/add_campaign', methods=["POST"])
@cross_origin()
def add_campaign():
    a = request.get_json()
    c=db.cursor()
    c.execute("""insert into campaign values (NULL, "{}", "{}", {}, "{}", "{}", "{}")""".format(a["name"],a["description"], int(a["age"]),a["gender"],a["network"],a["location"]))
    return json.dumps({"data": list(c.fetchall())})

# @app.route('/api/get_campaigns', methods=["POST"])
# @cross_origin()
# def add_campaign():
#     a = request.get_json()
#     c=db.cursor()
#     c.execute("""select * from campaign""")
#     return json.dumps({"data": list(c.fetchall())})

@app.route('/api/get_tweet/<tweet_id>')
def get_tweet(tweet_id):
    r = tf.get_tweet_stats(tweet_id)
    return json.dumps({"data": r})

@app.route('/api/get_campaigns/<user_id>')
def get_campaign(user_id):
    c=db.cursor()
    c.execute('''select campaign_user.user_id, campaign_user.campaign_id, campaign_user.link, campaign.network, campaign.age, campaign.location, campaign.description, campaign.name from 
        campaign left join campaign_user on campaign.id = campaign_user.campaign_id and campaign_user.user_id = {};'''.format(int(user_id),))
    r = list(c.fetchall())
    return json.dumps({"data": r})

@app.route('/api/set_campaign_url/<campaign_id>', methods=["POST"])
def set_campaign(campaign_id):
    c=db.cursor()
    a = request.form
    c.execute('''update campaign_user set link = "{}" where campaign_id = {};'''.format(a["link"], campaign_id))
    return json.dumps({"data": list(c.fetchall())})