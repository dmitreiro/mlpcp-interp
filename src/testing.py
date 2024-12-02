# %%
import pandas as pd;
import numpy as np;
import os
import random;
import matplotlib.pyplot as plt;
from sklearn.preprocessing import StandardScaler,MinMaxScaler;
from sklearn.model_selection import train_test_split;
from sklearn.linear_model import LinearRegression;
from sklearn.metrics import mean_squared_error, r2_score,mean_absolute_error,mean_absolute_percentage_error; 
from sklearn.ensemble import RandomForestRegressor;
from sklearn.svm import SVR;
import xgboost as xgb;
from IPython.core.interactiveshell import InteractiveShell;
from IPython.display import display;
import configparser
import time;
import joblib;
from sklearn.multioutput import MultiOutputRegressor;

# Reading configuration file
config = configparser.ConfigParser()
config.read(r"config/config.ini")

# Accessing variables
DATA = config.get("Paths", "data_cleaned")
MODELS = config.get("Paths", "models")
Y_TEST = config.get("Files", "y_test")

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

    # Predict training values
    try:
        y_test_pred = modelo.predict(X_test)
    except Exception as e:
        print(f"Error predicting values: {e}")
        return
    
    # Performance on training data
    r2_test = r2_score(y_test, y_test_pred)
    mae_test = mean_absolute_error(y_test, y_test_pred)
    mape_test = mean_absolute_percentage_error(y_test, y_test_pred)

    print(f'R-squared on {test_method} test for {grid}_{method} model: {r2_test}')
    print(f'MAE on {test_method} test for {grid}_{method} model: {mae_test}')
    print(f'MAPE on {test_method} test for {grid}_{method} model: {mape_test}')

    return {
        "grid": grid,
        "model_method": method,
        "test_method": test_method,
        "r2": r2_test,
        "mae": mae_test,
        "mape": mape_test
    }

result_path = os.path.join(MODELS, "testing_performance_metrics.csv")

# Check if the file exists and delete it if it does
if os.path.exists(result_path):
    os.remove(result_path)

# Iterate over the main folder numbers and subfolder numbers to train and evaluate models
for grid in GRIDS:
    for method in METHODS:
        for test_method in METHODS:
            result = test_and_evaluate(grid, method, test_method)
            if result:  # Ensure result is not None
                # Save results
                result_df = pd.DataFrame([result])
                write_header = not os.path.exists(result_path)
                result_df.to_csv(result_path, mode="a", header=write_header, index=False)
                print(f"Testing performance metrics saved to {result_path}")
