from app_2.WSBDataParser import DataParser as DP
import app_2.WSBTicker as tker
import re


class WallStreetBets(DP):
    def __init__(self, autho_dict, posts):
        super().__init__(autho_dict, posts)
        self.tickers = []

    def parser(self, enable_debug=bool):
        ticker_list = list(self.ticker_list['Symbol'].unique())
        comment_list = list(self.break_up_data['Comments'].unique())

        for ticker in ticker_list:
            for comment in comment_list:
                # count = count + re.findall((r'\s{}\s').format(ticker), str(comment))
                find_ticker = re.findall((' ' + ticker + ' '), str(comment))

                if len(find_ticker) > 0:
                    ticker_instance = tker.Ticker(ticker=ticker)
                    if any(self.tickers) is True:
                        for i in self.tickers:
                            if i[0] == ticker:
                                i[1] = i[1] + 1


                    else:
                        ticker_instance.increment_count()
                        ticker_instance.append_comments(comment=comment)
                        self.tickers.append(ticker_instance.useable())

        if enable_debug is True:
            self.debug()

        return self.tickers