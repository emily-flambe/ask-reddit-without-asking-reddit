# data_collector.py
# This module will contain the logic to fetch data from Reddit and save it to the database. We will use the requests library to make HTTP requests to the Reddit API. We will also use the RedditPost model to save the data to the database.

import requests
from .config import Config
from .models import RedditPost
from .db import db
from requests.auth import HTTPBasicAuth

def get_access_token():
    # Use refresh token to get a new access token
    response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=HTTPBasicAuth(Config.CLIENT_ID, Config.CLIENT_SECRET),
        data={
            "grant_type": "refresh_token",
            "refresh_token": Config.REFRESH_TOKEN
        },
        headers={"User-Agent": "RedditDataCollector/1.0"}
    )
    return response.json().get("access_token")

def fetch_reddit_data(search_term):
    access_token = get_access_token()
    url = "https://oauth.reddit.com/r/factorio/search"
    params = {"q": f"title:{search_term}", "sort": "new", "t": "day", "restrict_sr": "1"}
    headers = {"Authorization": f"Bearer {access_token}", "User-Agent": "RedditDataCollector/1.0"}
    
    response = requests.get(url, headers=headers, params=params)
    posts = response.json().get("data", {}).get("children", [])
    return [{"title": post["data"]["title"], "url": post["data"]["url"], "text": post["data"].get("selftext", "")} for post in posts]

def save_to_database(posts):
    for post in posts:
        if not RedditPost.query.filter_by(reddit_id=post["id"]).first():  # Avoid duplicates
            new_post = RedditPost(
                title=post["title"],
                url=post["url"],
                text=post["text"],
                reddit_id=post["id"]
            )
            db.session.add(new_post)
    db.session.commit()
