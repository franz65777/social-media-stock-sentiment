from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.WSBDatabase import *
import os
import re
import praw
import datetime as dt
import pandas as pd


class WSBBase:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
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
        self.authentication = autho_dict
        self.posts = posts

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

    # fetches data from a specified subreddit using a filter method e.g. recent, hot
    # saves the comments of posts to a dataframe
    def read_submissions(self, mode):
        sub = self.connect.subreddit('wallstreetbets')  # select subreddit
        submission_type = None
        mode = mode.lower()
        comment_list = []

        if mode == "new":
            submission_type = sub.new(limit=self.posts)
        elif mode == "hot":
            submission_type = sub.hot(limit=self.posts)

        elif mode == "rising":
            submission_type = sub.rising(limit=self.posts)

        else:
            exit("Error: 1 - mode type not recognised. Mode Types (new, hot, rising, live)")

        for submission in submission_type:
            submission.comments.replace_more(limit=1)

            for comment in submission.comments.list():
                dictionary_data = {
                    "datetime": dt.datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    "user": str(comment.author),
                    "upvotes": comment.score,
                    "text": comment.body
                }
                comment_list.append(dictionary_data)
        return pd.DataFrame.from_records(data=comment_list)

    def live_submissions(self):
        subreddit = self.connect.subreddit("wallstreetbets")

        for comment in subreddit.stream.comments(skip_existing=True):
            Submission().insert_submission(
                date=dt.datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                user=str(comment.author), upvotes=comment.score, text=comment.body,
                ticker=self.ticker(text=comment.body),
                sentiment=self.sia.polarity_scores(comment.body)['compound'],
                position=""
            )

    def ticker(self, text):
        usedFlag = 0
        ticker = ""
        for ticker_name in self.ticker_list["Symbol"]:
            ticker_pattern = re.compile(r'\b%s\b' % ticker_name)
            if len(ticker_pattern.findall(str(text))) > 0:
                usedFlag = 1
                ticker = ticker_name
                return ticker
        if usedFlag == 0:
            ticker = ""
            return ticker