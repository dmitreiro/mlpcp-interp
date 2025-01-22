# %% Importing libraries
import configparser
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Reading configuration file
config = configparser.ConfigParser()
config.read(r"config/config.ini")

# Accessing variables
CENT = config.get("Files", "centroids")
PLOTS = config.get("Paths", "resources")

# %% Domain region plot

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


# Load the centroids
centroids = pd.read_csv(CENT, header=None)  # Assuming no header
centroid_x = centroids.iloc[:, 0]  # First column
centroid_y = centroids.iloc[:, 1]  # Second column

# Generate the coordinates for different grid sizes
grid_sizes = [20, 30, 40]
coords = [mesh_gen(n_points) for n_points in grid_sizes]
print(f"Mesh grid 20: {len(coords[0][0])}/{grid_sizes[0]*grid_sizes[0]} points ({(len(coords[0][0])/(grid_sizes[0]*grid_sizes[0]))*100}%)")
print(f"Mesh grid 30: {len(coords[1][0])}/{grid_sizes[1]*grid_sizes[1]} points ({(len(coords[1][0])/(grid_sizes[1]*grid_sizes[1]))*100}%)")
print(f"Mesh grid 40: {len(coords[2][0])}/{grid_sizes[2]*grid_sizes[2]} points ({(len(coords[2][0])/(grid_sizes[2]*grid_sizes[2]))*100}%)")

# Create the plots
fig, axes = plt.subplots(1, 3, figsize=(18, 6))  # 1 row, 3 columns of subplots

# Plot each grid
for ax, (n_points, (x_coords, y_coords)) in zip(axes, zip(grid_sizes, coords)):
    # Scatter plot for the mesh grid points
    ax.scatter(x_coords, y_coords, color="blue", s=2, label="Grid")
    # Scatter plot for the centroids
    ax.scatter(centroid_x, centroid_y, color="red", s=2, label="Centroids")
    ax.set_title(f"Grid: {n_points}x{n_points}")
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.legend()  # Add a legend
    ax.grid(True)

# Adjust layout and show the combined plots
plt.tight_layout()

# saves plot to external file
plt.savefig(os.path.join(PLOTS, "grid_1x3_compilation.pdf"))

# Now display each subplot individually
for i, (n_points, (x_coords, y_coords)) in enumerate(zip(grid_sizes, coords), start=1):
    plt.figure(figsize=(8, 8))  # Create a new figure for each individual plot
    # Scatter plot for the mesh grid points
    plt.scatter(x_coords, y_coords, color="blue", s=2, label="Grid")
    # Scatter plot for the centroids
    plt.scatter(centroid_x, centroid_y, color="red", s=2, label="Centroids")
    plt.title(f"Grid: {n_points}x{n_points}")
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.legend()  # Add a legend
    plt.grid(True)

    # saves plot to external file
    plt.savefig(os.path.join(PLOTS, f"grid_{n_points}x{n_points}.pdf"))
