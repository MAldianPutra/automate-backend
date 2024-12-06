from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
import logging
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)

    # Initialize Swagger
    root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    swagger_file_path = os.path.join(root_directory, 'swagger.yml')
    swagger = Swagger(app, template_file=swagger_file_path)

    # Enable CORS for all routes
    CORS(app)  

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Application setup started")

    with app.app_context():
        from . import models
        from .routes import register_blueprints
        register_blueprints(app)
        db.create_all()

    # Register error handlers
    register_error_handlers(app)

    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500