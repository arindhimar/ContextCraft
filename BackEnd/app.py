import logging
from flask import Flask, redirect, request
from kiteconnect import KiteConnect
from dotenv import load_dotenv
import os

app = Flask(__name__)
env = load_dotenv()
# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.DEBUG)
# Set up logging to file
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

 

#get data from .env file
# Load environment variables from .env file
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
# API_KEY = env.get("API_KEY", "lol")
# API_SECRET = env.get("API_SECRET", "kidding me ??")
kite = KiteConnect(api_key=API_KEY)

@app.route('/')
def login():
    login_url = kite.login_url()
    return redirect(login_url)

@app.route('/callback')
def callback():
    request_token = request.args.get('request_token')
    if not request_token:
        return "No request token found", 400

    try:
        data = kite.generate_session(request_token, api_secret=API_SECRET)
        kite.set_access_token(data["access_token"])
        print(data)
        return f"Access token generated: {data['access_token']}"
    except Exception as e:
        return f"Error generating session: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
