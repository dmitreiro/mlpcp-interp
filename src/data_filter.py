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
import time;
import joblib;
from sklearn.multioutput import MultiOutputRegressor;

# %%
# Importar ficheiro X
X = pd.read_csv(r"/home/dmitreiro/WinVM/abaqus_datasets/x_cruciform.csv", header=None)
display(X)

# Remover linhas duplicadas
X.drop_duplicates(inplace=True)

# Remover linhas com NULL
X.dropna(inplace=True)

# Remover Coluna 1
# X = X.iloc[:, 1:]

display(X)

# %%
# Importar ficheiro y
y = pd.read_csv(r"/home/dmitreiro/WinVM/abaqus_datasets/y_cruciform.csv", sep=",")
display(y)

# Filtro de colunas
colunas_selecionadas = [coluna for coluna in y.columns if not coluna.startswith('Unnamed')]
colunas_sem_nan = [coluna for coluna in colunas_selecionadas if not y[coluna].isnull().all()]
y = y[colunas_sem_nan]

# y=y.loc[X.index]
display(y)

# %%
# Colocar colunas no X
l=[]
for x in range(1,21):
    l.append("Force_x_"+str(x))
    l.append("Force_y_"+str(x))
    for p in range(1,565):#numero de elementos
        l.append("Strain_x_"+str(p)+"_"+str(x))
        l.append("Strain_y_"+str(p)+"_"+str(x))
        l.append("Strain_xy_"+str(p)+"_"+str(x))
X.columns = l

# %%
X=X.reset_index(drop=True)
y=y.reset_index(drop=True)

# Filtro para ignorar testes nos quais a força no último time step é inferior à penúltima
index1=X[(X["Force_y_20"]-X["Force_y_19"]>0) & (X["Force_x_20"]-X["Force_x_19"]>0)].index
index1

# %%
# Aplicação de filtro ao dataframe original p/ extrair ensaios bons
X=X.iloc[index1]
y=y.iloc[index1]

display(X)
display(y)

# %%
# Set a random seed for reproducibility
random_state = 42
np.random.seed(random_state)

# Calculate the number of rows to delete we do this to get a "round number"
#rows_to_delete = len(X) - 4750
rows_to_delete = len(X) - 2600

# Randomly choose the indices to delete
indices_to_delete = np.random.choice(X.index, size=rows_to_delete, replace=False)

# Drop the selected indices from both X and y
X_reduced = X.drop(indices_to_delete)
y_reduced = y.drop(indices_to_delete)


X = X_reduced
y = y_reduced
# Display the updated DataFrames
display(X_reduced)
display(y_reduced)

# %%
# Scaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled=pd.DataFrame(X_scaled)

X=X.reset_index(drop=True)
y=y.reset_index(drop=True)

display(X)
display(y)

# %%
display(X_scaled)

# %%
import matplotlib.pyplot as plt

X_inverse = scaler.inverse_transform(X_scaled)

plt.subplot(2, 2, 1)
plt.hist(X_scaled[0], bins=20)
plt.subplot(2, 2, 2)
plt.hist(X["Force_x_1"], bins=20)
plt.subplot(2, 2, 3)
plt.hist(X_inverse[:, 0], bins=20)

# %%
# Separar dados para teste e treino
r = random.sample(range(0, len(X)), 260) #DEFENIR O NÚMERO DE SIMULAÇÔES PARA TESTAR
X_test = X_scaled.loc[r]
y_test = y.loc[r]
X_train = X_scaled.drop(r)
y_train = y.drop(r)

# %%
X_train.to_csv("/home/dmitreiro/WinVM/abaqus_datasets/x_train.csv", index=False)
y_train.to_csv("/home/dmitreiro/WinVM/abaqus_datasets/y_train.csv", index=False)

X_test.to_csv("/home/dmitreiro/WinVM/abaqus_datasets/x_test.csv", index=False)
y_test.to_csv("/home/dmitreiro/WinVM/abaqus_datasets/y_test.csv", index=False)


