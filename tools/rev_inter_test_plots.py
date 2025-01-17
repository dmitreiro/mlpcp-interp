import configparser
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Reading configuration file
config = configparser.ConfigParser()
config.read(r"config/config.ini")

# Accessing variables
TST_METRICS = config.get("Files", "test_metrics")
PLOT = config.get("Paths", "resources")
DATA = config.get("Paths", "data_cleaned")

# path to get data
REV_METRICS = os.path.join(DATA, "inverse_prediction_metrics.csv")

# path to save plots
TST_SIMPLE_BYMETHOD_PLOT = os.path.join(PLOT, "tst_metrics_simple_bymethod_plot.pdf")
TST_SIMPLE_BYGRID_PLOT = os.path.join(PLOT, "tst_metrics_simple_bygrid_plot.pdf")
TST_CROSS_PLOT = os.path.join(PLOT, "tst_metrics_cross_plot.pdf")
REV_PLOT = os.path.join(PLOT, "inv_inter_test_plots.pdf")

def tst_simple_bymethod_plot():
    # Load the data from the CSV file
    df = pd.read_csv(TST_METRICS)

    # filters data
    filtered_df = df[df['model_method'] == df['test_method']]

    # choose color pallete
    palette = sns.color_palette("tab10")[:3]

    # Set up the plotting grid
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)
    fig.canvas.manager.set_window_title("By method plot")

    # Define metrics and titles
    metrics = ["r2", "mae", "mape"]
    titles = ["R² (Goodness of Fit)", "MAE (Mean Absolute Error)", "MAPE (Mean Absolute Percentage Error)"]
    y_limits = [(0.95, 1.02), (0, 2), (0, 0.03)]  # Custom y-axis limits

    # Create a plot for each metric
    for ax, metric, title, ylim in zip(axes, metrics, titles, y_limits):
        # Use seaborn's barplot for each metric
        sns.barplot(
            data=filtered_df,
            x="model_method",
            y=metric,
            hue="grid",
            ax=ax,
            palette=palette
        )
        ax.set_title(title)
        ax.set_xlabel("Model Method")
        ax.set_ylabel(metric.upper())
        ax.legend(title="grid", loc="upper right")
        ax.set_ylim(ylim)  # Apply custom y-axis limits
        
        # Add grid lines corresponding to y-axis ticks
        ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    # Adjust layout
    plt.tight_layout()

    # saves plot to external file
    plt.savefig(TST_SIMPLE_BYMETHOD_PLOT, format="pdf")

    # shows plot
    plt.show()

def tst_simple_bygrid_plot():
    # Load the data from the CSV file
    df = pd.read_csv(TST_METRICS)

    # filters data
    filtered_df = df[df['model_method'] == df['test_method']]
    # filtered_df = filtered_df[df['grid'] == 20]

    # choose color pallete
    palette = sns.color_palette("tab10")[:3]

    # Set up the plotting grid
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)
    fig.canvas.manager.set_window_title("By grid plot")

    # Define metrics and titles
    metrics = ["r2", "mae", "mape"]
    titles = ["R² (Goodness of Fit)", "MAE (Mean Absolute Error)", "MAPE (Mean Absolute Percentage Error)"]
    y_limits = [(0.95, 1.02), (0, 2), (0, 0.03)]  # Custom y-axis limits

    # Create a plot for each metric
    for ax, metric, title, ylim in zip(axes, metrics, titles, y_limits):
        # Use seaborn's barplot for each metric
        sns.barplot(
            data=filtered_df,
            # x="model_method",
            x="grid",
            y=metric,
            hue="model_method",
            ax=ax,
            palette=palette
        )
        ax.set_title(title)
        ax.set_xlabel("grid")
        ax.set_ylabel(metric.upper())
        ax.legend(title="model_method", loc="upper right")
        ax.set_ylim(ylim)  # Apply custom y-axis limits
        
        # Add grid lines corresponding to y-axis ticks
        ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    # Adjust layout
    plt.tight_layout()

    # saves plot to external file
    plt.savefig(TST_SIMPLE_BYGRID_PLOT, format="pdf")

    # shows plot
    plt.show()

def rev_interp_plt():
    # Load the data from the CSV file
    df = pd.read_csv(REV_METRICS)

    # choose color pallete
    palette = sns.color_palette("tab10")[:3]

    # Set up the plotting grid
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)
    fig.canvas.manager.set_window_title("O que eu quiser")

    # Define metrics and titles
    metrics = ["r2", "mae", "mape"]
    titles = ["R² (Goodness of Fit)", "MAE (Mean Absolute Error)", "MAPE (Mean Absolute Percentage Error)"]
    y_limits = [(0.95, 1.02), (0, 0.1), (0, 1)]  # Custom y-axis limits

    # Create a plot for each metric
    for ax, metric, title, ylim in zip(axes, metrics, titles, y_limits):
        # Use seaborn's barplot for each metric
        sns.barplot(
            data=df,
            x="method",
            y=metric,
            hue="grid",
            ax=ax,
            palette=palette
            )
        ax.set_title(title)
        ax.set_xlabel("Method")
        ax.set_ylabel(metric.upper())
        # ax.legend(title="Test Method", loc="upper right")
        ax.set_ylim(ylim)  # Apply custom y-axis limits

        # Add grid lines corresponding to y-axis ticks
        ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    # Adjust layout
    plt.tight_layout()

    # saves plot to external file
    plt.savefig(REV_PLOT, format="pdf")

    # shows plot
    plt.show()

if __name__ == "__main__":
    tst_simple_bymethod_plot()
    tst_simple_bygrid_plot()
    rev_interp_plt()
    
