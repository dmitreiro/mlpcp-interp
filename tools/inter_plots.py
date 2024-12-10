import numpy as np
import configparser
import csv
import matplotlib.pyplot as plt

# Reading configuration file
config = configparser.ConfigParser()
config.read(r"config/config.ini")

# Accessing variables
#DATA = config.get("Paths", "data_cleaned")
INT_P = config.get("Files", "centroids")
X_TRAIN = config.get("Files", "x_train")

GRIDS = [20, 30, 40]
METHODS = ["quintic", "gaussian", "inverse_multiquadric"]

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

x_grid, y_grid = mesh_gen(30)

# Importing x,y coordinates of element's reduced integration points (centroids) into separate arrays.
# Initialize arrays
x = []
y = []
# Read the CSV file
with open(INT_P, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        x.append(row[0])  # First column
        y.append(row[1])  # Second column

# Convert to float array
x = np.array(x, dtype=float)
y = np.array(y, dtype=float)

# Get exx values from original train dataset
with open(X_TRAIN, 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    row = next(reader)
    x_ori_exx = []
    # print(int(len(row)-(len(row)/20-2)))
    for i in range(len(row)-(int(len(row)/20)-2), len(row), 3):
        x_ori_exx.append(row[i])


# Get exx values from interpolated train dataset
with open("/home/dmitreiro/MLCCM/data/cleaned/x_train_30_inverse_multiquadric.csv", 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    row = next(reader)
    x_int_exx= []
    # print(int(len(row)-(len(row)/20-2)))
    for i in range(len(row)-(int(len(row)/20)-2), len(row), 3):
        x_int_exx.append(row[i])

# Ensure both are float
x_ori_exx = np.array(x_ori_exx, dtype=float)
x_int_exx = np.array(x_int_exx, dtype=float)

# Combine values to determine the global color scale
all_values = np.concatenate([x_ori_exx, x_int_exx])  # Combine both datasets
ori_min, ori_max = x_ori_exx.min(), x_ori_exx.max()
int_min, int_max = x_int_exx.min(), x_int_exx.max()
vmin, vmax = all_values.min(), all_values.max()  # Global min and max

# Create the plot
plt.figure(figsize=(12, 10))

scatter1 = NotImplemented
scatter2 = NotImplemented

# Plot the first set of points
#scatter1 = plt.scatter(x, y, c=x_ori_exx, cmap='Reds', s=50, edgecolor='k', vmin=ori_min, vmax=ori_max, label='Centroids')
# print(xx.shape, yy.shape, x_cent_exx.shape)

# Plot the second set of points
scatter2 = plt.scatter(x_grid, y_grid, c=x_int_exx, cmap='Reds', s=50, edgecolor='k', vmin=int_min, vmax=int_max, label='Int. points')

# Add a single colorbar for both sets
if scatter1 != NotImplemented and scatter2 != NotImplemented:
    cbar = plt.colorbar(scatter1, label='Original Epsilon_xx')
    cbar2 = plt.colorbar(scatter2, label='Interpolated Epsilon_xx')
    plt.title('Original and interpolated data comparison')
elif scatter1 != NotImplemented:
    cbar = plt.colorbar(scatter1, label='Original Epsilon_xx')
    plt.title('Original data plot')
elif scatter2 != NotImplemented:
    cbar = plt.colorbar(scatter2, label='Interpolated Epsilon_xx')
    plt.title('Interpolated data plot')

# Set labels and title
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')

# Add a legend
# plt.legend(loc='upper right')

# Show the plot
plt.show()
