import logging
import re
import requests
from datetime import datetime, timezone
from requests.auth import HTTPBasicAuth
from .config import Config
from .database_models import RedditPost
from .db_setup import db

logging.basicConfig(level=logging.DEBUG)


class RedditHandler:
    def __init__(self, client_id, client_secret, refresh_token, user_agent):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.user_agent = user_agent
        self.access_token = None

    def get_access_token(self):
        """Fetch a new access token using the refresh token."""
        response = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            data={"grant_type": "refresh_token", "refresh_token": self.refresh_token},
            headers={"User-Agent": self.user_agent},
        )
        self.access_token = response.json().get("access_token")
        return self.access_token

    def fetch_reddit_data(self, query_params):
        """Fetch data from the Reddit API based on query parameters."""
        if not self.access_token:
            self.get_access_token()

        # Merge query_params into defaults
        default_params = Config.DEFAULT_REDDIT_SEARCH_PARAMS
        params = {**default_params, **query_params}

        # Extract parameters
        search_term = params.get("search_term")
        search_entire_posts = params.get("search_entire_posts")
        sort = params.get("sort")
        time_period = params.get("time_period")
        subreddit = params.get("subreddit")
        restrict_sr = True if subreddit else False

        # Set the URL based on whether a subreddit is specified
        url = (
            f"https://oauth.reddit.com/r/{subreddit}/search"
            if subreddit
            else "https://oauth.reddit.com/search"
        )

        # Set up query parameters
        q = search_term if search_entire_posts else f"title:{search_term}"
        api_params = {
            "q": q,
            "sort": sort,
            "t": time_period,
            "restrict_sr": restrict_sr,
        }

        # Set headers with access token and user agent
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": self.user_agent,
        }

        # Send request to Reddit API
        response = requests.get(url, headers=headers, params=api_params)

        if response.status_code != 200:
            logging.error(f"Failed to fetch data: {response.status_code}")
            return []

        # Parse and filter posts
        posts = response.json().get("data", {}).get("children", [])
        return api_params, posts

    def filter_posts(self, posts, limit):
        """
        Filter Reddit posts.
        -   Remove posts with a score less than 5.
        -   Remove posts with less than 10 words.
        -   Sort posts by score in descending order and return the top 'limit' posts (or all if limit is None).
        """

        # Add a field, 'all_text', that combines the title and text of each post
        for post in posts:
            post["data"]["all_text"] = f"{post['data'].get('title', '')} {post['data'].get('selftext', '')}".strip()

        filtered_posts = [
            {
                "title": post["data"]["title"],
                "url": post["data"]["url"],
                "text": post["data"].get("selftext", ""),
                "reddit_id": post["data"]["id"],
                "score": post["data"]["score"],
                "created_utc": post["data"]["created_utc"],
                "retrieved_utc": datetime.now(timezone.utc).isoformat(),
            }
            for post in posts
            if "data" in post  # Ensure 'data' key exists
            and post["data"].get("score", 0) >= 5
            and len(re.sub(r"http\S+", "", post["data"].get("all_text", ""))) > 10
        ]

        return sorted(filtered_posts, key=lambda x: x["score"], reverse=True)[:limit]

    def save_to_database(self, posts):
        """Save filtered Reddit posts to the database."""
        for post in posts:
            post = post["data"]
            # Truncate title and text to first 100 characters
            post["title"] = post["title"][:100]
            post["selftext"] = post["selftext"][:100] if post["selftext"] else ""
            if not RedditPost.query.filter_by(reddit_id=post["id"]).first():
                new_post = RedditPost(
                    title=post["title"],
                    url=post["url"],
                    text=post["selftext"],
                    reddit_id=post["id"],
                )
                db.session.add(new_post)
        db.session.commit()




# Usage example
if __name__ == "__main__":
    handler = RedditHandler(
        client_id=Config.CLIENT_ID,
        client_secret=Config.CLIENT_SECRET,
        refresh_token=Config.REFRESH_TOKEN,
        user_agent="RedditDataCollector/1.0",
    )

    query_params = {
        "search_term": "Python programming",
        "search_entire_posts": True,
        "limit": 10,
        "sort": "relevance",
        "time_period": "month",
        "subreddit": "learnpython",
    }

    api_params, posts = handler.fetch_reddit_data(query_params)
    #handler.save_to_database(posts)
