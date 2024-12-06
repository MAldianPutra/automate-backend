from .car_routes import car_api
from .raw_data_routes import raw_data_api
from .prediction_result_routes import prediction_result_api

def register_blueprints(app):
    app.register_blueprint(car_api, url_prefix='/api')
    app.register_blueprint(raw_data_api, url_prefix='/api')
    app.register_blueprint(prediction_result_api, url_prefix='/api')
