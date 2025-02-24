import pandas as pd
import numpy as np
import configparser
import os
import matplotlib.pyplot as plt

from sklearn.metrics import r2_score, mean_absolute_error

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

plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath}",
    "axes.facecolor": (1,1,1),
    "figure.facecolor": (1,1,1),
    # "font.family": "serif",
    "font.family": "Palatino",
    "font.size": 8,
    "legend.fontsize": 6,
    "legend.edgecolor": "black"
})

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
    # rows = (num_params // 3) + (1 if num_params % 3 else 0)
    # fig, axes = plt.subplots(rows, 3, figsize=(18, 6 * rows))
    # axes = axes.flatten()  # Flatten axes array for easy indexing

    fig_width_in = 13.7 / 2.54  # Convert cm to inches
    subplot_size = fig_width_in / 3  # Keep subplots square
    num_params = 7  # Number of subplots

    rows = (num_params // 3) + (1 if num_params % 3 else 0)
    fig_height_in = rows * subplot_size  # Maintain square aspect ratio
    fig, axes = plt.subplots(rows, 3, figsize=(fig_width_in, fig_height_in))
    axes = axes.flatten()

    # for i in range(num_params, len(axes)):  # Hide extra subplots
    #     fig.delaxes(axes[i])
    
    for ax in axes[:num_params]:  # Only set for used subplots
        ax.set_aspect("equal", adjustable="box")

    # Adjust subplot spacing
    plt.subplots_adjust(
        left=0.05,   # Adjust left margin
        right=1.02,  # Adjust right margin
        top=0.95,    # Adjust top margin
        bottom=0.08, # Adjust bottom margin
        wspace=0.1,  # Increase horizontal space between plots
        hspace=0.7   # Increase vertical space between plots
    )

    # labels for each subplot
    letters = [
        r"\textbf{(a)}", r"\textbf{(b)}", r"\textbf{(c)}",
        r"\textbf{(d)}", r"\textbf{(e)}", r"\textbf{(f)}",
        r"\textbf{(g)}"
    ]
    positions = [
        (0.10, 0.98), (0.435, 0.98), (0.768, 0.98),
        (0.10, 0.64), (0.435, 0.64), (0.768, 0.64),
        (0.10, 0.31)
    ]

    for letter, (x_pos, y_pos) in zip(letters, positions):
        fig.text(x_pos, y_pos, letter,
                verticalalignment="top", horizontalalignment="left")
        
    config = {
        "y_labels": {"F": r"$F$",
                     "G": r"$G$",
                     "H": r"$H$",
                     "N": r"$N$",
                     "sigma0": r"$\sigma_{0}$",
                     "k": r"$K$",
                     "n": r"$n$"},
    }

    try:
        # Plot each parameter in its designated subplot
        for idx, column in enumerate(columns_to_plot):
            ax = axes[idx]
            ax.scatter(
                y_test[column], y_pred[column],
                s=0.3, color='black'#, label=f"Parameter: {column}"
            )
            ax.plot(
                [y_test[column].min(), y_test[column].max()],
                [y_test[column].min(), y_test[column].max()],
                color='red',
                linewidth=0.8
                # label='Ideal Line'
            )

            # Calculate R^2 and MAE
            r2 = r2_score(y_test[column], y_pred[column])
            mae = mean_absolute_error(y_test[column], y_pred[column])

            # Add R^2 and MAE as text in the top left corner
            ax.text(
                0.05, 0.95,
                # f"$R^2$: {r2:.3f}\nMAE: {mae:.3f}",
                f"$R^2$: {r2:.3f}",
                transform=ax.transAxes,
                fontsize=6,
                verticalalignment='top',
                # bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white')
            )

            # ax.set_xlabel(f"{column} simulated")
            # ax.set_ylabel(f"{column} predicted")
            ax.set_xlabel(f"{config['y_labels'].get(column, column)} test")
            ax.set_ylabel(f"{config['y_labels'].get(column, column)} predicted")
            #ax.legend(loc='upper left', fontsize='small')
            #ax.set_title(f"{column}")
            ax.set_aspect("equal")  # force equal scaling
            ax.autoscale()
            # x_min, x_max = ax.get_xlim()
            # y_min, y_max = ax.get_ylim()
            # num_ticks = 4
            # x_ticks = np.linspace(x_min, x_max, num_ticks)  # X-axis ticks
            # y_ticks = np.linspace(y_min, y_max, num_ticks)  # Y-axis ticks
            # ax.set_xticks(x_ticks)
            # ax.set_yticks(y_ticks)
            ax.locator_params(axis="x", nbins=4)
            ax.locator_params(axis="y", nbins=4)
            

        # Hide any unused subplots
        for idx in range(num_params, len(axes)):
            fig.delaxes(axes[idx])

        # Adjust layout and save the plot
        # plt.tight_layout()
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
