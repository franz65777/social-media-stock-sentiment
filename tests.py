import app.WSBAuthentication as creds
import app.WSBPrimary as WSB
from pprint import pprint
import os
import pandas as pd

instance = WSB.WallStreetBets(autho_dict=creds.autho, posts=1)
data = instance.create()

for obj in data:
    print(obj.get_values)