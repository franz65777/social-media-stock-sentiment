import os
import praw
import pandas as pd
import datetime as dt


class DataParser:
    def __init__(self, autho_dict, posts):
        self.authentication = autho_dict
        self.posts = posts
        self.comment_list = []
        self.title_list = []
        self.ticker_list = pd.read_csv(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\dependencies\\ticker_list.csv")

    @property
    # creates instance of reddit using authenticaton from app.WSBAuthentication
    def connect(self):
        return praw.Reddit(
            client_id=self.authentication.get("app_id"),
            client_secret=self.authentication.get("secret"),
            username=self.authentication.get("username"),
            password=self.authentication.get("password"),
            user_agent=self.authentication.get("user_agent")
        )

    @property
    # fetches data from a specified subreddit using a filter method e.g. recent, hot
    def fetch_data(self):
        sub = self.connect.subreddit("wallstreetbets")  # select subreddit
        new_wsb = sub.hot(limit=self.posts)  # sorts by new and pulls the last 1000 posts of r/wsb
        return new_wsb

    @property
    # saves the comments of posts to a dataframe
    def break_up_data(self):
        for submission in self.fetch_data:
            self.title_list.append(submission.title)  # creates list of post subjects, elements strings
            submission.comments.replace_more(limit=1)

            for comment in submission.comments.list():
                dictionary_data = {comment.body}
                self.comment_list.append(dictionary_data)
        return pd.DataFrame(self.comment_list, columns=['Comments'])

    # saves all comments to a csv document saved in 'logs'
    def debug(self):
        save_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\logs"
        return self.break_up_data.to_excel(save_file + "\\log-{}.xlsx".format(
            dt.datetime.now().strftime("D%Y-%m-%d_T%H.%M.%S")), sheet_name='Log')
