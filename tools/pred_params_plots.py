import pandas as pd
import numpy as np
import configparser
import os
import matplotlib.pyplot as plt

# Reading configuration file
config = configparser.ConfigParser()
config.read(r"config/config.ini")

# Folder paths from config
DATA = config.get("Paths", "data_cleaned")
Y_TEST = config.get("Files", "y_test")
PLOT = config.get("Paths", "resources")

# Paths and configurations (modify as needed)
GRIDS = [20, 30, 40]
METHODS = ["linear", "cubic", "multiquadric"]

def generate_comparison_plots(grid, method, test_method):
    """
    Generates a comparison plot with subplots for selected parameters
    and saves it to a PDF file.
    
    Parameters:
        grid: Grid number
        method: Method used
        test_method: Test method used
    """
    # File paths for the predicted and original y data
    pred_params_path = os.path.join(DATA, f"y_pred_{grid}_{method}_{test_method}.csv")
    y_test_path = Y_TEST  # Original test data

    try:
        # Load both files with headers
        print(f"Loading predicted data from {pred_params_path}")
        y_pred = pd.read_csv(pred_params_path, header=0)  # Load with header
        
        print(f"Loading original data from {y_test_path}")
        y_test = pd.read_csv(y_test_path, header=0)  # Load with header
        
        # Replace the header of y_pred with the correct header from y_test
        y_pred.columns = y_test.columns
        print("Replaced y_pred header with y_test header.")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Ensure dimensions match
    if y_pred.shape != y_test.shape:
        print(f"Dimension mismatch: y_pred shape {y_pred.shape}, y_test shape {y_test.shape}")
        return

    # Skip 4th and 5th parameters
    columns_to_plot = [col for i, col in enumerate(y_test.columns) if i not in (3, 4)]
    num_params = len(columns_to_plot)

    # Determine subplot grid layout
    rows = (num_params // 3) + (1 if num_params % 3 else 0)
    fig, axes = plt.subplots(rows, 3, figsize=(18, 6 * rows))
    axes = axes.flatten()  # Flatten axes array for easy indexing

    try:
        # Plot each parameter in its designated subplot
        for idx, column in enumerate(columns_to_plot):
            ax = axes[idx]
            ax.scatter(
                y_test[column], y_pred[column],
                label=f"Parameter: {column}", s=10, color='black'
            )
            ax.plot(
                [y_test[column].min(), y_test[column].max()],
                [y_test[column].min(), y_test[column].max()],
                color='red', label='Ideal Line'
            )

            ax.set_xlabel("Original (y_test)")
            ax.set_ylabel("Predicted (y_pred)")
            ax.legend(loc='upper left', fontsize='small')
            ax.set_title(f"Comparison for {column}")

        # Hide any unused subplots
        for idx in range(num_params, len(axes)):
            fig.delaxes(axes[idx])

        # Adjust layout and save the plot
        plt.tight_layout()
        plot_path = os.path.join(PLOT, f"y_pred_plot_{grid}_{method}_{test_method}.pdf")
        plt.savefig(plot_path)
        plt.close()
        print(f"Plot saved to {plot_path}")
    except Exception as e:
        print(f"Error generating plot: {e}")


# Iterate over grid, method, and test_method combinations
for grid in GRIDS:
    for method in METHODS:
        for test_method in METHODS:
            generate_comparison_plots(grid, method, test_method)
