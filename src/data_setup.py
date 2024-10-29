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
print(config.sections())

# Accessing variables
DATA = config.get("Paths", "data_cleaned")
X_TRAIN = config.get("Files", "x_train")
Y_TRAIN = config.get("Files", "y_train")

# IMPORT THE ENTIRE DATA FOR RANDOMLY SEPARATE
# THE DATA SHOULD ONLY CONTAIN USEFUL SIMULATIONS (Fxy20>Fxy19)
# THE DATA SHOULD ALREADY BE NORMALIZED
X = pd.read_csv(X_TRAIN)
display(X)

# IMPORT THE ENTIRE DATA FOR RANDOMLY SEPARATE
# THE DATA SHOULD ONLY CONTAIN USEFUL SIMULATIONS (Fxy20>Fxy19)
# THE DATA SHOULD ALREADY BE NORMALIZED
# THE DATA SHOULD ONLY CONTAIN THE NON-CONSTANT VALUES OF THE CONSTITUTIVE LAW
y = pd.read_csv(Y_TRAIN)
display(y)

X=X.reset_index(drop=True)
y=y.reset_index(drop=True)

# DEFINE MODEL modelo_xgboost_aaaa_b
# A=aaaa
# b=Nº do modelo [1-5]
A=2000
b=1

# RANDOMIZE NUMBER OF ROWS
random_rows = random.sample(range(len(X)), A)
len(random_rows)

# SELECTED VERSION ONLY
X_selected = X.iloc[random_rows]
display(X_selected)

y_selected = y.iloc[random_rows]
display(y_selected)

# RESET INDEX OF NUMBER OF SIMULATIONS
X_selected=X_selected.reset_index(drop=True)
y_selected=y_selected.reset_index(drop=True)

display(X_selected)
display(y_selected)

X_selected.to_csv(f"{DATA}/x_train_{A}_{b}.csv", index=False)
y_selected.to_csv(f"{DATA}/y_train_{A}_{b}.csv", index=False)
