from app_2.WSBDataParser import DataParser as DP
import app_2.WSBTicker as tker
import re


class WallStreetBets(DP):
    def __init__(self, autho_dict, posts):
        super().__init__(autho_dict, posts)
        self.tickers = []
        self.mentions_tickers = []

    def parser(self, enable_debug=bool):
        ticker_list = list(self.ticker_list['Symbol'].unique())
        comment_list = self.break_up_data
        comment_list_filtered = list(comment_list['Comments'].unique())

        for ticker in ticker_list:
            for comment in comment_list_filtered:
                find_ticker = re.findall(r'\b{}\b'.format(ticker), str(comment))
                if len(find_ticker) > 0:
                    self.mentions_tickers.append([str(ticker), str(comment)])
        return self.mentions_tickers

