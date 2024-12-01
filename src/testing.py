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

def test_and_evaluate(grid, method):
    # IMPORT THE FILTERED DATA FOR TESTING
    # THE DATA SHOULD ALREADY BE NORMALIZED
    # THE DATA SHOULD ONLY CONTAIN USEFUL SIMULATIONS (Fxy20>Fxy19)
    # CHANGE NUMBERS ON THE MODEL NAME FILE FOR THE DESIRED MODEL

    # Construct the paths to the testing files
    x_test = os.path.join(
        DATA, f"x_test_{grid}_{method}.csv"
    )
    xgb_model = os.path.join(
        MODELS, f"xgb_{grid}_{method}.joblib"
    )
    print(f"Loading data from {x_test} and {Y_TEST}")
    X_test = pd.read_csv(x_test)
    y_test = pd.read_csv(Y_TEST)

    # Get the number of columns and points
    n_cols = len(X_test.columns)
    points = int((n_cols/20-2)/3)

    # DEFINE X COLUMNS
    l=[]
    for x in range(1,21):
        l.append("Force_x_"+str(x))
        l.append("Force_y_"+str(x))
        for p in range(1, points+1):  # elements number
            l.append("Strain_x_"+str(p)+"_"+str(x))
            l.append("Strain_y_"+str(p)+"_"+str(x))
            l.append("Strain_xy_"+str(p)+"_"+str(x))
    X_test.columns = l

    #display(X_test)
    #display(y_test)

    # Load trained model
    print("Loading xgb model...")
    modelo = joblib.load(xgb_model)
    #print(modelo.get_params())

    # PREDICT TRAINING VALUES
    y_test_pred = modelo.predict(X_test)

    # PERFORMANCE ON TRAINING
    r2_test = r2_score(y_test, y_test_pred)
    mae_test = mean_absolute_error(y_test, y_test_pred)
    mape_test = mean_absolute_percentage_error(y_test, y_test_pred)

    print(f'R-squared on Test Data for {grid}_{method}: {r2_test}')
    print(f'MAE on Test Data for {grid}_{method}: {mae_test}')
    print(f'MAPE on Test Data for {grid}_{method}: {mape_test}')

    return {
        "grid": grid,
        "method": method,
        "r2": r2_test,
        "mae": mae_test,
        "mape": mape_test,
    }

# Iterate over the main folder numbers and subfolder numbers to train and evaluate models
results = []
for grid in GRIDS:
    for method in METHODS:
        result = test_and_evaluate(grid, method)
        if result:  # Ensure result is not None
            results.append(result)

# Save overall results
results_df = pd.DataFrame(results)
overall_results_path = os.path.join(MODELS, "testing_performance_metrics.csv")
results_df.to_csv(overall_results_path, index=False)
print(f"Overall performance metrics saved to {overall_results_path}")
