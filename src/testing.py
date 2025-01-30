import pandas as pd
import os
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_absolute_percentage_error
)
import configparser
import time
import joblib

# Reading configuration file
config = configparser.ConfigParser()
config.read(r"config/config.ini")

# Accessing variables
DATA = config.get("Paths", "data_cleaned")
MODELS = config.get("Paths", "models")
Y_TEST = config.get("Files", "y_test")
METRICS = config.get("Files", "test_metrics")

GRIDS = [20, 30, 40]
METHODS = ["linear", "cubic", "multiquadric"]

def test_and_evaluate(grid, method, test_method):
    # IMPORT THE FILTERED DATA FOR TESTING
    # THE DATA SHOULD ALREADY BE NORMALIZED
    # THE DATA SHOULD ONLY CONTAIN USEFUL SIMULATIONS (Fxy20>Fxy19)
    # CHANGE NUMBERS ON THE MODEL NAME FILE FOR THE DESIRED MODEL

    # Construct the paths to the testing files
    x_test = os.path.join(
        DATA, f"x_test_{grid}_{test_method}.csv"
    )
    xgb_model = os.path.join(
        MODELS, f"xgb_{grid}_{method}.joblib"
    )

    # Load the feature and target data
    try:
        print(f"Loading data from {x_test} and {Y_TEST}")
        X_test = pd.read_csv(x_test)
        y_test = pd.read_csv(Y_TEST)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    # Get the number of columns and points
    n_cols = len(X_test.columns)
    points = int((n_cols/20-2)/3)

    # Define the columns for X_test
    l=[]
    for x in range(1,21): # each timestep
        l.append("Force_x_"+str(x))
        l.append("Force_y_"+str(x))
        for p in range(1, points+1):  # elements number
            l.append("Strain_x_"+str(p)+"_"+str(x))
            l.append("Strain_y_"+str(p)+"_"+str(x))
            l.append("Strain_xy_"+str(p)+"_"+str(x))
    
    # Assign the defined column names to X_train
    X_test.columns = l
    print(f"X_train shape: {X_test.shape}")

    # Load trained model
    try:
        print("Loading xgb model...")
        modelo = joblib.load(xgb_model)
        #print(modelo.get_params())
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Start the timer
    start_time = time.time()

    # Predict training values
    try:
        y_test_pred = modelo.predict(X_test)
    except Exception as e:
        print(f"Error predicting values: {e}")
        return
    
    # End the timer and calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Convert elapsed time to minutes and seconds
    elapsed_minutes = int(elapsed_time // 60)
    elapsed_seconds = int(elapsed_time % 60)

    # Print total elapsed time in "minutes:seconds" format
    print(
        f"Finished testing {xgb_model} in {elapsed_minutes}:{elapsed_seconds:02d} minutes."
    )
    
    # Performance on training data
    r2_test = r2_score(y_test, y_test_pred)
    mae_test = mean_absolute_error(y_test, y_test_pred)
    mape_test = mean_absolute_percentage_error(y_test, y_test_pred)

    print(f'R-squared on {test_method} test for {grid}_{method} model: {r2_test}')
    print(f'MAE on {test_method} test for {grid}_{method} model: {mae_test}')
    print(f'MAPE on {test_method} test for {grid}_{method} model: {mape_test}')

    # saves predicted y data to csv file
    pred_params_path = os.path.join(DATA, f"y_pred_{grid}_{method}_{test_method}.csv")
    df = pd.DataFrame(y_test_pred)
    df.to_csv(pred_params_path, mode="w", header=True, index=False)

    return {
        "grid": grid,
        "model_method": method,
        "test_method": test_method,
        "r2": r2_test,
        "mae": mae_test,
        "mape": mape_test,
        "testing_duration": elapsed_time
    }

def main():
    """
    Main function to start code execution.
    """

    # Start the timer
    start_time = time.time()

    # Check if the file exists and delete it if it does
    if os.path.exists(METRICS):
        os.remove(METRICS)

    # Iterate over the main folder numbers and subfolder numbers to train and evaluate models
    for grid in GRIDS:
        for method in METHODS:
            for test_method in METHODS:
                result = test_and_evaluate(grid, method, test_method)
                if result:  # Ensure result is not None
                    # Save results
                    result_df = pd.DataFrame([result])
                    write_header = not os.path.exists(METRICS)
                    result_df.to_csv(METRICS, mode="a", header=write_header, index=False)
                    print(f"Testing performance metrics saved to {METRICS}")

    # End the timer and calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Convert elapsed time to minutes and seconds
    elapsed_minutes = int(elapsed_time // 60)
    elapsed_seconds = int(elapsed_time % 60)

    # Print total elapsed time in "minutes:seconds" format
    print(
        f"Total elapsed time: {elapsed_minutes}:{elapsed_seconds:02d} minutes."
    )

if __name__ == "__main__":
    main()