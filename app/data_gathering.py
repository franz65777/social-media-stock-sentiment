from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import re
import praw
import pandas as pd


class SocialMedia:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ticker_list = pd.read_csv(self.dir_name + '\\dependencies\\ticker_list.csv')

    # saves all comments to a csv document saved in 'logs'
    def debug(self, data=pd.DataFrame()):
        return data.to_csv(self.dir_name + '\\dependencies\\log.csv')

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


class Reddit(SocialMedia):
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


class Twitter(SocialMedia):
    def __init__(self, autho_dict, posts):
        super().__init__()
        self.authentication = autho_dict
        self.posts = posts