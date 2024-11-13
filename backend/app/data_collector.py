# data_collector.py
# This module will contain the logic to fetch data from Reddit and save it to the database. We will use the requests library to make HTTP requests to the Reddit API. We will also use the RedditPost model to save the data to the database.

import logging
import re
import requests
from .config import Config
from .database_models import RedditPost
from .db_setup import db
from requests.auth import HTTPBasicAuth

logging.basicConfig(level=logging.DEBUG)


def get_access_token():
    # Use refresh token to get a new access token
    response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=HTTPBasicAuth(Config.CLIENT_ID, Config.CLIENT_SECRET),
        data={"grant_type": "refresh_token", "refresh_token": Config.REFRESH_TOKEN},
        headers={"User-Agent": "RedditDataCollector/1.0"},
    )
    return response.json().get("access_token")


def fetch_reddit_data(search_term):
    access_token = get_access_token()
    url = "https://oauth.reddit.com/r/factorio/search"
    params = {"q": f"title:{search_term}", "sort": "top", "t": "month", "restrict_sr": "true"}
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "RedditDataCollector/1.0"
    }

    # Send request to Reddit API
    response = requests.get(url, headers=headers, params=params)

    # Check for successful response
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return []

    # Parse response data
    posts = response.json().get("data", {}).get("children", [])

    # Filter posts to only include those with a score >= 5 and with more than 10 characters of text
    filtered_posts = [
        {
            "title": post["data"]["title"],
            "url": post["data"]["url"],
            "text": post["data"].get("selftext", ""),
            "reddit_id": post["data"]["id"],
            "score": post["data"]["score"]
        }
        for post in posts
        if post["data"].get("score", 0) >= 5
        and len(post["data"].get("selftext", "")) > 10
    ]
    
    logging.info(f"Found {len(filtered_posts)} posts for search term: {search_term}")
    logging.debug(filtered_posts)

    # Limit to top 20 posts based on score
    filtered_posts = sorted(filtered_posts, key=lambda x: x["score"], reverse=True)[:20]

    return filtered_posts

def sanitize_reddit_posts(posts):
    """ 
    Remove any URLs and special characters from the "texn" field of the Reddit posts.
    """
    for post in posts:
        # Remove URLs from the text
        post["text"] = re.sub(r"http\S+", "", post["text"])
        # Remove special characters
        post["text"] = re.sub(r"[^a-zA-Z0-9 %.,!?\"']", "", post["text"])
    return posts


def save_to_database(posts):
    for post in posts:
        # Avoid duplicates by checking the reddit_id
        if not RedditPost.query.filter_by(reddit_id=post["reddit_id"]).first():
            new_post = RedditPost(
                title=post["title"],
                url=post["url"],
                text=post["text"],
                reddit_id=post["reddit_id"],
            )
            db.session.add(new_post)
    db.session.commit()  # Commit all new records to the database