from flask import Blueprint, request, jsonify
from ..models import db, RawData

raw_data_api = Blueprint('raw_data_api', __name__)

# Create
@raw_data_api.route('/rawdata', methods=['POST'])
def create_raw_data():
    data = request.json
    new_raw_data = RawData(**data)
    db.session.add(new_raw_data)
    db.session.commit()
    return jsonify({"message": "Raw data created", "raw_data": new_raw_data.id}), 201

# Read all
@raw_data_api.route('/rawdata', methods=['GET'])
def get_raw_data():
    raw_data = RawData.query.all()
    return jsonify([raw_data_item_to_dict(rd) for rd in raw_data])

# Read one
@raw_data_api.route('/rawdata/<int:raw_data_id>', methods=['GET'])
def get_single_raw_data(raw_data_id):
    raw_data = RawData.query.get_or_404(raw_data_id)
    return jsonify(raw_data_item_to_dict(raw_data))

# Update
@raw_data_api.route('/rawdata/<int:raw_data_id>', methods=['PUT'])
def update_raw_data(raw_data_id):
    raw_data = RawData.query.get_or_404(raw_data_id)
    data = request.json

    for key, value in data.items():
        setattr(raw_data, key, value)

    db.session.commit()
    return jsonify({"message": "Raw data updated", "raw_data": raw_data.id})

# Delete
@raw_data_api.route('/rawdata/<int:raw_data_id>', methods=['DELETE'])
def delete_raw_data(raw_data_id):
    raw_data = RawData.query.get_or_404(raw_data_id)
    db.session.delete(raw_data)
    db.session.commit()
    return jsonify({"message": "Raw data deleted"})

def raw_data_item_to_dict(raw_data):
    return {column.name: getattr(raw_data, column.name) for column in raw_data.__table__.columns}
