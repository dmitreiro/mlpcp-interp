# %% Importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %% Grid generation
points = 300  # Total points in one axis
x = np.linspace(0, 30, int(np.sqrt(points)))
y = np.linspace(0, 30, int(np.sqrt(points)))
xx, yy = np.meshgrid(x, y)

# Combine x and y into a dataframe for clarity
grid_data = pd.DataFrame({
    'x': xx.flatten(),
    'y': yy.flatten()
})

grid_data

# %% Domain region plot

import numpy as np
import matplotlib.pyplot as plt

# Define the grid
n_points = 20
x = np.linspace(0, 30, n_points)
y = np.linspace(0, 30, n_points)
xx, yy = np.meshgrid(x, y)
points = np.column_stack([xx.flatten(), yy.flatten()])

# Define the conditions for the region
inside_main_square = (points[:, 0] >= 0) & (points[:, 0] <= 30) & (points[:, 1] >= 0) & (points[:, 1] <= 30)
outside_excluded_square = ~((points[:, 0] > 15) & (points[:, 0] < 30) & (points[:, 1] > 15) & (points[:, 1] < 30))
outside_excluded_circle = ((points[:, 0] - 15)**2 + (points[:, 1] - 15)**2) >= 7**2

# Conditions for the two new circles
inside_circle_1 = ((points[:, 0] - 12.5)**2 + (points[:, 1] - 24.17)**2) <= 2.5**2
inside_circle_2 = ((points[:, 0] - 24.17)**2 + (points[:, 1] - 12.5)**2) <= 2.5**2

# Define the conditions for the squares to remove
inside_square_1 = (points[:, 0] > 13.16) & (points[:, 0] < 15) & (points[:, 1] > 21.75) & (points[:, 1] < 24.17)
inside_square_2 = (points[:, 0] > 21.75) & (points[:, 0] < 24.17) & (points[:, 1] > 13.16) & (points[:, 1] < 15)

# Keep points only within the circles for these squares
square_1_condition = inside_square_1 & inside_circle_1
square_2_condition = inside_square_2 & inside_circle_2

# Combine all conditions
final_region_with_borders = (
    inside_main_square
    & outside_excluded_square
    & outside_excluded_circle
    & ~inside_square_1
    & ~inside_square_2
)
final_region_with_borders |= square_1_condition | square_2_condition

# Extract the valid points
valid_points_with_borders = points[final_region_with_borders]
print(f"Valid points: {len(valid_points_with_borders)}/{len(points)}")

# Plot the region
plt.figure(figsize=(8, 8))
plt.scatter(valid_points_with_borders[:, 0], valid_points_with_borders[:, 1], s=1, alpha=0.6)
plt.title("Domain region")
plt.xlabel("x (mm)")
plt.ylabel("y (mm)")
plt.grid(True)
plt.axis('equal')
plt.show()
