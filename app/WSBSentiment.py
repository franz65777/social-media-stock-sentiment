from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import os
import praw
import pandas as pd
import datetime as dt


class WallStreetBetsSentiment:
    def __init__(self, autho_dict, posts):
        self.__authentication = autho_dict
        self.__posts = posts
        self.__comment_list = []
        self.__title_list = []
        self.__ticker_list = pd.read_csv(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\dependencies\\ticker_list.csv")
        self.__sia = SentimentIntensityAnalyzer()

    @property
    # creates instance of reddit using authenticaton from app.WSBAuthentication
    def __connect(self):
        return praw.Reddit(
            client_id=self.__authentication.get("app_id"),
            client_secret=self.__authentication.get("secret"),
            username=self.__authentication.get("username"),
            password=self.__authentication.get("password"),
            user_agent=self.__authentication.get("user_agent")
        )

    @property
    # fetches data from a specified subreddit using a filter method e.g. recent, hot
    def __fetch_data(self):
        sub = self.__connect.subreddit("wallstreetbets")  # select subreddit
        new_wsb = sub.hot(limit=self.__posts)  # sorts by new and pulls the last 1000 posts of r/wsb
        return new_wsb

    @property
    # saves the comments of posts to a dataframe
    def __break_up_data(self):
        for submission in self.__fetch_data:
            self.__title_list.append(submission.title)  # creates list of post subjects, elements strings
            submission.comments.replace_more(limit=1)

            for comment in submission.comments.list():
                dictionary_data = {comment.body}
                self.__comment_list.append(dictionary_data)
        return pd.DataFrame(self.__comment_list, columns=['Comments'])

    # saves all comments to a csv document saved in 'logs'
    def debug(self):
        save_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\logs"
        return self.__break_up_data.to_excel(save_file + "\\log-{}.xlsx".format(
            dt.datetime.now().strftime("D%Y-%m-%d_T%H.%M.%S")), sheet_name='Log')

    # loops though comments to find tickers in self.ticker_list
    def parser(self, enable_debug=bool):
        ticker_list = list(self.__ticker_list['Symbol'].unique())
        # titlelist = list(df2['Titles'].unique())
        comment_list = list(self.__break_up_data['Comments'].unique())
        ticker_count_list = []

        for ticker in ticker_list:
            count = []
            sentiment = 0
            for comment in comment_list:
                # count = count + re.findall((r'\s{}\s').format(ticker), str(comment))
                count = count + re.findall((' ' + ticker + ' '), str(comment))

                if len(count) > 0:
                    score = self.__sia.polarity_scores(comment)
                    sentiment = score['compound']  # adding all the compound sentiments
            if len(count) > 0:
                ticker_count_list.append([ticker, len(count), (sentiment / len(count))])

        if enable_debug is True:
            self.debug()

        else:
            pass
        # ISSUE: the re.findall function would return match on AIN if someone says PAIN
        df4 = pd.DataFrame(ticker_count_list, columns=['Ticker', 'Count', 'Sentiment'])
        df4 = df4.sort_values(by='Count', ascending=False)
        return df4
