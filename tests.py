import app.WSBAuthentication as creds
import app.WSBPrimary as WSB
from pprint import pprint
import os
import pandas as pd
import numpy as np
import re

instance = WSB.WallStreetBets(autho_dict=creds.autho, posts=1)

data_0 = instance.read_submissions(mode="hot")

transfrom = WSB.DataFrameWSB(data_frame=data_0)

print(transfrom.data())