from datetime import datetime
from app import create_app, db
from app.models import Car, RawData, PredictionResult

app = create_app()

with app.app_context():
    # Create mock data for Car table
    car1 = Car(model_name='Toyota Corolla', plate_number='ABC123', chassis_number='XYZ987654321')
    car2 = Car(model_name='Honda Civic', plate_number='DEF456', chassis_number='UVW123456789')

    db.session.add(car1)
    db.session.add(car2)
    db.session.commit()

    # Create mock data for RawData table
    raw_data1 = RawData(
        car_id = car1.id,
        engine_rpm=3000.0,
        throttle=30.5,
        engine_load=75.0,
        coolant_temperature=90.0,
        long_term_fuel_trim_bank_1=1.5,
        short_term_fuel_trim_bank_1=1.0,
        intake_manifold_pressure=101.3,
        commanded_throttle_actuator=45.0,
        fuel_air_commanded_equiv_ratio=0.85,
        intake_air_temp=25.0,
        timing_advance=10.0,
        catalyst_temperature_bank1_sensor1=400.0,
        catalyst_temperature_bank1_sensor2=405.0,
        control_module_voltage=14.0
    )

    raw_data2 = RawData(
        car_id = car2.id,
        engine_rpm=3500.0,
        throttle=28.0,
        engine_load=80.0,
        coolant_temperature=95.0,
        long_term_fuel_trim_bank_1=1.8,
        short_term_fuel_trim_bank_1=1.2,
        intake_manifold_pressure=102.0,
        commanded_throttle_actuator=50.0,
        fuel_air_commanded_equiv_ratio=0.9,
        intake_air_temp=27.0,
        timing_advance=12.0,
        catalyst_temperature_bank1_sensor1=410.0,
        catalyst_temperature_bank1_sensor2=415.0,
        control_module_voltage=13.8
    )

    db.session.add(raw_data1)
    db.session.add(raw_data2)
    db.session.commit()

    # Create mock data for PredictionResult table
    prediction_result1 = PredictionResult(
        car_id=car1.id,
        engine_score=85.0,
        brakes_score=78.0,
        oil_score=88.0
    )

    prediction_result2 = PredictionResult(
        car_id=car2.id,
        engine_score=82.0,
        brakes_score=80.0,
        oil_score=85.0
    )

    db.session.add(prediction_result1)
    db.session.add(prediction_result2)
    db.session.commit()

    print("Mock data inserted successfully!")
