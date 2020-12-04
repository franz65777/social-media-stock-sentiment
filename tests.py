import app.WSBAuthentication as creds
import app.WSBPrimary as WSB
from pprint import pprint
import os
import pandas as pd
import numpy as np
import re

re.purge()

instance = WSB.WallStreetBets(autho_dict=creds.autho, posts=1)

data_0 = instance.live_data()
print(data_0)