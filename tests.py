import app.WSBAuthentication as creds
import app_3.app_3 as WSB
from pprint import pprint

instance = WSB.WallStreetBets(autho_dict=creds.autho, posts=1)

print(instance.break_up_data)
