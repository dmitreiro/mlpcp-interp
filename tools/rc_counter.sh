#!/bin/bash

# Check if a file argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <csv_file>"
    exit 1
fi

# Assign the file argument to a variable
csv_file="$1"

# Check if the file exists
if [ ! -f "$csv_file" ]; then
    echo "Error: File '$csv_file' does not exist."
    exit 1
fi

# Count rows
row_count=$(awk 'END {print NR}' "$csv_file")

# Count columns by checking the first row
column_count=$(head -n 1 "$csv_file" | awk -F',' '{print NF}')

# Print the result
echo "Size: $row_count, $column_count"
