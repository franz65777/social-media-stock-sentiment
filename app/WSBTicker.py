from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re


class Ticker:

    def __init__(self, ticker):
        self.ticker = ticker
        self.comments = []
        self.sentiment = []
        self.count = 0
        self.positions = []
        self.sia = SentimentIntensityAnalyzer()

    def increment_count(self):
        self.count = self.count + 1
        return self.count

    def analyzer(self):
        score = self.sia.polarity_scores(self.comments)
        sentiment = score['compound']
        return self.sentiment.append(sentiment)

    def get_positions(self):
        # positions are in form SPY 300c 11/20
        for comment in self.comments:
            position = re.findall(r'{}\s\d+\w\s\d+\S\d+'.format(self.ticker), comment)
            if position != []:
                self.positions.append(position)
        return self.positions

    def main(self):
        return {
            "ticker": self.ticker,
            "mentions": self.increment_count(),
            "comments": self.comments

        }
