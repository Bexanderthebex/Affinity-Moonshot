from flask import request
import json
import requests
from app import app
from app import twitter_functions as tf
from werkzeug import secure_filename
import subprocess
from flask_cors import CORS, cross_origin
import json
@app.route("/")
@cross_origin()
def index():
    return "YEA"

@app.route('/api/get_stats/<username>')
@cross_origin()
def get_stats(username):
    labels = "follower_count,following_count,mentions_received,retweets_received,mentions_sent,retweets_sent,tweets,sentiment_dist,top_tweets,name,description,image,influence".split(",")
    values = tf.get_user_stats(username)
    mapp = {}
    for i in range(len(labels)):
        mapp[labels[i]] = values[i]
    return json.dumps(mapp)

@app.route('/api/get_follower_stats/<username>')
@cross_origin()
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
@cross_origin()
def train_data():
    f = request.files['file']
    f.save('app/train.csv')
    subprocess.check_output(['ls','-l']) #all that is technically needed...
    out = subprocess.check_output(['ls','-l'])
    f.write('app/weights.txt')
    return json.dumps(out)
