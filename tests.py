import app.WSBAuthentication as creds
import app_2.WSBMain as wsb
import matplotlib as plot
from pprint import pprint

sentiment = wsb.WallStreetBets(autho_dict=creds.autho, posts=1)
pprint(sentiment.parser(enable_debug=False)) # Use enable_debug=True to save the log of comments. (slows down performance)
