# __init__.py
# Configures the Flask app.

from flask import Flask
from .config import Config
from .db_setup import db, init_db
from .routes import main  # Import the blueprint containing routes


def create_app():
    # Create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database with the app
    init_db(app)

    # Register blueprints for routes
    app.register_blueprint(main)

    return app
