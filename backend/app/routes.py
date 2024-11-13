import requests
from flask import Blueprint, jsonify, request
from .data_collector import get_access_token, fetch_reddit_data, sanitize_reddit_posts, save_to_database
from .database_models import RedditPost
from .chatgpt_summarizer import ChatGPTSummarizer

main = Blueprint('main', __name__)
summarizer = ChatGPTSummarizer()

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


@main.route('/summarize_post', methods=['POST'])
def summarize_post():
    # Assuming the client sends a JSON payload with post_id
    post_id = request.json.get('post_id')

    # Retrieve the post from the database by ID
    post = RedditPost.query.get(post_id)
    if not post:
        return jsonify({"status": "fail", "message": "Post not found"}), 404

    # Send the post text to ChatGPT for summarization
    summary = summarizer.summarize(post.text)

    # Return the summary
    return jsonify({"status": "success", "summary": summary})



@main.route("/ask_reddit", methods=["POST"])
def ask_reddit():
    """
    Endpoint to ask a question and summarize Reddit posts related to that question.
    """
    data = request.json
    query = data.get("q")
    
    if not query:
        return jsonify({"status": "fail", "message": "/ask_reddit requires a question, you donkey"}), 400
    
    # Fetch and save Reddit data based on the query
    posts = fetch_reddit_data(query)
    save_to_database(posts)
    
    # Sanitize and prepare text for summarization
    sanitized_posts = sanitize_reddit_posts(posts)
    sanitized_post_texts = [post['text'] for post in sanitized_posts]
    text_to_summarize = '\n\n'.join(sanitized_post_texts)
    
    # Generate summary
    summary = summarizer.summarize(query, text_to_summarize)
    
    return jsonify({"status": "success", "summary": summary, "posts": sanitized_posts})
