# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 14:33:07 2022

@author: kevin
"""
import numpy as np
import glob
import os
import csv
import pandas as pd 
import re

mycsvdir = r'C:\Users\gambo\Desktop\CVs'


# get all the csv files in that directory (assuming they have the extension .csv)
csvfiles = glob.glob(os.path.join(mycsvdir, '*.csv'))
final_rows = []
final_y = []
#print(len(csvfiles))
for cs in csvfiles:
    rows = []
    with open(cs,"r") as file:
        csvreader=csv.reader(file)
        for row in csvreader:
            rows.append(row)
    rows = [x for f in rows for x in f]
    final_rows.append(rows)
    final_y.append(re.findall(r'\d+(?:\.\d+)?',cs))
    
    
print("1")
p = pd.DataFrame(final_rows)
print("1")
pf=pd.DataFrame(final_y,columns=["F","G","H","L", "M", "N","sigma0","k","n"])
print("1")
p.to_csv(r'C:\Users\gambo\Desktop\append_csvs\X_cruciform.csv')
pf.to_csv(r'C:\Users\gambo\Desktop\append_csvs\y_cruciform.csv')

