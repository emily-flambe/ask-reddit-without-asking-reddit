# data_collector.py
# This module will contain the logic to fetch data from Reddit and save it to the database. We will use the requests library to make HTTP requests to the Reddit API. We will also use the RedditPost model to save the data to the database.

import logging
import re
import requests
from .config import Config
from .database_models import RedditPost
from .db_setup import db
from datetime import datetime, timezone
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


def fetch_reddit_data(query_params):
    """
    Query the Reddit API for posts based on the search term and other parameters.
    Parameters (included in query_params, or from default values):
        search_term (str): The term to search for in the post titles.
        search_entire_posts (bool): Whether to search entire posts. If False, only the titles will be searched.
        limit (int): The maximum number of posts to use to generate the summary. More posts means more context for the summary, and also more spend.
        sort (str): The sorting method for the posts (e.g., "top", "new", "relevance").
        time_period (str): The time period to search within (e.g., "day", "week", "month", "year", "all").
        restrict_sr (bool): Restrict to the subreddit specified in the subreddit parameter.
        subreddit (str, Optional): The subreddit to search within.

    Returns:
        list: A list of dictionaries containing post information.

    """

    access_token = get_access_token()

    # Merge query_params into defaults
    default_params = Config.DEFAULT_REDDIT_SEARCH_PARAMS
    params = {**default_params, **query_params}

    # Extract parameters
    search_term = params.get("search_term")
    search_entire_posts = params.get("search_entire_posts")
    limit = params.get("limit")
    sort = params.get("sort")
    time_period = params.get("time_period")
    restrict_sr = params.get("restrict_sr")
    subreddit = params.get("subreddit")

    # Set the URL based on whether a subreddit is specified
    if subreddit:
        url = f"https://oauth.reddit.com/r/{subreddit}/search"
    else:
        url = "https://oauth.reddit.com/search"

    # Set up query parameters
    q = search_term if search_entire_posts else f"title:{search_term}"
    params = {
        "q": q,
        "sort": sort,
        "t": time_period,
        "restrict_sr": restrict_sr,
    }

    # Set headers with access token and user agent
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "AskRedditWithoutAskingReddit/1.0 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    }

    # Send request to Reddit API
    response = requests.get(url, headers=headers, params=params)

    # Check for successful response
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return []

    # Parse response data
    posts = response.json().get("data", {}).get("children", [])

    # Filter posts to only include those with a score >= 5 and with more than 10 characters of text (excluding any URLs)
    filtered_posts = [
        {
            "title": post["data"]["title"],
            "url": post["data"]["url"],
            "text": post["data"].get("selftext", ""),
            "reddit_id": post["data"]["id"],
            "score": post["data"]["score"],
            "created_utc": post["data"]["created_utc"],
            "retreived_utc": datetime.now(timezone.utc).isoformat(),
        }
        for post in posts
        if post["data"].get("score", 0) >= 5
        and len(re.sub(r"http\S+", "", post["data"].get("selftext", ""))) > 10
    ]

    # Limit to top 20 posts based on score
    filtered_posts = sorted(filtered_posts, key=lambda x: x["score"], reverse=True)[
        :limit
    ]

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
