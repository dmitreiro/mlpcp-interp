import numpy as np
import configparser
import csv
import os
import matplotlib.pyplot as plt

# Reading configuration file
config = configparser.ConfigParser()
config.read(r"config/config.ini")

# Accessing variables
DATA = config.get("Paths", "data_cleaned")
INT_P = config.get("Files", "centroids")
X_TRAIN = config.get("Files", "x_train")
PLOT = config.get("Paths", "resources")

GRIDS = [20, 30, 40]
METHODS = ["linear", "cubic", "multiquadric"]

def mesh_gen(n_points: int):
    """
    Function to define mesh grid for interpolation.
    The mesh is filtered to fit cruciform geometry domain.
    """
    # Define the grid
    x = np.linspace(0, 30, n_points)
    y = np.linspace(0, 30, n_points)
    xx, yy = np.meshgrid(x, y)
    points = np.column_stack([xx.flatten(), yy.flatten()])

    # Define the conditions for the region
    in_main_square = (points[:, 0] >= 0) & (points[:, 0] <= 30) & (points[:, 1] >= 0) & (points[:, 1] <= 30)
    out_excluded_square = ~((points[:, 0] > 15) & (points[:, 0] <= 30) & (points[:, 1] > 15) & (points[:, 1] <= 30))
    out_excluded_circle = ((points[:, 0] - 15)**2 + (points[:, 1] - 15)**2) >= 7**2
    in_fillet_circ_1 = ((points[:, 0] - 12.5)**2 + (points[:, 1] - 24.17)**2) <= 2.5**2
    in_fillet_circ_2 = ((points[:, 0] - 24.17)**2 + (points[:, 1] - 12.5)**2) <= 2.5**2
    out_square_1 = (points[:, 0] > 13.16) & (points[:, 0] < 15) & (points[:, 1] > 21.75) & (points[:, 1] < 24.17)
    out_square_2 = (points[:, 0] > 21.75) & (points[:, 0] < 24.17) & (points[:, 1] > 13.16) & (points[:, 1] < 15)

    # Keep points only within the circles for these squares
    square_1_cond = out_square_1 & in_fillet_circ_1
    square_2_cond = out_square_2 & in_fillet_circ_2

    # Combine all conditions
    final_region = (
        in_main_square
        & out_excluded_square
        & out_excluded_circle
        & ~out_square_1
        & ~out_square_2
    )
    final_region |= square_1_cond | square_2_cond

    # Extract the valid points
    valid_points = points[final_region]

    # Separate into x and y coordinates
    x_coords = valid_points[:, 0]  # All rows, first column
    y_coords = valid_points[:, 1]  # All rows, second column
    
    return x_coords, y_coords

# Importing centroid coordinates
x_centroids, y_centroids = [], []
with open(INT_P, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        x_centroids.append(float(row[0]))
        y_centroids.append(float(row[1]))

x_centroids = np.array(x_centroids)
y_centroids = np.array(y_centroids)

# Original exx values
x_ori_exx = []
with open(X_TRAIN, 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    row = next(reader)
    for i in range(len(row) - (int(len(row)/20) - 2), len(row), 3):
        x_ori_exx.append(float(row[i]))
x_ori_exx = np.array(x_ori_exx)

# Determine global color scale
global_min, global_max = x_ori_exx.min(), x_ori_exx.max()


# Iterate over grid-method combinations
for grid in GRIDS:
    x_grid, y_grid = mesh_gen(grid)
    for method in METHODS:
        interpolated_file = f"x_train_{grid}_{method}.csv"

        # Interpolated exx values
        x_int_exx = []
        with open(os.path.join(DATA, interpolated_file), 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            row = next(reader)
            for i in range(len(row) - (int(len(row)/20) - 2), len(row), 3):
                x_int_exx.append(float(row[i]))
        x_int_exx = np.array(x_int_exx)

        # Update global color scale
        global_min = min(global_min, x_int_exx.min())
        global_max = max(global_max, x_int_exx.max())

        # Create the plot
        plt.figure(figsize=(10, 8))
        scatter1 = plt.scatter(x_centroids, y_centroids, c=x_ori_exx, cmap='Reds', s=200, edgecolor='k',
                               vmin=global_min, vmax=global_max, label='Centroids', marker='^')
        scatter2 = plt.scatter(x_grid, y_grid, c=x_int_exx, cmap='Reds', s=70, edgecolor='k',
                               vmin=global_min, vmax=global_max, label=f'Interpolated ({method})')

        # Add colorbar
        cbar = plt.colorbar(scatter2, label='Epsilon_xx')
        plt.title(f'Grid {grid}, Method: {method}')

        # Set labels and legend
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.legend(loc='upper right')

        # Save plot
        plt.savefig(os.path.join(PLOT, f'plot_grid_{grid}_method_{method}.pdf'))
        plt.close()