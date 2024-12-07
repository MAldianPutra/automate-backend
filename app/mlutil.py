import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Function to load and preprocess data. The df is n row * 14 features table
def load_data(df, features, time_steps=7*24):
    # Convert datetime columns to UNIX timestamp
    # Will be changed if the date is already in integer
    df['Date_of_Compute'] = pd.to_datetime(df['Date_of_Compute'], format="%d/%m/%Y %H:%M").astype(np.int64) // 10**9
    df['Date_of_Garage'] = pd.to_datetime(df['Date_of_Garage'], format="%d/%m/%Y %H:%M").astype(np.int64) // 10**9

    # Define x min and max values for features
    x_min = np.array([0.0000000e+00, 0.0000000e+00, 1.5686275e+01, 0.0000000e+00,
                             2.8000000e+01, -5.4687500e+00, -1.2500000e+01, 1.8000000e+01,
                             1.0605000e+01, 0.0000000e+00, 2.8099998e+01, 1.0000000e+00,
                             1.4993856e+09, 1.4993856e+09])
    x_max = np.array([2.26950000e+03, 4.80000000e+01, 4.07843130e+01, 9.64705890e+01,
                             9.10000000e+01, 3.90625000e+00, 1.17187500e+01, 1.01000000e+02,
                             1.43350000e+01, 0.00000000e+00, 5.72799988e+02, 2.00000000e+00,
                             1.73335680e+09, 1.71365760e+09])

    # Reconstruct scaler for features
    scaler = create_target_scaler(x_min, x_max)

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

# Main function
def main(model_path, csv_file_path):
    # Load model
    model = load_model(model_path)
    print("Model loaded successfully.")
    print(f"Model input shape: {model.input_shape}")
    print(model.summary())

    # Load and preprocess CSV data
    data = pd.read_csv(csv_file_path)
    features = [
        "ENGINE_RPM ()", "VEHICLE_SPEED ()", "THROTTLE ()", "ENGINE_LOAD ()", "COOLANT_TEMPERATURE ()",
        "LONG_TERM_FUEL_TRIM_BANK_1 ()", "SHORT_TERM_FUEL_TRIM_BANK_1 ()", "INTAKE_MANIFOLD_PRESSURE ()",
        "CONTROL_MODULE_VOLTAGE ()", "FUEL_AIR_COMMANDED_EQUIV_RATIO ()", "CATALYST_TEMPERATURE_BANK1_SENSOR1 ()",
        "Moving", "Date_of_Compute", "Date_of_Garage"
    ]

    # Select first 300 rows
    random_sample = data.head(300)
    X_seq = load_data(random_sample, features)

    # Define target scaler
    y_min = np.array([-847.])
    y_max = np.array([364.])
    target_scaler = create_target_scaler(y_min, y_max)

    # Predict
    predictions = model.predict(X_seq)
    print("Predictions (normalized):")
    print(predictions)

    # Denormalize predictions
    predictions_mean = predictions.mean(axis=0)  # Take mean if needed
    y_pred_denormalized = target_scaler.inverse_transform([[predictions_mean]])
    print("Predicted Value (denormalized):")
    print(y_pred_denormalized[0][0])

# If running as a standalone script
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python mlutil.py <model_path> <csv_file_path>")
    else:
        main(sys.argv[1], sys.argv[2])
