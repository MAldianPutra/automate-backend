from flask import Blueprint, request, jsonify
from ..models import db, Car

car_api = Blueprint('car_api', __name__)

# Create
@car_api.route('/cars', methods=['POST'])
def create_car():
    data = request.json
    new_car = Car(
        model_name=data.get('model_name'),
        plate_number=data.get('plate_number'),
        chassis_number=data.get('chassis_number')
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({"message": "Car created", "car": new_car.id}), 201

# Read all
@car_api.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    return jsonify([{"id": car.id, "model_name": car.model_name, "plate_number": car.plate_number, "chassis_number": car.chassis_number} for car in cars])

# Read one
@car_api.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    car = Car.query.get_or_404(car_id)
    return jsonify({"id": car.id, "model_name": car.model_name, "plate_number": car.plate_number, "chassis_number": car.chassis_number})

# Update
@car_api.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = Car.query.get_or_404(car_id)
    data = request.json

    car.model_name = data.get('model_name', car.model_name)
    car.plate_number = data.get('plate_number', car.plate_number)
    car.chassis_number = data.get('chassis_number', car.chassis_number)

    db.session.commit()
    return jsonify({"message": "Car updated", "car": car.id})

# Delete
@car_api.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return jsonify({"message": "Car deleted"})
