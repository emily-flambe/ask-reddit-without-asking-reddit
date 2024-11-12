from flask import Blueprint, jsonify, request
from .data_collector import fetch_reddit_data, save_to_database
from .models import RedditPost

main = Blueprint('main', __name__)

@main.route('/search_reddit', methods=['GET'])
def search_reddit():
    term = request.args.get('term', 'Gleba')
    posts = fetch_reddit_data(term)
    save_to_database(posts)
    return jsonify(posts)

@main.route('/visualize_wordcloud', methods=['GET'])
def visualize_wordcloud():
    # This could be an endpoint that generates a word cloud from the database
    wordcloud_data = generate_wordcloud_data()
    return jsonify(wordcloud_data)
