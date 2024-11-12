from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy instance
db = SQLAlchemy()

def init_db(app):
    # Initialize the database with the Flask app
    db.init_app(app)  # Bind db instance to app
    with app.app_context():
        db.create_all()  # Create tables if they don’t exist
