from abaqus import *
from abaqusConstants import *

import __main__
import os
import csv
import time
import numpy
import regionToolset
import displayGroupMdbToolset
import mesh
import displayGroupOdbToolset

# Define path for data
current_dir = os.getcwd()
MYCSVDIR = os.path.join(current_dir, '..', '..', 'data', 'raw')
MYCSVDIR = os.path.normpath(MYCSVDIR)

overwrite=True

# Start the timer
start_time = time.time()

odb_Path = 'Job-1.odb'
cruci_ODB = session.openOdb(name=odb_Path)

frames = len(cruci_ODB.steps['Step-1'].frames)                                                          #Number of Frames
nodes = len(cruci_ODB.steps['Step-1'].frames[0].fieldOutputs['S'].values[0].instance.nodes)             #Number of Nodes
elements = len(cruci_ODB.steps['Step-1'].frames[0].fieldOutputs['S'].values[0].instance.elements)       #Number of Elements
no_of_field_output_ut_values = len(cruci_ODB.steps['Step-1'].frames[0].fieldOutputs['S'].values)        #Field Output Values

# Define CSV file path
csv_nodes = r'{}\nodes.csv'.format(MYCSVDIR)
csv_elements = r'{}\elements.csv'.format(MYCSVDIR)

# Open a .csv file to write the results
with open(csv_nodes, 'wb') as f_nodes:
    nodes_writer = csv.writer(f_nodes)
    
    # Create a list to store all rows of data
    nodes_all_data = []
    
    # Loop for nodes
    for frame in range(frames):
        nodes_data = []
        for node in range(nodes):
            n_cords = cruci_ODB.steps['Step-1'].frames[frame].fieldOutputs['COORD'].values[node].data
            for cord in n_cords:
                nodes_data.extend([cord])

        # Append the row data to all_data
        nodes_all_data.append(nodes_data)

    # Use writerows() to write all_data to the CSV file in bulk
    nodes_writer.writerows(nodes_all_data)
    
with open(csv_elements, 'wb') as f_elements:
    el_writer = csv.writer(f_elements)

    # Create a list to store all rows of data
    el_all_data = []

    # Loop for elements
    for el in range(elements):
        el_data = []
        el_nodes = cruci_ODB.steps['Step-1'].frames[0].fieldOutputs['S'].values[0].instance.elements[el].connectivity
        for n in el_nodes:
            el_data.extend([n])

        # Append the row data to all_data
        el_all_data.append(el_data)

    # Use writerows() to write all_data to the CSV file in bulk
    el_writer.writerows(el_all_data)

#Close the ODB file
cruci_ODB.close()

# End the timer and calculate elapsed time
end_time = time.time()
elapsed_time = end_time - start_time

# Convert elapsed time to minutes and seconds
elapsed_minutes = int(elapsed_time // 60)
elapsed_seconds = int(elapsed_time % 60)

# Print total elapsed time in "minutes:seconds" format
print("Finished in {}:{:02d} minutes.".format(elapsed_minutes, elapsed_seconds))