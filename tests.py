import app.WSBAuthentication as creds
import app_3.app_3 as WSB
from pprint import pprint
import os
import pandas as pd


instance = WSB.WallStreetBets(autho_dict=creds.autho, posts=1)

print(instance.create())

