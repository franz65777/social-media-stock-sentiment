from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import praw
import pandas as pd
import datetime as dt
import os

df = pd.read_csv('C:/Users/John/Test Workbooks/Reddit Bot Data/All US Tickers.csv')
df3 = pd.read_excel('C:/Users/John/Test Workbooks/Reddit Bot Data/WSBcomments.xlsx')
tickerlist = list(df['Symbol'].unique())
commentlist = list(df3['Comments'].unique())

sia = SentimentIntensityAnalyzer()

class Ticker:
    

    def __init__(self, ticker): #pass the comment into ticker
        self.ticker = ticker
        self.comments = []
        self.titles = []
        self.sentiment = []
        self.count = 0
    # Remove this 
    def get_comments(self):
        for comment in commentlist:
            if len(re.findall((r'\s{}\s').format(self.ticker), comment)) > 0:
                self.comments.append(comment)
        return self.comments

    def get_count(self):
        self.count = len(self.comments)
        return self.count

    def analyzer(self):
        for comment in self.comments:
            score = sia.polarity_scores(comment)
            sentiment = score['compound']
            self.sentiment.append(sentiment)
                    
            
            
 #Call ticker in WSBSentiment        
objlist = []
for ticker in tickerlist:
    objlist.append(Ticker(ticker))

for obj in objlist:
    obj.get_comments()
    obj.get_count()

final_list = []
for obj in objlist:
    if obj.count > 0:
        final_list.append(obj)

for obj in final_list:
    obj.analyzer()
    
