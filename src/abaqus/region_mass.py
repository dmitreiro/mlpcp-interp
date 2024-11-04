from abaqus import *
from abaqusConstants import *
import regionToolset

import os
import csv

# Define path for data
current_dir = os.getcwd()
MYCSVDIR = os.path.join(current_dir, '..', '..', 'data', 'raw')
MYCSVDIR = os.path.normpath(MYCSVDIR)

overwrite=True

a = mdb.models['Model-1'].rootAssembly
elements = a.instances['Part-1-1'].elements

# Define CSV file path
csv_centroids = r'{}\centroids.csv'.format(MYCSVDIR)

# Open a .csv file to write the results
with open(csv_centroids, 'wb') as f_cent:
    cent_writer = csv.writer(f_cent)
    
    # Create a list to store all rows of data
    centroid_list = []
    
    # Loop for elements
    for i, el in enumerate(elements):
        region = regionToolset.Region(elements=elements[i:i+1])
        properties = a.getMassProperties(regions=region)

        # Append the row data
        centroid_list.append(list(properties['volumeCentroid']))

    # Use writerows() to write all_data to the CSV file in bulk
    cent_writer.writerows(centroid_list)