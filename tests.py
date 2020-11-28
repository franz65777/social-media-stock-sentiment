import app.WSBAuthentication as creds
import app_3.app_3 as WSB
from pprint import pprint
import os
import pandas as pd

instance = WSB.WallStreetBets(autho_dict=creds.autho, posts=1)

__list = instance.break_up_data
converted_list = instance.debug(data=__list)

comment_list = pd.read_csv(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\logs\\log.csv")

ticker = WSB.Ticker()

