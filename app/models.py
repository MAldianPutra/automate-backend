from . import db
from datetime import datetime, timezone

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    modified_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, nullable=True)

class Car(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100))
    plate_number = db.Column(db.String(50))
    chassis_number = db.Column(db.String(100))    

class RawData(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    engine_rpm = db.Column(db.Float)
    throttle = db.Column(db.Float)
    engine_load = db.Column(db.Float)
    coolant_temperature = db.Column(db.Float)
    long_term_fuel_trim_bank_1 = db.Column(db.Float)
    short_term_fuel_trim_bank_1 = db.Column(db.Float)
    intake_manifold_pressure = db.Column(db.Float)
    commanded_throttle_actuator = db.Column(db.Float)
    fuel_air_commanded_equiv_ratio = db.Column(db.Float)
    intake_air_temp = db.Column(db.Float)
    timing_advance = db.Column(db.Float)
    catalyst_temperature_bank1_sensor1 = db.Column(db.Float)
    catalyst_temperature_bank1_sensor2 = db.Column(db.Float)
    control_module_voltage = db.Column(db.Float)

    car = db.relationship('Car', backref=db.backref('raw_data', lazy=True))

class PredictionResult(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    engine_score = db.Column(db.Float)
    brakes_score = db.Column(db.Float)
    oil_score = db.Column(db.Float)

    car = db.relationship('Car', backref=db.backref('prediction_results', lazy=True))


# Add more models as needed