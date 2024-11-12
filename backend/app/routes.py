import requests
from flask import Blueprint, jsonify, request
from .data_collector import get_access_token, fetch_reddit_data, save_to_database
from .database_models import RedditPost

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def hello():
    return "Great job"


@main.route("/health", methods=["GET"])
def health_check():
    # Step 1: Attempt to get a new access token
    try:
        access_token = get_access_token()
        if not access_token:
            return (
                jsonify({"status": "fail", "message": "Failed to obtain access token"}),
                403,
            )
    except Exception as e:
        return (
            jsonify(
                {"status": "fail", "message": f"Error obtaining access token: {e}"}
            ),
            500,
        )

    # Step 2: Verify access token by making a request to Reddit API
    # (this should probably be a simpler request)
    url = "https://oauth.reddit.com/r/factorio/search?q=title:Gleba&sort=new&t=day&restrict_sr=1"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "YourAppName/1.0 (by /u/yourusername)",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return (
                jsonify({"status": "success", "message": "Authentication successful"}),
                200,
            )
        elif response.status_code == 403:
            return (
                jsonify(
                    {
                        "status": "fail",
                        "message": "403 Forbidden - Check authentication and permissions",
                    }
                ),
                403,
            )
        else:
            return (
                jsonify(
                    {
                        "status": "fail",
                        "message": f"Unexpected status code {response.status_code}",
                        "response": response.text,
                    }
                ),
                response.status_code,
            )
    except requests.RequestException as e:
        return (
            jsonify(
                {"status": "fail", "message": f"Request to Reddit API failed: {e}"}
            ),
            500,
        )


@main.route("/search_reddit", methods=["GET"])
def search_reddit():
    term = request.args.get("term", "Gleba")
    posts = fetch_reddit_data(term)
    save_to_database(posts)
    return jsonify(posts)


@main.route("/get_saved_posts", methods=["GET"])
def get_saved_posts():
    # Query all saved posts
    posts = RedditPost.query.all()
    # Format the posts as a list of dictionaries
    result = [
        {"title": post.title, "url": post.url, "text": post.text} for post in posts
    ]
    return jsonify(result)
