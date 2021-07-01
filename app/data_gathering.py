import os
import re
from datetime import datetime as dt
import pandas as pd
import praw
from twitter import Api
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Analyse:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ticker_list = pd.read_csv(self.dir_name + '\\dependencies\\ticker_list.csv')

    # check if a ticker exists in a comment
    def ticker(self, text):
        found_flag = 0
        ticker = ''
        for ticker_name in self.ticker_list['Symbol']:
            ticker_pattern = re.compile(r'\b%s\b' % ticker_name)
            if len(ticker_pattern.findall(str(text))) > 0:
                found_flag = 1
                ticker = ticker_name
                return ticker
        if found_flag == 0:
            ticker = ''
            return ticker

    def update_comments(self, element):
        element["ticker"] = self.ticker(element["text"])
        element["sentiment"] = self.sia.polarity_scores(element["text"])['compound']
        return element


class Reddit:
    def __init__(self, client_id, client_secret, username, password, user_agent):
        self.connection = praw.Reddit(client_id=client_id, client_secret=client_secret, username=username,
                                      password=password, user_agent=user_agent)
        self.comment_bundle = []

    def stream_reddit(self, reddit_stream):
        reddit_stream = self.connection.subreddit(reddit_stream)
        for comment in reddit_stream.stream.comments(skip_existing=True):
            comment_dict = {
                'datetime': dt.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'sub_reddit': str(comment.subreddit),
                'platform': "Reddit",
                'text': comment.body
            }
            self.comment_bundle.append(comment_dict)
            print(comment_dict)


class Twitter:
    def __init__(self, con_key, con_secret, access_key, access_secret):
        self.connection = Api(consumer_key=con_key, consumer_secret=con_secret,
                              access_token_key=access_key, access_token_secret=access_secret)
        self.comment_bundle = []

    def stream_twitter(self, twitter_stream, lang="en"):
        for line in self.connection.GetStreamFilter(track=twitter_stream, languages=lang, filter_level="low"):
            if 'extended_tweet' in line:
                text = line["extended_tweet"]["full_text"]

            if 'retweeted_status' in line:
                text = line["retweeted_status"]["text"]

            else:
                text = line['text']

            text = re.sub(r"\S*https?:\S*", "", text)
            text = text.strip()
            text.replace("\\n", " . ")

            comment_dict = {
                'datetime': dt.utcfromtimestamp(int(line["timestamp_ms"][0:-3])).strftime('%Y-%m-%d %H:%M:%S'),
                'text': text,
                'platform': "Twitter"
            }
            self.comment_bundle.append(comment_dict)
            print(comment_dict)
