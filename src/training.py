import configparser
import pandas as pd
import time
import joblib
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_absolute_percentage_error,
)
from sklearn.multioutput import MultiOutputRegressor
import xgboost as xgb
import os

# Reading configuration file
config = configparser.ConfigParser()
config.read(r"config/config.ini")

# Accessing variables
DATA = config.get("Paths", "data_cleaned")
MODELS = config.get("Paths", "models")
Y_TRAIN = config.get("Files", "y_train")
METRICS = config.get("Files", "train_metrics")

GRIDS = [20, 30, 40]
METHODS = ["linear", "cubic", "multiquadric"]

# Function to train and evaluate model
def train_and_evaluate(grid, method):
    # Construct the paths to the training files
    x_train = os.path.join(
        DATA, f"x_train_{grid}_{method}.csv"
    )

    # Load the feature and target data
    try:
        print(f"Loading data from {x_train} and {Y_TRAIN}")
        X_train = pd.read_csv(x_train)
        y_train = pd.read_csv(Y_TRAIN)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    # Get the number of columns and points
    n_cols = len(X_train.columns)
    points = int((n_cols/20-2)/3)

    # Define the columns for X_train
    l = []
    for x in range(1, 21): # each timestep
        l.append("Force_x_" + str(x))
        l.append("Force_y_" + str(x))
        for p in range(1, points+1):  # elements number
            l.append("Strain_x_" + str(p) + "_" + str(x))
            l.append("Strain_y_" + str(p) + "_" + str(x))
            l.append("Strain_xy_" + str(p) + "_" + str(x))

    # Assign the defined column names to X_train
    X_train.columns = l
    print(f"X_train shape: {X_train.shape}")
    # print(f"X_train columns: {X_train.columns.tolist()}")

    # Start the timer for training
    start_time_training = time.monotonic()

    # Train the model on the training data
    try:
        print(f"Starting train...")
        modelo = MultiOutputRegressor(xgb.XGBRegressor(learning_rate=0.02, max_depth=4, n_estimators=1000, tree_method="hist", device="cpu")).fit(X_train, y_train)
    except Exception as e:
        print(f"Error training model: {e}")
        return

    # Stop the timer for training
    end_time_training = time.monotonic()
    training_duration = end_time_training - start_time_training
    print(
        f"Training duration for model {grid}_{method}: {training_duration} seconds"
    )

    # Save the trained model
    model_filename = os.path.join(
        MODELS, f"xgb_{grid}_{method}.joblib")
    try:
        joblib.dump(modelo, model_filename)
        print(f"Model saved as {model_filename}")
    except Exception as e:
        print(f"Error saving model: {e}")
        return

    # Predict on the training data
    try:
        y_train_pred = modelo.predict(X_train)
    except Exception as e:
        print(f"Error predicting on training data: {e}")
        return

    # Performance on training data
    try:
        r2_train = r2_score(y_train, y_train_pred)
        mae_train = mean_absolute_error(y_train, y_train_pred)
        mape_train = mean_absolute_percentage_error(y_train, y_train_pred)
        print(
            f"R-squared on Train Data for {grid}_{method}: {r2_train}"
        )
        print(
            f"MAE on Train Data for {grid}_{method}: {mae_train}"
        )
        print(
            f"MAPE on Train Data for {grid}_{method}: {mape_train}"
        )
    except Exception as e:
        print(f"Error calculating performance metrics: {e}")
        return

    return {
        "grid": grid,
        "method": method,
        "r2": r2_train,
        "mae": mae_train,
        "mape": mape_train,
        "training_duration": training_duration
    }

def main():
    """
    Main function to start code execution.
    """

    # Check if the file exists and delete it if it does
    if os.path.exists(METRICS):
        os.remove(METRICS)

    # Iterate over the main folder numbers and subfolder numbers to train and evaluate models
    for grid in GRIDS:
        for method in METHODS:
            result = train_and_evaluate(grid, method)
            if result:  # Ensure result is not None
                # Save results
                result_df = pd.DataFrame([result])
                write_header = not os.path.exists(METRICS)
                result_df.to_csv(METRICS, mode="a", header=write_header, index=False)
                print(f"Training performance metrics saved to {METRICS}")

if __name__ == "__main__":
    main()