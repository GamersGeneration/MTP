import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

def calculate_density(node_locations):
    kmeans = KMeans(n_clusters=1)
    kmeans.fit(node_locations[:, :2])
    density = len(kmeans.labels_) / kmeans.inertia_
    return density

def place_transmitters(node_locations):
    num_transmitters = 1
    while True:
        kmeans = KMeans(n_clusters=num_transmitters)
        kmeans.fit(node_locations[:, :2])
        transmitter_locations = kmeans.cluster_centers_

        # Check if all nodes are covered
        covered_nodes = set()
        for i, node in enumerate(node_locations):
            distances = np.linalg.norm(transmitter_locations - node[:2], axis=1)
            closest_transmitter = np.argmin(distances)
            covered_nodes.add(closest_transmitter)

        if len(covered_nodes) == len(node_locations):
            break  # All nodes are covered, stop the loop
        else:
            num_transmitters += 1

    return transmitter_locations, num_transmitters

# Replace this line with your actual file path
csv_file_path = r'C:\Users\IIT_ROPAR_User\Desktop\MTP\dir_2023_dataset_ropar_csv\RDILP_CSV_100_20_3.csv'

# Read CSV file without header and with specified column names
node_data = pd.read_csv(csv_file_path, header=None, usecols=[1, 2, 3], names=['X-coordinate', 'Y-coordinate', 'Radius'])

# Extract node locations and radius from the CSV file
node_locations = node_data.values

# Calculate node density
density = calculate_density(node_locations)
print(f"Node Density: {density}")

# Place transmitters dynamically
transmitter_locations, num_transmitters = place_transmitters(node_locations)
print(f"Transmitter Locations based on Density:\n{transmitter_locations}")
print(f"Number of Transmitters Required: {num_transmitters}")
