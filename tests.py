import app.WSBAuthentication as creds
import app.WSBPrimary as WSB
from pprint import pprint
import os
import pandas as pd
import numpy as np
import re

instance = WSB.WallStreetBets(autho_dict=creds.autho, posts=1)

data_0 = instance.read_submissions
data_0["Ticker"] = ""

for index, row in data_0.iterrows():
    for ticker in instance.ticker_list["Symbol"]:
        row["Ticker"] = ticker

print(data_0.head(50))
