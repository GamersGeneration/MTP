#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      IIT_ROPAR_User
#
# Created:     03-02-2024
# Copyright:   (c) IIT_ROPAR_User 2024
# Licence:     <your licence>
#This code adds each node placement's details to a DataFrame (results_df). It includes columns for the node number, the number of powered nodes, the location of the transmitter, the angle range, and the list of powered nodes. Additionally, it calculates and prints the minimum number of transmitters required in the network.-------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

def generate_powered_nodes(loc, beam_angle):
    num_nodes = len(loc)
    powered_nodes_sets = []
    results_table = []

    for j in range(num_nodes):
        print(f"\nNode {j + 1} - Powered Nodes:")
        powered_nodes_list = []

        for angle in range(360):
            powered_nodes = set()

            for k in range(num_nodes):
                if j != k and is_node_in_beam(loc[j], loc[k], angle, beam_angle, loc[k, 2]):
                    powered_nodes.add(k)

            print(f"  Angle ({angle}-{(angle + beam_angle) % 360}) - Nodes powered: {len(powered_nodes)} - Powered Nodes: {list(powered_nodes)}")

            results_table.append({
                'Node': j + 1,
                'Powered Nodes': len(powered_nodes),
                'Transmitter Location': loc[j],
                'Angle Range': (angle, (angle + beam_angle) % 360),
                'Powered Nodes List': list(powered_nodes)
            })

            powered_nodes_list.append(powered_nodes)

        powered_nodes_sets.append(powered_nodes_list)

    results_df = pd.DataFrame(results_table)

    return powered_nodes_sets, results_df

def is_node_in_beam(source, target, angle, beam_angle, radius):
    angle_rad = np.deg2rad(angle)
    delta_x = target[0] - source[0]
    delta_y = target[1] - source[1]
    node_angle = np.arctan2(delta_y, delta_x)

    # Ensure the node angle is within the range [0, 360)
    node_angle = (node_angle + 2 * np.pi) % (2 * np.pi)

    # Check if the transmitter is within the node's range
    transmitter_distance = np.sqrt(delta_x**2 + delta_y**2)
    return -beam_angle/2 <= (node_angle - angle_rad) <= beam_angle/2 and transmitter_distance <= radius

# Replace this line with your actual file path
csv_file_path = r'C:\Users\IIT_ROPAR_User\Desktop\MTP\dir_2023_dataset_ropar_csv\RDILP_CSV_100_20_3.csv'

# Read CSV file without header and with specified column names
node_data = pd.read_csv(csv_file_path, header=None, usecols=[1, 2, 3], names=['X-coordinate', 'Y-coordinate', 'Radius'])

# Extract node locations and radius from the CSV file
node_locations = node_data.values

# Beam angle for rotation
beam_angle = 15

# Generate powered nodes sets and results DataFrame
powered_nodes_sets, results_df = generate_powered_nodes(node_locations, beam_angle)

# Display the results DataFrame
print("\nResults Table:")
print(results_df)

# Calculate minimum number of transmitters required
min_transmitters_required = len(set.union(*[set.union(*powered_nodes_list) for powered_nodes_list in powered_nodes_sets]))
print(f"\nMinimum Number of Transmitters Required: {min_transmitters_required}")

# Visualize the relationship between the number of nodes and the minimum number of transmitters required
plt.figure(figsize=(10, 6))
sns.scatterplot(x=results_df['Node'], y=results_df['Powered Nodes'])
plt.xlabel('Node Number')
plt.ylabel('Number of Transmitters Required')
plt.title('Number of Nodes vs Number of Transmitters Required')
plt.show()


