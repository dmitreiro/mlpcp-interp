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
    """Generate mesh grid and filter points for cruciform geometry."""
    x = np.linspace(0, 30, n_points)
    y = np.linspace(0, 30, n_points)
    xx, yy = np.meshgrid(x, y)
    points = np.column_stack([xx.flatten(), yy.flatten()])

    in_main_square = (points[:, 0] >= 0) & (points[:, 0] <= 30) & (points[:, 1] >= 0) & (points[:, 1] <= 30)
    out_excluded_square = ~((points[:, 0] > 15) & (points[:, 0] <= 30) & (points[:, 1] > 15) & (points[:, 1] <= 30))
    out_excluded_circle = ((points[:, 0] - 15)**2 + (points[:, 1] - 15)**2) >= 7**2
    in_fillet_circ_1 = ((points[:, 0] - 12.5)**2 + (points[:, 1] - 24.17)**2) <= 2.5**2
    in_fillet_circ_2 = ((points[:, 0] - 24.17)**2 + (points[:, 1] - 12.5)**2) <= 2.5**2
    out_square_1 = (points[:, 0] > 13.16) & (points[:, 0] < 15) & (points[:, 1] > 21.75) & (points[:, 1] < 24.17)
    out_square_2 = (points[:, 0] > 21.75) & (points[:, 0] < 24.17) & (points[:, 1] > 13.16) & (points[:, 1] < 15)

    square_1_cond = out_square_1 & in_fillet_circ_1
    square_2_cond = out_square_2 & in_fillet_circ_2

    final_region = (
        in_main_square
        & out_excluded_square
        & out_excluded_circle
        & ~out_square_1
        & ~out_square_2
    )
    final_region |= square_1_cond | square_2_cond

    valid_points = points[final_region]
    return xx, yy, final_region.reshape(xx.shape), valid_points

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
    xx, yy, mask, valid_points = mesh_gen(grid)
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

        # Create the plots
        fig, ax = plt.subplots(1, 2, figsize=(18, 8))

        # Plot 1: Interpolated data without centroids
        z_data = np.full(xx.shape, np.nan)  # Initialize with NaN
        z_data[mask] = x_int_exx  # Place valid data into masked regions

        mesh1 = ax[0].pcolormesh(xx, yy, z_data, cmap='jet', shading='auto',
                                 vmin=global_min, vmax=global_max)
        ax[0].set_title(f'Grid {grid}, {method} method')
        ax[0].set_xlabel('X coordinate (mm)')
        ax[0].set_ylabel('Y coordinate (mm)')
        cbar1 = fig.colorbar(mesh1, ax=ax[0], label='Epsilon_xx')

        # Plot 2: Centroids represented with imshow
        z_centroids = np.full(xx.shape, np.nan)
        for x, y, val in zip(x_centroids, y_centroids, x_ori_exx):
            idx_x = np.abs(xx[0, :] - x).argmin()
            idx_y = np.abs(yy[:, 0] - y).argmin()
            z_centroids[idx_y, idx_x] = val

        img = ax[1].imshow(z_centroids, cmap='jet', origin='lower',
                           vmin=global_min, vmax=global_max)   
        
        ax[1].set_title(f'Centroids')
        ax[1].set_xlabel('X coordinate (mm)')
        ax[1].set_ylabel('Y coordinate (mm)')
        cbar2 = fig.colorbar(img, ax=ax[1], label='Epsilon_xx')


        # Save plot
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT, f'interp_pcolor_{grid}_{method}.pdf'))
        plt.close()
