import configparser
import glob
import os
import csv
import pandas as pd
import re
import time

# Reading configuration file
config = configparser.ConfigParser()
config.read(r"config/config.ini")

# Accessing variables
MYCSVDIR = config.get("Paths", "data_raw")
EL = config.get("Files", "elements")
ND = config.get("Files", "nodes")
INT_P = config.get("Files", "integration_points")

# Start the timer
start_time = time.time()

# Checking for previous data files
if os.path.isfile(INT_P):
    os.remove(INT_P)

with open(EL, 'r') as f_elem, open(ND, 'r') as f_nodes, open(INT_P, 'wb') as f_intp:
    f_elem_r = csv.reader(f_elem)
    f_nodes_r = csv.reader(f_nodes)
    f_intp_w = csv.writer(f_intp)
    coords = []

    for element in f_elem_r:
        el_coords = []
        el_x = []
        el_y = []
        el_z = []
        for node in element:
            el_x.append(f_nodes_r[(int(node)-1)*3])
            el_y.append(f_nodes_r[(int(node)-1)*3+1])
            el_z.append(f_nodes_r[(int(node)-1)*3+2])

        x_val = sum(el_x)/len(el_x)
        y_val = sum(el_y)/len(el_y)
        z_val = sum(el_z)/len(el_z)
        el_coords.extend([x_val, y_val, z_val])
        coords.append(el_coords)
    
    f_intp_w.writerows(coords)


# End the timer and calculate elapsed time
end_time = time.time()
elapsed_time = end_time - start_time

# Convert elapsed time to minutes and seconds
elapsed_minutes = int(elapsed_time // 60)
elapsed_seconds = int(elapsed_time % 60)

# Print total elapsed time in "minutes:seconds" format
print(f"Finished in {elapsed_minutes}:{elapsed_seconds:02d} minutes.")
