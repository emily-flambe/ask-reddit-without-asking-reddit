import logging
import requests
from flask import Blueprint, jsonify, request
from .config import Config
from .reddit_handler import RedditHandler
from .database_models import RedditPost
from .ai_handler import AIHandler

main = Blueprint("main", __name__)
ai_handler = AIHandler(
    api_key=Config.OPENAI_API_KEY,
    max_tokens=Config.OPENAI_MAX_TOKENS,
    openai_chat_model=Config.OPENAI_CHAT_MODEL,
)
reddit_handler = RedditHandler(
    client_id=Config.CLIENT_ID,
    client_secret=Config.CLIENT_SECRET,
    refresh_token=Config.REFRESH_TOKEN,
    user_agent=Config.USER_AGENT,
)

logging.basicConfig(level=logging.INFO)

@main.route("/", methods=["GET"])
def hello():
    return "Great job"


@main.route("/health", methods=["GET"])
def health_check():
    # Step 1: Attempt to get a new access token
    try:
        access_token = reddit_handler.get_access_token()
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


@main.route("/get_saved_posts", methods=["GET"])
def get_saved_posts():
    # Query all saved posts
    posts = RedditPost.query.all()
    # Format the posts as a list of dictionaries
    result = [
        {"title": post.title, "url": post.url, "text": post.text} for post in posts
    ]
    return jsonify(result)


@main.route("/summarize_post_from_database", methods=["POST"])
def summarize_post_from_database():
    # Assuming the client sends a JSON payload with post_id
    post_id = request.json.get("post_id")

    # Retrieve the post from the database by ID
    post = RedditPost.query.get(post_id)
    if not post:
        return jsonify({"status": "fail", "message": "Post not found"}), 404

    # Send the post text to ChatGPT for summarization
    summary = ai_handler.summarize(post.text)

    # Return the summary
    return jsonify({"status": "success", "summary": summary})


@main.route("/ask_reddit", methods=["POST"])
def ask_reddit():
    """
    Endpoint to ask a question and summarize Reddit posts related to that question.
    Default values for params are set in data_collector.py.
    """

    query_params = request.json

    search_term = query_params.get("search_term")
    if not search_term:
        return (
            jsonify(
                {
                    "status": "fail",
                    "message": "This is an app for asking a question. You need to have something to ask. Try and keep up.",
                }
            ),
            400,
        )

    # Optionally use AI to construct query params using the prompt. This is FANCY and more expensive.
    if query_params.get("generate_reddit_query_using_ai"):
        query_params = ai_handler.generate_query_params(search_term)
        logging.info(f"Updated query params using AI fanciness: {query_params}")

    # Fetch and save Reddit data based on the query
    api_params, posts = reddit_handler.fetch_reddit_data(query_params=query_params)
    reddit_handler.save_to_database(posts)

    # Sanitize and prepare text for summarization
    filtered_reddit_posts = reddit_handler.filter_posts(
        posts, limit=query_params.get("limit")
    )
    # Return an error if no posts are found
    if not filtered_reddit_posts:
        return (
            jsonify(
                {
                    "status": "fail",
                    "message": "No relevant posts found. Try asking a different question.",
                }
            ),
            404,
        )

    text_to_summarize = "\n".join([post["text"] for post in filtered_reddit_posts])

    # Calculate the number of tokens to use for summarization
    # messages_for_ai_summarization is the object that will be sent to the AI model containing prompts for the system and user
    messages_for_ai_summarization = ai_handler.generate_messages_summarize_posts(topic=search_term, text=text_to_summarize)
    tokens_and_cost = ai_handler.calculate_token_usage(messages=messages_for_ai_summarization)
    tokens = tokens_and_cost.get("total_tokens")
    cost = tokens_and_cost.get("cost")
    logging.info(f"Request will need {tokens} and cost ${cost:.2f}")

    # Generate summary
    summary = ai_handler.send_request(messages=messages_for_ai_summarization)

    return (
        jsonify(
            {
                "status": "success",
                "summary": summary,
                "posts": filtered_reddit_posts,
                "query": query_params,
            }
        ),
        200,
    )