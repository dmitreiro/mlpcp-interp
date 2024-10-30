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

# List of main folder numbers to iterate over
main_folder_numbers = [
    500,
    1000,
    1500,
    2000,
    2500,
]  # Update with your actual main folder numbers
subfolder_numbers = [1, 2, 3, 4, 5]  # Subfolders labeled 1 to 5

# Function to train and evaluate model
def train_and_evaluate(main_folder_number, subfolder_number):
    # Construct the paths to the training files
    X_train_path = os.path.join(
        DATA, f"x_train_{main_folder_number}_{subfolder_number}.csv"
    )
    y_train_path = os.path.join(
        DATA, f"y_train_{main_folder_number}_{subfolder_number}.csv"
    )

    # Load the feature and target data
    try:
        print(f"Loading data from {X_train_path} and {y_train_path}")
        X_train = pd.read_csv(X_train_path)
        y_train = pd.read_csv(y_train_path)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    # Define the columns for X_train
    l = []
    for x in range(1, 21):
        l.append("Force_x_" + str(x))
        l.append("Force_y_" + str(x))
        for p in range(1, 565):  # elements number
            l.append("Strain_x_" + str(p) + "_" + str(x))
            l.append("Strain_y_" + str(p) + "_" + str(x))
            l.append("Strain_xy_" + str(p) + "_" + str(x))

    # Assign the defined column names to X_train
    X_train.columns = l
    print(f"X_train shape: {X_train.shape}")
    print(f"X_train columns: {X_train.columns.tolist()}")

    # Start the timer for training
    start_time_training = time.monotonic()

    # Train the model on the training data
    try:
        modelo = MultiOutputRegressor(xgb.XGBRegressor(learning_rate=0.02, max_depth=6, n_estimators=1000, tree_method="hist", device="cpu")).fit(X_train, y_train)
    except Exception as e:
        print(f"Error training model: {e}")
        return

    # Stop the timer for training
    end_time_training = time.monotonic()
    training_duration = end_time_training - start_time_training
    print(
        f"Training duration for model {main_folder_number}_{subfolder_number}: {training_duration} seconds"
    )

    # Save the trained model
    model_filename = f"{MODELS}/modelo_xgboost_{main_folder_number}_{subfolder_number}.joblib"
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
            f"R-squared on Train Data for {main_folder_number}_{subfolder_number}: {r2_train}"
        )
        print(
            f"MAE on Train Data for {main_folder_number}_{subfolder_number}: {mae_train}"
        )
        print(
            f"MAPE on Train Data for {main_folder_number}_{subfolder_number}: {mape_train}"
        )
    except Exception as e:
        print(f"Error calculating performance metrics: {e}")
        return

    return {
        "main_folder_number": main_folder_number,
        "subfolder_number": subfolder_number,
        "r2": r2_train,
        "mae": mae_train,
        "mape": mape_train,
        "training_duration": training_duration,
    }


# Iterate over the main folder numbers and subfolder numbers to train and evaluate models
results = []
for main_folder_number in main_folder_numbers:
    for subfolder_number in subfolder_numbers:
        result = train_and_evaluate(main_folder_number, subfolder_number)
        if result:  # Ensure result is not None
            results.append(result)

# Save overall results
results_df = pd.DataFrame(results)
overall_results_path = os.path.join(MODELS, "overall_performance_metrics.csv")
results_df.to_csv(overall_results_path, index=False)
print(f"Overall performance metrics saved to {overall_results_path}")
