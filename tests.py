import app.WSBAuthentication as creds
import app.WSBSentiment as wsb
import matplotlib as plot

sentiment = wsb.WallStreetBetsSentiment(autho_dict=creds.autho, posts=1)
print(sentiment.parser(enable_debug=True)) # Use enable_debug=True to save the log of comments. (slows down performance)
