import os
import praw
import re
import pandas as pd
import datetime as dt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import xlrd


class WallStreetBets:
    def __init__(self, autho_dict, posts):
        self.title_list = []
        self.authentication = autho_dict
        self.dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.posts = posts
        self.comment_list = []
        self.ticker_list = pd.read_csv(self.dir_name + '\\dependencies\\ticker_list.csv')

    @property
    # creates instance of reddit using authenticaton from app.WSBAuthentication
    def connect(self):
        return praw.Reddit(
            client_id=self.authentication.get('app_id'),
            client_secret=self.authentication.get('secret'),
            username=self.authentication.get('username'),
            password=self.authentication.get('password'),
            user_agent=self.authentication.get('user_agent')
        )

    @property
    # fetches data from a specified subreddit using a filter method e.g. recent, hot
    # saves the comments of posts to a dataframe
    def read_data(self):
        sub = self.connect.subreddit('wallstreetbets')  # select subreddit
        new_wsb = sub.hot(limit=self.posts)  # sorts by new and pulls the last 1000 posts of r/wsb

        for submission in new_wsb:
            self.title_list.append(submission.title)  # creates list of post subjects, elements strings
            submission.comments.replace_more(limit=1)

            for comment in submission.comments.list():
                dictionary_data = [
                    dt.datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    str(comment.author),
                    comment.score,
                    comment.body
                ]
                self.comment_list.append(dictionary_data)
        return pd.DataFrame(self.comment_list, columns=['Date Created', 'Author', 'Score', 'Comments'])

    # saves all comments to a csv document saved in 'logs'
    def debug(self, data=pd.DataFrame()):
        return data.to_csv(self.dir_name + '\\dependencies\\log.csv')

    # creates a ticker object for each ticker in ticker_list
    def create(self):
        objlist = []
        for ticker in self.ticker_list['Symbol'].unique():
            objlist.append(Ticker(ticker=ticker))
        print(objlist)

        for obj in objlist:
            obj.get_comments()
            obj.get_count()

        final_list = []
        for obj in objlist:
            if obj.count > 0:
                final_list.append(obj)

        print(final_list)

        for obj in final_list:
            obj.analyzer()
            obj.average_sentiment()
            obj.get_positions()

        return final_list


master_comments = list(pd.read_csv(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\dependencies\\log.csv')['Comments'])


class Ticker:
    def __init__(self, ticker):
        self.ticker = ticker
        self.comment_list = 0
        self.comments = []
        self.sentiment = []
        self.sia = SentimentIntensityAnalyzer()
        self.count = 0
        self.avgsent = 0
        self.positions = []

    def get_comments(self):
        for comment in master_comments:
            if len(re.findall(r'\b{}\b'.format(self.ticker), str(comment))) > 0:
                self.comments.append(comment)
        return self.comments

    def get_count(self):
        self.count = len(self.comments)
        return self.count

    def analyzer(self):
        for comment in self.comments:
            score = self.sia.polarity_scores(comment)
            sentiment = score['compound']
            self.sentiment.append(sentiment)

    def average_sentiment(self):
        counter = 0
        sent = 0
        for sentiment in self.sentiment:
            if sentiment != 0:
                sent += sentiment
                counter += 1
        if counter > 0:
            self.avgsent = round(sent / counter, ndigits=2)
        return self.avgsent

    def get_positions(self):
        # positions are in form SPY 300c 11/20
        for comment in self.comments:
            position = re.findall(r'{}\s\d+\w\s\d+\S\d+'.format(self.ticker), comment)
            if position != []:
                self.positions.append(position)
        return self.positions