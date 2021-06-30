import app.data_gathering as data
import app.Authentication as authentication
import datetime as dt

reddit = data.Reddit(client_id=authentication.reddit.get('app_id'),
                     client_secret=authentication.reddit.get('secret'),
                     username=authentication.reddit.get('username'),
                     password=authentication.reddit.get('password'),
                     user_agent=authentication.reddit.get('user_agent'))

# ["investing", "cryptocurrency", "securityanalysis", "wallstreetbets"]

reddit.results(reddit_stream="investing+securityanalysis+cryptocurrency+wallstreetbets")
