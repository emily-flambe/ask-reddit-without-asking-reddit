import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///reddit_data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLIENT_ID = os.getenv("WEB_APP_CLIENT_ID")
    CLIENT_SECRET = os.getenv("WEB_APP_CLIENT_SECRET")
    REFRESH_TOKEN = os.getenv("WEB_APP_REFRESH_TOKEN")
