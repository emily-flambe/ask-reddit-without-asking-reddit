from flask import Flask
from flask_cors import CORS
from .config import Config
from .db_setup import db, init_db
from .routes import main  # Import the blueprint containing routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)  # Initialize the database with the app
    CORS(app)  # Enable CORS
    app.register_blueprint(main)  # Register the routes blueprint
    return app
