from flask import Blueprint, jsonify
import os
import json

# Create a new blueprint for the garage endpoint
garage_api = Blueprint('garage_api', __name__)

@garage_api.route('/garage', methods=['GET'])
def get_garage_data():
    # Construct the path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'garage.json')

    # Read the JSON file
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500
