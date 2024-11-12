from flask import Blueprint, jsonify, request
from .data_collector import fetch_reddit_data, save_to_database
from .database_models import RedditPost

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def hello():
    return "Great job"

@main.route('/search_reddit', methods=['GET'])
def search_reddit():
    term = request.args.get('term', 'Gleba')
    posts = fetch_reddit_data(term)
    save_to_database(posts)
    return jsonify(posts)