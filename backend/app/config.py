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
