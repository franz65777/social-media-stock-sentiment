from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import re
import praw
import pandas as pd
import asyncio
import twitter
import threading


class Analyse:
    """
    This Class analyses the comments after they have been find (reddit and twitter classes).
    The Reddit and Twitter classes send their data to this class to get processed.
    """
    def __init__(self):
        self.data_bundle = []
        self.sia = SentimentIntensityAnalyzer()
        self.dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ticker_list = pd.read_csv(self.dir_name + '\\dependencies\\ticker_list.csv')

    def add_to_queue(self, data_packet):
        self.data_bundle.append(data_packet)
        return self.data_bundle


class Delivery:
    """
    This class add data via the users settings e.g. to a database or csv or another file formate
    """
    def __init__(self):
        pass

    def to_csv(self):
        pass

    def to_db(self):
        pass

    def to_excel(self):
        pass


class Reddit:
    """
    This class revives data stream from reddit
    TODO: check if it can understand polls
    TODO: view posts and add it as well
    TODO:
    """
    def __init__(self, client_id, client_secret, username, password, user_agent):
        self.connection = praw.Reddit(client_id=client_id, client_secret=client_secret, username=username,
                                      password=password, user_agent=user_agent)

    def results(self, reddit_stream):
        reddit_stream = self.connection.subreddit(reddit_stream)

        for comment in reddit_stream.stream.comments(skip_existing=True):
            print(comment.subreddit)


class Twitter:
    """
    This class revives data stream from twitter
    TODO: check if it can understand polls
    TODO: view posts and add it as well as replies
    TODO: get api
    """
    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        self.connection = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                                      access_token_key=access_token_key, access_token_secret=access_token_secret)

    def results(self, data_wanted):
        pass
