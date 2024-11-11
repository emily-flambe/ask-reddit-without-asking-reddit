import os
from flask import Flask, request, redirect, url_for
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

CLIENT_ID = os.getenv("WEB_APP_CLIENT_ID")
CLIENT_SECRET = os.getenv("WEB_APP_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
REFRESH_TOKEN = os.getenv("WEB_APP_REFRESH_TOKEN")  # Optional
breakpoint()

@app.route('/')
def home():
    # If a refresh token is already set, use it to get a new access token
    if REFRESH_TOKEN:
        print("refresh token")
        return redirect(url_for('refresh_access_token'))
    # Otherwise, initiate the authorization code flow
    auth_url = (
        "https://www.reddit.com/api/v1/authorize?"
        f"client_id={CLIENT_ID}&response_type=code&state=random&"
        f"redirect_uri={REDIRECT_URI}&duration=permanent&scope=identity"
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Retrieve the authorization code
    code = request.args.get('code')
    if not code:
        return "Error: No code provided", 400

    # Exchange the code for an access token and refresh token
    token_response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        },
        headers={"User-Agent": "YourAppName/1.0"}
    )

    if token_response.status_code == 200:
        tokens = token_response.json()
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')
        return f"Access Token: {access_token}<br>Refresh Token: {refresh_token}"
    else:
        return f"Error: {token_response.json()}", 400

@app.route('/refresh_access_token')
def refresh_access_token():
    # Use the refresh token to get a new access token
    token_response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
        data={
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN
        },
        headers={"User-Agent": "YourAppName/1.0"}
    )

    if token_response.status_code == 200:
        tokens = token_response.json()
        access_token = tokens.get('access_token')
        return f"New Access Token: {access_token}"
    else:
        return f"Error refreshing token: {token_response.json()}", 400

if __name__ == '__main__':
    app.run(debug=True)
