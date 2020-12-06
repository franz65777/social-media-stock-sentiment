import app.WSBAuthentication as creds
import app.WSBPrimary as WSB
from pprint import pprint
import os
import pandas as pd
import re
import mysql.connector
import praw
import datetime as dt

"""conn = praw.Reddit(
    client_id=creds.autho.get('app_id'),
    client_secret=creds.autho.get('secret'),
    username=creds.autho.get('username'),
    password=creds.autho.get('password'),
    user_agent=creds.autho.get('user_agent')
)

reader = PSAPI(praw=conn)
start_epoch = int(dt.datetime(2020, 1, 1).timestamp())

comment_list = list(reader.search_comments(after=start_epoch,
                                           subreddit='wallstreetbets'))
appended_data = []
for comment in comment_list:
    data = []
    data.append(dt.datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'))
    data.append(comment.author)
    data.append(comment.score)
    data.append(comment.body)

    appended_data.append(data)

dataframe = pd.DataFrame(appended_data, columns=["Datetime", "Author", "Upvotes", "Body"])
dataframe.to_csv(path_or_buf="E:\\Golafshan Capital\\wsb-sentiment\\dependencies\\test.csv")"""

instance = WSB.WallStreetBets(autho_dict=creds.autho, posts=1)
instance.live_submissions()

