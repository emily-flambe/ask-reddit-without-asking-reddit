import os
from flask import Flask, jsonify, request
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Load environment variables
CLIENT_ID = os.getenv("WEB_APP_CLIENT_ID")
CLIENT_SECRET = os.getenv("WEB_APP_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("WEB_APP_REFRESH_TOKEN")  # Ensure this is set

if not REFRESH_TOKEN:
    raise EnvironmentError("WEB_APP_REFRESH_TOKEN is required as an environment variable.")

def get_new_access_token():
    # Use the refresh token to get a new access token
    token_response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
        data={
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN
        },
        headers={"User-Agent": "YourAppName/1.0"}
    )

    # Check if the token request was successful
    if token_response.status_code == 200:
        tokens = token_response.json()
        return tokens.get('access_token')
    else:
        raise RuntimeError(f"Failed to refresh access token: {token_response.json()}")

def get_post_text(subreddit, post_id, access_token):
    # Fetch the full post data from the /comments endpoint
    url = f"https://oauth.reddit.com/r/{subreddit}/comments/{post_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "YourAppName/1.0"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Extract the title, selftext, and url of the post
        post_data = response.json()[0]["data"]["children"][0]["data"]
        return {
            "title": post_data.get("title"),
            "url": f"https://www.reddit.com{post_data.get('permalink')}",
            "text": post_data.get("selftext")
        }
    else:
        return None  # Return None if the request fails

@app.route('/search_factorio', methods=['GET'])
def search_factorio():
    """
    Search for recent posts in the Factorio subreddit with a specific term in the title.
    The search term can be provided as a query parameter, defaulting to "Gleba".

    Example usage:
    - /search_factorio?term=modding
    - /search_factorio?term=blueprint
    """

    # SEARCH PARAMS
    search_term = request.args.get('term', 'Gleba')
    sort_by = request.args.get('sort', 'top')
    restrict_day_range = request.args.get('days', '1')
    
    # Get a new access token using the refresh token
    access_token = get_new_access_token()
    
    # Define the search URL and parameters using the search term
    search_url = "https://oauth.reddit.com/r/factorio/search"
    params = {
        "q": f"title:{search_term}",
        "sort": sort_by,
        "t": "day", # keep time interval fixed as "day" for simplicity
        "restrict_sr": restrict_day_range
    }

    # Make the request to Reddit's search API with the access token
    search_response = requests.get(
        search_url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "YourAppName/1.0"
        },
        params=params
    )

    # For each post, retrieve the title, url, and full text using the post ID
    if search_response.status_code == 200:
        posts = search_response.json().get("data", {}).get("children", [])
        detailed_posts = []
        
        for post in posts:
            post_id = post["data"]["id"]
            post_data = get_post_text("factorio", post_id, access_token)
            if post_data:
                detailed_posts.append(post_data)

        return jsonify(detailed_posts)
    else:
        return jsonify({"error": "Failed to retrieve posts", "details": search_response.json()}), search_response.status_code

if __name__ == '__main__':
    app.run(debug=True)
