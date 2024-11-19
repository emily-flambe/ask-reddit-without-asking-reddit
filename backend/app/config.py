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

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_CHAT_MODEL = "gpt-4o-mini-2024-07-18"
    OPENAI_MAX_TOKENS = 2000

    # User Agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

    # Default Reddit search parameters
    DEFAULT_REDDIT_SEARCH_PARAMS = {
        "search_entire_posts": False,
        "limit": None,
        "sort": "relevance",
        "time_period": "month",
        "subreddit": None,
    }
