import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

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

    transmitter_locations = set()
    powered_nodes_by_angle = {}

    for transmitter_location in region_nodes:
        powered_nodes = {tuple(transmitter_location)}
        powered_nodes_at_angle = {}

        for angle in range(360):
            nodes_at_angle = set()
            for node_location in region_nodes:
                if is_node_in_beam(transmitter_location, node_location, beam_angle, node_location[2]):
                    nodes_at_angle.add(tuple(node_location))
                    powered_nodes.add(tuple(node_location))
            powered_nodes_at_angle[angle] = nodes_at_angle

        transmitter_locations.update(powered_nodes)
        powered_nodes_by_angle[transmitter_location] = powered_nodes_at_angle

    return transmitter_locations, powered_nodes_by_angle

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
    region_transmitters, powered_nodes_by_angle = place_transmitters_in_region(node_locations, region_label)

    # Print nodes powered at each angle within the region
    print(f"\nDensity Region {region_label}")
    for transmitter_location, nodes_at_angle in powered_nodes_by_angle.items():
        print(f"  Transmitter at {transmitter_location} - Nodes powered at each angle:")
        for angle, nodes in nodes_at_angle.items():
            print(f"    Angle {angle}: {len(nodes)} nodes powered")

    min_transmitters_required.update(region_transmitters)

# Print the results
print("\nMinimum Number of Transmitters Required for the Entire Grid:")
for transmitter in min_transmitters_required:
    print(transmitter)
print(f"\nTotal Minimum Number of Transmitters Required: {len(min_transmitters_required)}")
