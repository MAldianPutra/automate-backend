from flask import Blueprint, jsonify
from .car_routes import car_api
from .raw_data_routes import raw_data_api
from .prediction_result_routes import prediction_result_api
from .garage_routes import garage_api

# Create a general blueprint for miscellaneous routes
general_api = Blueprint('general_api', __name__)

# Define a simple health check route
@general_api.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

def register_blueprints(app):
    app.register_blueprint(car_api, url_prefix='/api')
    app.register_blueprint(raw_data_api, url_prefix='/api')
    app.register_blueprint(prediction_result_api, url_prefix='/api')
    app.register_blueprint(garage_api, url_prefix='/api')
    app.register_blueprint(general_api, url_prefix='/api')
