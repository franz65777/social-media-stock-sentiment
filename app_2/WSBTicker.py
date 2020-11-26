class Ticker:
    def __init__(self, ticker):
        self.ticker = ticker
        self.count = 0
        self.comments = []

    def increment_count(self):
        self.count = self.count + 1
        return self.count

    def append_comments(self, comment):
        self.comments.append(comment)

    def useable(self):
        return [
            self.ticker,
            self.count,
            self.comments,
        ]
