import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
import networkx as nx
import matplotlib.pyplot as plt

def is_node_in_beam(source, target, beam_angle, radius):
    delta_x = target[0] - source[0]
    delta_y = target[1] - source[1]
    node_distance = np.sqrt(delta_x**2 + delta_y**2)

    if node_distance <= radius:
        return True

    angle_rad = np.arctan2(delta_y, delta_x)
    node_angle = (angle_rad + 2 * np.pi) % (2 * np.pi)
    source_angle = source[2]  # Transmitter angle

    # Check if the node is within the transmitter's beam angle
    angle_diff = np.abs((node_angle - source_angle + 360) % 360)
    return angle_diff <= beam_angle / 2

def calculate_density(node_locations):
    db = DBSCAN(eps=1.5, min_samples=5)  # You can adjust eps and min_samples based on your data
    db.fit(node_locations[:, :2])
    labels = db.labels_
    unique_labels, counts = np.unique(labels, return_counts=True)
    density = dict(zip(unique_labels, counts / len(node_locations)))
    return density, labels

def place_transmitters_in_region(node_locations, region_label, beam_angle=15):
    region_nodes = node_locations[labels == region_label]

    G = nx.Graph()

    for node_location in region_nodes:
        G.add_node(tuple(node_location))

    for node1 in G.nodes():
        for node2 in G.nodes():
            if node1 != node2 and is_node_in_beam(node1, node2, beam_angle, node2[2]):
                G.add_edge(node1, node2)

    components = list(nx.connected_components(G))

    transmitter_locations = set()
    for component in components:
        transmitter_locations.add(min(component, key=lambda x: x[2]))  # Choose the node with the smallest radius

    return transmitter_locations

# Replace this line with your actual file path
csv_file_path = r'C:\Users\IIT_ROPAR_User\Desktop\MTP\dir_2023_dataset_ropar_csv\RDILP_CSV_100_20_3.csv'

# Read CSV file without header and with specified column names
node_data = pd.read_csv(csv_file_path, header=None, usecols=[1, 2, 3], names=['X-coordinate', 'Y-coordinate', 'Radius'])

# Extract node locations and radius from the CSV file
node_locations = node_data.values

# Calculate node density using DBSCAN
density, labels = calculate_density(node_locations)

# Sort regions by density in decreasing order
sorted_regions = sorted(density.keys(), key=lambda x: density[x], reverse=True)

min_transmitters_required = set()

for region_label in sorted_regions:
    region_transmitters = place_transmitters_in_region(node_locations, region_label)
    min_transmitters_required.update(region_transmitters)

# Print the results
print("\nMinimum Number of Transmitters Required for the Entire Grid:")
for transmitter in min_transmitters_required:
    print(transmitter)
print(f"\nTotal Minimum Number of Transmitters Required: {len(min_transmitters_required)}")
