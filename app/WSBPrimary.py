from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import re
import praw
import pandas as pd
import datetime as dt
import numpy as np

pd.set_option('display.max_rows', 50000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class WSBBase:
    def __init__(self):
        self.dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ticker_list = pd.read_csv(self.dir_name + '\\dependencies\\ticker_list.csv')

        self.master_comments = pd.read_csv(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\dependencies\\log.csv').drop(
            ["Unnamed: 0"], axis=1)

    # saves all comments to a csv document saved in 'logs'
    def debug(self, data=pd.DataFrame()):
        return data.to_csv(self.dir_name + '\\dependencies\\log.csv')


class WallStreetBets(WSBBase):
    def __init__(self, autho_dict, posts):
        super().__init__()
        self.title_list = []
        self.authentication = autho_dict
        self.posts = posts
        self.comment_list = []

    @property
    # creates instance of reddit using authentication from app.WSBAuthentication
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
    def read_submissions(self):
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

    def live_data(self):
        subreddit = self.connect.subreddit("wallstreetbets")
        for comment in subreddit.stream.comments(skip_existing=True):
            print(comment.body)


class DataFrameWSB(WSBBase):
    def __init__(self):
        super().__init__()
        self.data_frame = self.master_comments
        self.sia = SentimentIntensityAnalyzer()

    def __sentiment(self):
        result = []
        for value in self.data_frame["Comments"]:
            score = self.sia.polarity_scores(value)['compound']
            sentiment = score
            result.append(sentiment)

        self.data_frame["Sentiment"] = result

        return self.data_frame

    def __ticker(self):
        tickers = []
        for comment in self.data_frame["Comments"]:
            for ticker_name in self.ticker_list["Symbol"]:
                if len(re.findall(r'\b{}\b'.format(ticker_name), str(comment))) > 0:
                    tickers.append(ticker_name)
                    print(ticker_name)

                else:
                    tickers.append(np.nan)

        self.data_frame["Ticker"] = tickers
        return self.data_frame

    def __positions(self):
        pass

    def data(self):
        self.__ticker()
        self.__sentiment()
        return self.data_frame
