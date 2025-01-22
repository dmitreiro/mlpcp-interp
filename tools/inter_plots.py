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
    for i in range(len(row) - (int(len(row) / 20) - 2), len(row), 3):
        x_ori_exx.append(float(row[i]))
x_ori_exx = np.array(x_ori_exx)

# Determine global color scale
global_min, global_max = x_ori_exx.min(), x_ori_exx.max()

# Iterate over grid-method combinations
for grid in GRIDS:
    x_coords, y_coords = mesh_gen(grid)
    for method in METHODS:
        interpolated_file = f"x_train_{grid}_{method}.csv"

        # Interpolated exx values
        x_int_exx = []
        with open(os.path.join(DATA, interpolated_file), 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            row = next(reader)
            for i in range(len(row) - (int(len(row) / 20) - 2), len(row), 3):
                x_int_exx.append(float(row[i]))
        x_int_exx = np.array(x_int_exx)

        # Update global color scale
        global_min = min(global_min, np.nanmin(x_int_exx))
        global_max = max(global_max, np.nanmax(x_int_exx))

        # Create the plots with constrained_layout enabled
        fig, ax = plt.subplots(1, 2, figsize=(18, 8), 
                               gridspec_kw={'width_ratios': [1, 1], 'wspace': 0.1},
                               constrained_layout=True)

        # define element size according to grid
        match grid:
            case 20:
                size = 900
            case 30:
                size = 450
            case 40:
                size = 250
            case _:
                size = 50
        
        # Plot 1: Interpolated data represented with scatter
        scatter1 = ax[0].scatter(x_coords, y_coords, c=x_int_exx, cmap='jet', s=size, alpha=0.9, edgecolors='none', vmin=global_min, vmax=global_max)
        ax[0].set_title(f'{grid}x{grid}, {method}')
        ax[0].set_xlabel('X (mm)')
        ax[0].set_ylabel('Y (mm)')
        # cbar1 = fig.colorbar(scatter1, ax=ax[0], label=r'$\varepsilon_{xx}$')

        # Plot 2: Centroids represented with scatter
        scatter2 = ax[1].scatter(x_centroids, y_centroids, c=x_ori_exx, cmap='jet', s=450, alpha=0.9, edgecolors='none', vmin=global_min, vmax=global_max)
        ax[1].set_title(f'Centroids')
        ax[1].set_xlabel('X (mm)')
        ax[1].set_ylabel('Y (mm)')
        # cbar2 = fig.colorbar(scatter, ax=ax[1], label=r'$\varepsilon_{xx}$')

        # Add a single shared colorbar for both plots
        cbar = fig.colorbar(scatter2, ax=ax, label=r'$\varepsilon_{xx}$')

        # saves and closes plot
        plt.savefig(os.path.join(PLOT, f'interp_{grid}_{method}.pdf'))
        plt.close()
