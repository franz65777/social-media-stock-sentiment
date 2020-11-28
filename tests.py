import app.WSBAuthentication as creds
import app_2.WSBTicker as ticker
from pprint import pprint




tickers_data = ticker.Ticker(autho_dict=creds.autho, posts=1)
pprint(tickers_data.create_tickers())