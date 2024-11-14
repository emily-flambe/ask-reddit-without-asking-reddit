# app/config.py

import os


class Config:
    # Configure SQLite as the database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///reddit_data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Reddit API Credentials (example)
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

    # Default Reddit search parameters
    DEFAULT_REDDIT_SEARCH_PARAMS = {
        "search_entire_posts": False,
        "limit": 20,
        "sort": "top",
        "time_period": "month",
        "subreddit": None,
        "restrict_sr": True,
    }
