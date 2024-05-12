import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def visualize_network(file_path):
    # Read CSV file without header
    df = pd.read_csv(file_path, header=None)

    # Extract number of nodes and grid size
    num_nodes = df.shape[0]
    grid_size = 50  # Assuming a fixed grid size of 50x50

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Generate light multicolor for different node radii using np.linspace
    colors = plt.cm.viridis_r(np.linspace(0, 1, num_nodes))

    # Scatter plot for each node
    for i in range(num_nodes):
        x, y, radius = float(df.iloc[i, 0]), float(df.iloc[i, 1]), float(df.iloc[i, 2])
        ax.scatter(x, y, color=colors[i], s=radius*10, edgecolor='black', alpha=0.7)

    # Set aspect ratio and axis limits based on grid size
    ax.set_aspect('equal', 'box')
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)

    # Set labels and title
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    plt.title(f'Network Visualization - {num_nodes} Nodes, Grid Size: {grid_size}')

    # Show the plot
    plt.show()

# Example usage
file_path = r'C:\Users\IIT_ROPAR_User\Desktop\MTP\dir_2023_dataset_ropar_csv\RDILP_CSV_100_20_1.csv'
visualize_network(file_path)
