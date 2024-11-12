# main.py
# Entrypoint for the Flask app. This file creates and runs the Flask app

from . import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
