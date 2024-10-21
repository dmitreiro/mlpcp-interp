import numpy as np
import glob
import os
import csv
import pandas as pd
import re
import time

# Global variables
MYCSVDIR = r"/home/dmitreiro/WinVM/abaqus_datasets/dataset"
X_CRUCIFORM = r"/home/dmitreiro/WinVM/abaqus_datasets/x_cruciform.csv"
Y_CRUCIFORM = r"/home/dmitreiro/WinVM/abaqus_datasets/y_cruciform.csv"
X_BUFF_TSHOLD = 100

# Start the timer
start_time = time.time()

# Get all the csv files in that directory (assuming they have the extension .csv)
csvfiles = glob.glob(os.path.join(MYCSVDIR, "*.csv"))
total_files = len(csvfiles)

# Checking for previous data files
if os.path.isfile(X_CRUCIFORM):
    os.remove(X_CRUCIFORM)
if os.path.isfile(Y_CRUCIFORM):
    os.remove(Y_CRUCIFORM)

final_rows = []
final_y = []

for index, cs in enumerate(csvfiles, start=1):
    rows = []
    with open(cs, "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)
    rows = [x for f in rows for x in f]
    final_rows.append(rows)
    final_y.append(re.findall(r"\d+(?:\.\d+)?", cs))

    # Print progress
    print(f"Processed {index}/{total_files} files")

    # If buffer x file has more than 100 lines, it is dumped
    if len(final_rows) == X_BUFF_TSHOLD:
        # Print progress
        print(f"Dumping x buffer file")
        p = pd.DataFrame(final_rows)
        p.to_csv(X_CRUCIFORM, mode="a", header=False, index=False)
        final_rows = []

print("Dataframe x and y data")
p = pd.DataFrame(final_rows)
pf = pd.DataFrame(final_y, columns=["F", "G", "H", "L", "M", "N", "sigma0", "k", "n"])

print("Writting final x and y data.")
p.to_csv(X_CRUCIFORM, mode="a", header=False, index=False)
pf.to_csv(Y_CRUCIFORM)

# End the timer and calculate elapsed time
end_time = time.time()
elapsed_time = end_time - start_time

# Convert elapsed time to minutes and seconds
elapsed_minutes = int(elapsed_time // 60)
elapsed_seconds = int(elapsed_time % 60)

# Print total elapsed time in "minutes:seconds" format
print(
    f"Finished processing {total_files} files in {elapsed_minutes}:{elapsed_seconds:02d} minutes."
)
