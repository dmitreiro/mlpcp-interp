import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the CSV file
file_path = "~/MLCCM/models/testing_performance_metrics.csv"  # Replace with the path to your CSV file
df = pd.read_csv(file_path)

# Set up the plotting grid
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)

# Define metrics and titles
metrics = ["r2", "mae", "mape"]
titles = ["R² (Goodness of Fit)", "MAE (Mean Absolute Error)", "MAPE (Mean Absolute Percentage Error)"]
y_limits = [(0.9, 1.050), (0, 5), (0, 0.06)]  # Custom y-axis limits

# Create a plot for each metric
for ax, metric, title, ylim in zip(axes, metrics, titles, y_limits):
    # Use seaborn's barplot for each metric
    sns.barplot(
        data=df,
        x="model_method",
        y=metric,
        hue="test_method",
        ax=ax
    )
    ax.set_title(title)
    ax.set_xlabel("Model Method")
    ax.set_ylabel(metric.upper())
    ax.legend(title="Test Method", loc="upper right")
    ax.set_ylim(ylim)  # Apply custom y-axis limits
    
    # Add grid lines corresponding to y-axis ticks
    ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Adjust layout
plt.tight_layout()
plt.show()
