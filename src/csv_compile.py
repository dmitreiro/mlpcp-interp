import os
import glob
import csv
import pandas as pd
import re
import time

mycsvdir = r"/home/dmitreiro/WinVM/abaqus_datasets/dataset"

# Get all the CSV files in that directory
csvfiles = glob.glob(os.path.join(mycsvdir, "*.csv"))

# Create empty DataFrames to store final results
final_x_file = r"/home/dmitreiro/WinVM/abaqus_datasets/X_cruciform.csv"
final_y_file = r"/home/dmitreiro/WinVM/abaqus_datasets/y_cruciform.csv"

# Start the timer
start_time = time.time()

# Write headers to the output files first
with open(final_x_file, "w", newline="") as x_out, open(
    final_y_file, "w", newline=""
) as y_out:
    x_writer = csv.writer(x_out)
    y_writer = csv.writer(y_out)

    # Write header row to final_y_file
    y_writer.writerow(["F", "G", "H", "L", "M", "N", "sigma0", "k", "n"])

    # Process files one at a time with a counter
    total_files = len(csvfiles)
    for index, cs in enumerate(csvfiles, start=1):
        # Read CSV file into DataFrame
        df = pd.read_csv(cs, header=None)
        # Write to output CSV file without keeping in memory
        df.to_csv(x_out, index=False, header=False)

        # Extract numeric values from file name
        matches = re.findall(r"\d+(?:\.\d+)?", cs)
        y_writer.writerow(matches)

        # Print progress
        print(f"Processed {index}/{total_files} files")

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
