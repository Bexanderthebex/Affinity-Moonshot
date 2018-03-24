from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
from textblob import TextBlob
# DONT FORGET TO CHANGE THE PATH WHEN DEPLOYING ON LIVE PRODUCTION ENVIRONMENT!
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/key_nlp.json"

# Instantiates a client
client = language.LanguageServiceClient()

# returns score, only determines whether the text is positive or negative
def analyze_text(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity