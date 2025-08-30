"""Backend package initialization."""
from flask import Flask
from .routes import register_routes

def create_app() -> Flask:
    """Application factory for the Flask backend."""
    app = Flask(__name__)
    register_routes(app)
    return app

