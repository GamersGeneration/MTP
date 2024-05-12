#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      IIT_ROPAR_User
#
# Created:     03-02-2024
# Copyright:   (c) IIT_ROPAR_User 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

def generate_powered_nodes(loc, beam_angle):
    num_nodes = len(loc)
    powered_nodes_sets = []

    for j in range(num_nodes):
        print(f"\nNode {j + 1} - Powered Nodes:")
        powered_nodes_list = []

        for angle in range(360):
            powered_nodes = set()

            for k in range(num_nodes):
                if j != k and is_node_in_beam(loc[j], loc[k], angle, beam_angle, loc[k, 2]):
                    powered_nodes.add(k)

            print(f"  Angle ({angle}-{(angle + beam_angle) % 360}) - Nodes powered: {len(powered_nodes)} - Powered Nodes: {list(powered_nodes)}")
            powered_nodes_list.append(powered_nodes)

        powered_nodes_sets.append(powered_nodes_list)

    return powered_nodes_sets

def is_node_in_beam(source, target, angle, beam_angle, radius):
    angle_rad = np.deg2rad(angle)
    delta_x = target[0] - source[0]
    delta_y = target[1] - source[1]
    node_angle = np.arctan2(delta_y, delta_x)

    # Check if the transmitter is within the node's range
    transmitter_distance = np.sqrt(delta_x**2 + delta_y**2)
    return -beam_angle/2 <= (node_angle - angle_rad) <= beam_angle/2 and transmitter_distance <= radius

# Replace this line with your actual file path
csv_file_path = r'C:\Users\IIT_ROPAR_User\Desktop\MTP\dir_2023_dataset_ropar_csv\RDILP_CSV_100_20_1.csv'

# Read CSV file without header and with specified column names
node_data = pd.read_csv(csv_file_path, header=None, usecols=[1, 2, 3], names=['X-coordinate', 'Y-coordinate', 'Radius'])

# Extract node locations and radius from the CSV file
node_locations = node_data.values

# Beam angle for rotation
beam_angle = 15

# Generate powered nodes sets
powered_nodes_sets = generate_powered_nodes(node_locations, beam_angle)

# Get the number of nodes
num_nodes = len(node_locations)

# Visualization of No. of Nodes Powered vs Angle
angles = range(360)
plt.figure(figsize=(12, 8))

for j, powered_nodes_list in enumerate(powered_nodes_sets):
    node_counts = [len(node_set) for node_set in powered_nodes_list]
    plt.plot(angles, node_counts, label=f'Node {j + 1}')

plt.xlabel('Angle')
plt.ylabel('Number of Powered Nodes')
plt.title('Number of Powered Nodes vs Angle')
plt.legend()
plt.show()

# Node Coverage Visualization
plt.figure(figsize=(10, 6))
plt.scatter(node_locations[:, 0], node_locations[:, 1], label='All Nodes', color='grey')
for j, powered_nodes_list in enumerate(powered_nodes_sets):
    powered_nodes = set.union(*powered_nodes_list)
    plt.scatter(node_locations[list(powered_nodes), 0], node_locations[list(powered_nodes), 1], label=f'Powered by Node {j + 1}')

plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.title('Node Coverage Visualization')
plt.legend()
plt.show()

# Histogram of Powered Nodes
plt.figure(figsize=(10, 6))
for j, powered_nodes_list in enumerate(powered_nodes_sets):
    node_counts = [len(node_set) for node_set in powered_nodes_list]
    plt.hist(node_counts, bins=range(0, max(node_counts)+2), alpha=0.5, label=f'Node {j + 1}')

plt.xlabel('Number of Powered Nodes')
plt.ylabel('Frequency')
plt.title('Histogram of Powered Nodes')
plt.legend()
plt.show()

# Node Connectivity Graph
plt.figure(figsize=(10, 8))
for j, powered_nodes_list in enumerate(powered_nodes_sets):
    powered_nodes = set.union(*powered_nodes_list)
    G = nx.Graph()
    G.add_nodes_from(range(1, num_nodes + 1))
    G.add_edges_from([(j + 1, k + 1) for k in powered_nodes])
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=700, font_size=8, label=f'Node {j + 1}')

plt.title('Node Connectivity Graph')
plt.show()

# Heatmap of Node Coverage
plt.figure(figsize=(12, 8))
sns.heatmap(np.array([len(set.union(*powered_nodes_list)) for powered_nodes_list in powered_nodes_sets]).reshape(1, -1), cmap='Blues', annot=True, fmt='g', xticklabels=range(1, num_nodes + 1), yticklabels=['Nodes Powered'])
plt.xlabel('Node')
plt.ylabel('Node Placement')
plt.title('Node Coverage Heatmap')
plt.show()
