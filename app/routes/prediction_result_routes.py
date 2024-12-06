from flask import Blueprint, request, jsonify
from ..models import db, PredictionResult

prediction_result_api = Blueprint('prediction_result_api', __name__)

# Create
@prediction_result_api.route('/predictionresults', methods=['POST'])
def create_prediction_result():
    data = request.json
    new_prediction_result = PredictionResult(**data)
    db.session.add(new_prediction_result)
    db.session.commit()
    return jsonify({"message": "Prediction result created", "prediction_result": new_prediction_result.id}), 201

# Read all
@prediction_result_api.route('/predictionresults', methods=['GET'])
def get_prediction_results():
    prediction_results = PredictionResult.query.all()
    return jsonify([prediction_result_to_dict(pr) for pr in prediction_results])

# Read one
@prediction_result_api.route('/predictionresults/<int:prediction_result_id>', methods=['GET'])
def get_single_prediction_result(prediction_result_id):
    prediction_result = PredictionResult.query.get_or_404(prediction_result_id)
    return jsonify(prediction_result_to_dict(prediction_result))

# Update
@prediction_result_api.route('/predictionresults/<int:prediction_result_id>', methods=['PUT'])
def update_prediction_result(prediction_result_id):
    prediction_result = PredictionResult.query.get_or_404(prediction_result_id)
    data = request.json

    for key, value in data.items():
        setattr(prediction_result, key, value)

    db.session.commit()
    return jsonify({"message": "Prediction result updated", "prediction_result": prediction_result.id})

# Delete
@prediction_result_api.route('/predictionresults/<int:prediction_result_id>', methods=['DELETE'])
def delete_prediction_result(prediction_result_id):
    prediction_result = PredictionResult.query.get_or_404(prediction_result_id)
    db.session.delete(prediction_result)
    db.session.commit()
    return jsonify({"message": "Prediction result deleted"})

def prediction_result_to_dict(prediction_result):
    return {column.name: getattr(prediction_result, column.name) for column in prediction_result.__table__.columns}
