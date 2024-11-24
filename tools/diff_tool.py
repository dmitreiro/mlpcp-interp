"""
Tool to check differences between manually calculated integration points and abaqus centroids.
"""

import configparser
import csv
import numpy as np
from sklearn import metrics
import time

# Reading configuration file
config = configparser.ConfigParser()
config.read(r"config/config.ini")

# Accessing variables
MYCSVDIR = config.get("Paths", "data_raw")
INTP = config.get("Files", "integration_points")
CENT = config.get("Files", "centroids")

# Start the timer
start_time = time.time()

with open(INTP, 'r') as f_intp, open(CENT, 'r') as f_cent:
    f_intp_r = csv.reader(f_intp)
    f_cent_r = csv.reader(f_cent)
    intp_data = []
    cent_data = []
    diff_data = []

    for row_intp, row_cent in zip(f_intp_r, f_cent_r):
        for intp, cent in zip(row_intp, row_cent):
            intp_data.append(float(intp))
            cent_data.append(float(cent))
            diff_data.append(float(intp)-float(cent))

print(f"Max diff value: {max(diff_data)}")
print(f"Mean diff value: {np.mean(diff_data)}")
print(f"MAE: {metrics.mean_absolute_error(cent_data, intp_data)}")
print(f"MAPE: {metrics.mean_absolute_percentage_error(cent_data, intp_data)}")

# End the timer and calculate elapsed time
end_time = time.time()
elapsed_time = end_time - start_time

# Convert elapsed time to minutes and seconds
elapsed_minutes = int(elapsed_time // 60)
elapsed_seconds = int(elapsed_time % 60)

# Print total elapsed time in "minutes:seconds" format
print(f"Finished in {elapsed_minutes}:{elapsed_seconds:02d} minutes.")
