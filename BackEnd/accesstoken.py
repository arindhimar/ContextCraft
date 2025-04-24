from kiteconnect import KiteConnect
import os

API_KEY = ""


kite = KiteConnect(api_key=API_KEY)


access_token = kite.generate_session(request_token, api_secret="")
print(access_token["access_token"])