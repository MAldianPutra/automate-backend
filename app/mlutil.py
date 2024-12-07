import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import os

# Function to preprocess data (scaling)
def data_preprocessing(df, features, time_steps=7*24):
    # Convert datetime columns to UNIX timestamp
    df['Date_of_Compute'] = pd.to_datetime(df['Date_of_Compute'], format="%d/%m/%Y %H:%M").astype(np.int64) // 10**9
    df['Date_of_Garage'] = pd.to_datetime(df['Date_of_Garage'], format="%d/%m/%Y %H:%M").astype(np.int64) // 10**9

    # Define original min and max values for features
    original_min = np.array([0.0000000e+00, 0.0000000e+00, 1.5686275e+01, 0.0000000e+00,
                             2.8000000e+01, -5.4687500e+00, -1.2500000e+01, 1.8000000e+01,
                             1.0605000e+01, 0.0000000e+00, 2.8099998e+01, 1.0000000e+00,
                             1.4993856e+09, 1.4993856e+09])
    original_max = np.array([2.26950000e+03, 4.80000000e+01, 4.07843130e+01, 9.64705890e+01,
                             9.10000000e+01, 3.90625000e+00, 1.17187500e+01, 1.01000000e+02,
                             1.43350000e+01, 0.00000000e+00, 5.72799988e+02, 2.00000000e+00,
                             1.73335680e+09, 1.71365760e+09])

    # Reconstruct scaler for features
    scaler = create_target_scaler(original_min, original_max)

    # Normalize features
    X = scaler.transform(df[features])

    # Create sequences
    X_seq = []
    for i in range(len(X) - time_steps):
        X_seq.append(X[i:i + time_steps])
    X_seq = np.array(X_seq)

    return X_seq

# Function to create scaler for target variable
def create_target_scaler(original_min, original_max):
    scaler = MinMaxScaler()
    data_range = original_max - original_min
    data_range[data_range == 0] = 1
    scaler.scale_ = 1 / data_range
    scaler.min_ = -original_min * scaler.scale_
    scaler.data_min_ = original_min
    scaler.data_max_ = original_max
    scaler.data_range_ = data_range
    return scaler

# Function to make predictions and denormalize results
def predict(model, df, features, target_min, target_max):
    # Preprocess data to get scaled X_seq
    X_seq = data_preprocessing(df, features)

    # Define target scaler for denormalization
    target_scaler = create_target_scaler(target_min, target_max)

    # Make predictions
    predictions = model.predict(X_seq)
    print("Predictions (normalized):")
    print(predictions)

    # Denormalize predictions
    predictions_mean = predictions.mean(axis=0)  # Average if needed
    y_pred_denormalized = target_scaler.inverse_transform([[predictions_mean]])

    return y_pred_denormalized[0][0]

# Main function that loads the model, makes prediction, and returns result
def main(df):
    # Load the model
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'ml', 'lstm_model.h5')
    model = load_model(model_path)
    print("Model loaded successfully.")
    print(f"Model input shape: {model.input_shape}")
    print(model.summary())

    # Define features and target min/max values
    features = [
        "ENGINE_RPM ()", "VEHICLE_SPEED ()", "THROTTLE ()", "ENGINE_LOAD ()", "COOLANT_TEMPERATURE ()",
        "LONG_TERM_FUEL_TRIM_BANK_1 ()", "SHORT_TERM_FUEL_TRIM_BANK_1 ()", "INTAKE_MANIFOLD_PRESSURE ()",
        "CONTROL_MODULE_VOLTAGE ()", "FUEL_AIR_COMMANDED_EQUIV_RATIO ()", "CATALYST_TEMPERATURE_BANK1_SENSOR1 ()",
        "Moving", "Date_of_Compute", "Date_of_Garage"
    ]

    target_min = np.array([-847.])
    target_max = np.array([364.])

    # Call predict to get the denormalized result
    result = predict(model, df, features, target_min, target_max)
    
    return result

# If running as a standalone script
if __name__ == "__main__":
    # Get the current directory (app directory)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define relative path to dataset
    csv_file_path = os.path.join(current_dir, '..', 'data', 'ml', 'dataset.csv')
    
    # Load dataset as df
    data = pd.read_csv(csv_file_path)
    random_sample = data.sample(n=300, random_state=42)
    
    # Call main to process the data and get the result
    result = main(random_sample)
    print("Final Prediction (denormalized):", result)
