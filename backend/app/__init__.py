# __init__.py
# Configures the Flask app.
# This file imports the Config class from config.py, the main blueprint from routes.py, and the database instance from db.py.
# It also initializes the database and registers the main blueprint with the app.
# Finally, it creates and returns the Flask app instance.

from flask import Flask
from .config import Config
from .routes import main
from .db import db, init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    init_db(app)

    # Register blueprints (e.g., routes)
    app.register_blueprint(main)

    return app
