import os
import re
from datetime import datetime as dt
import pandas as pd
from praw import Reddit as _reddit_
from twitter import Api as _twitter_
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

    # update the dict with new keys
    def update_comments(self, element):
        element['ticker'] = self.ticker(element['text'])
        element['sentiment'] = self.sia.polarity_scores(element['text'])['compound']
        return element


class Reddit:
    def __init__(self, client_id, client_secret, username, password, user_agent):
        self.connection = _reddit_(client_id=client_id, client_secret=client_secret, username=username,
                                   password=password, user_agent=user_agent)
        self.dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.comment_bundle = []

    # select the subreddits you want to stream in real-time
    def stream(self, subreddits):
        reddit_stream = self.connection.subreddit(subreddits)
        for line in reddit_stream.stream.comments(skip_existing=True):
            comment_dict = {
                'datetime': dt.utcfromtimestamp(line.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'sub_reddit': str(line.subreddit),
                'platform': 'Reddit',
                'text': line.body
            }

            comment_dict = Analyse().update_comments(comment_dict)
            self.comment_bundle.append(comment_dict)
            print(comment_dict)


class Twitter:
    def __init__(self, con_key, con_secret, access_key, access_secret):
        self.connection = _twitter_(consumer_key=con_key, consumer_secret=con_secret,
                                    access_token_key=access_key, access_token_secret=access_secret)
        self.dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.comment_bundle = []

    # select the tweets you want to stream in real-time based on the contents of the tweet
    def stream(self, track_words, language='en'):
        for line in self.connection.GetStreamFilter(track=track_words, languages=language, filter_level='low'):

            # We need to find text in the tweet use cases
            if 'extended_tweet' in line:
                text = line['extended_tweet']['full_text']

            if 'retweeted_status' in line:
                text = line['retweeted_status']['text']

            else:
                text = line['text']

            # This removes any links inside the of the string and cleans the string up
            text = re.sub(r'\S*https?:\S*', '', text)
            text = text.strip()

            comment_dict = {
                'datetime': dt.utcfromtimestamp(int(line['timestamp_ms'][0:-3])).strftime('%Y-%m-%d %H:%M:%S'),
                'text': text,
                'platform': 'Twitter'
            }
            comment_dict = Analyse().update_comments(comment_dict)
            self.comment_bundle.append(comment_dict)
            print(comment_dict)
