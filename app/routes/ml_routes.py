from flask import Blueprint, jsonify, request
import pandas as pd
import sqlite3
import config
from app.mlutil import main

# Create a blueprint for ml-related routes
ml_routes = Blueprint('ml_routes', __name__)

def get_car_data(car_id): 
  try:
      conn = sqlite3.connect(config.SQLALCHEMY_DATABASE_URI)  # Connect to your database
      query = f"SELECT * FROM raw_data WHERE car_id = ?"
      car_data = pd.read_sql_query(query, conn, params=(car_id,))
      conn.close()

      # Check if the data exists for the car_id
      if car_data.empty:
          return None  # Return None if no data is found for the car_id
      return car_data
  except Exception as e:
      print(f"Error fetching data from raw_data table: {e}")
      return None

@ml_routes.route('/predict/<int:car_id>', methods=['GET'])
def predict():
    car_id = request.args.get('car_id')
    if not car_id:
        # If no query params are provided, load data from CSV
        df = pd.read_csv('data/ml/dataset.csv')
    
        result = main(df)
        return jsonify({"prediction": result}), 200
    else:
        # Fetch car data from raw_data table
        car_data = get_car_data(car_id)
        
        if car_data is None:
            return jsonify({'error': 'Car ID not found in raw_data.'}), 404
