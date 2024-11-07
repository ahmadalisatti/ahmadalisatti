from flask import Flask
from .config import Config
from .models import setup_db
from . import routes  # Import the routes module to register routes with the app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from Config class

    setup_db(app)  # Initialize the database with the app

    # Register the Blueprint
    app.register_blueprint(routes.bp)

    return app
