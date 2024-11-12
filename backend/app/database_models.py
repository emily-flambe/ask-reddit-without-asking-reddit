from .db_setup import db
from datetime import datetime


class RedditPost(db.Model):
    __tablename__ = "reddit_posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    url = db.Column(db.String(255))
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reddit_id = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f"<RedditPost(title={self.title}, url={self.url})>"
