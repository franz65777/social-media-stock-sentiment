from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import pandas as pd
from app_2.WSBDataParser import DataParser as DP

df = pd.read_csv('C:/Users/John/Test Workbooks/Reddit Bot Data/All US Tickers.csv')
tickerlist = list(df)



class Ticker(DP):
    def __init__(self, autho_dict, posts, ticker):
        super().__init__(autho_dict, posts)
        self.ticker = ticker
        self.comments = []
        # self.titles = []
        self.sentiment = []
        # self.pos_sent = []
        # self.neg_sent = []
        self.sia = SentimentIntensityAnalyzer()
        self.count = 0
        self.avgsent = 0
        self.positions = []

    def get_comments(self):
        for comment in list(self.break_up_data['Comments'].unique()):
            if len(re.findall((r'\b{}\b').format(self.ticker), str(comment))) > 0:
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

    def create_tickers(self):
        objlist = []
        for ticker in self.ticker_list['Symbol'].unique():
            objlist.append(Ticker(autho_dict=))

        for obj in objlist:
            obj.get_comments()
            obj.get_count()

        final_list = []
        for obj in objlist:
            if obj.count > 0:
                final_list.append(obj)

        for obj in final_list:
            obj.analyzer()
            obj.average_sentiment()
            obj.get_positions()

        ticker_count_list = []
        for obj in final_list:
            ticker_count_list.append([obj.ticker, obj.count, obj.avgsent])

        df4 = pd.DataFrame(ticker_count_list, columns=['Ticker', 'Count', 'Sentiment'])
        df4 = df4.sort_values(by='Count', ascending=False)




