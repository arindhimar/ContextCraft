import logging
from flask import Flask, redirect, request
from kiteconnect import KiteConnect

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

API_KEY = env.get("API_KEY", "lol")
API_SECRET = env.get("API_SECRET", "kidding me ??")
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
