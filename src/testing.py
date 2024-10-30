# %%
import pandas as pd;
import numpy as np;
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
X_TEST = config.get("Files", "x_test")
Y_TEST = config.get("Files", "y_test")
XGB_MODEL = config.get("Files", "xgb_model")

# IMPORT THE FILTERED DATA FOR TESTING
# THE DATA SHOULD ALREADY BE NORMALIZED
# THE DATA SHOULD ONLY CONTAIN USEFUL SIMULATIONS (Fxy20>Fxy19)
# CHANGE NUMBERS ON THE MODEL NAME FILE FOR THE DESIRED MODEL

X_test = pd.read_csv(X_TEST)

# DEFINE X COLUMNS
l=[]
for x in range(1,21):
    l.append("Force_x_"+str(x))
    l.append("Force_y_"+str(x))
    for p in range(1,565):#elements number
        l.append("Strain_x_"+str(p)+"_"+str(x))
        l.append("Strain_y_"+str(p)+"_"+str(x))
        l.append("Strain_xy_"+str(p)+"_"+str(x))
X_test.columns = l

display(X_test)

# IMPORT THE FILTERED DATA FOR TRAINING
# THE DATA SHOULD ALREADY BE NORMALIZED
# THE DATA SHOULD ONLY CONTAIN USEFUL SIMULATIONS (Fxy20>Fxy19)
# COPY TRAINING SET FROM "(...)\Datasets\Datatrain\XXXX\N\ to (...)\TRAIN
# CHANGE NUMBERS ON THE TRAINING NAME FILE FOR THE DESIRED MODEL

y_test = pd.read_csv(Y_TEST)
display(y_test)

# LOAD TRAINED MODEL
# ADAPT TO NAME ON JOBLIB EG: modelo_xgboost_2500_3
modelo = joblib.load(XGB_MODEL)
print(modelo.get_params())

# PREDICT TRAINING VALUES
y_test_pred = modelo.predict(X_test)

# PERFORMANCE ON TRAINING
r2_test = r2_score(y_test, y_test_pred)
mae_test = mean_absolute_error(y_test, y_test_pred)
mape_test = mean_absolute_percentage_error(y_test, y_test_pred)
print(f'R-squared on Test Data: {r2_test}')
print(f'MAE on Test Data: {mae_test}')
print(f'MAPE on Test Data: {mape_test}')
