from flask import Flask
from flask_cors import CORS
from app.routes import main

def create_app():
    app = Flask(__name__)

    # Enable CORS for all routes
    CORS(app)

    # Register blueprints
    app.register_blueprint(main)
    return app  