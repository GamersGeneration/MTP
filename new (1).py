import numpy as np
import pandas as pd

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

            print(f"  Angle ({angle}-{(angle + beam_angle) % 360}) - Nodes powered: {list(powered_nodes)}")
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
csv_file_path = r'C:\Users\IIT_ROPAR_User\Desktop\MTP\dir_2023_dataset_ropar_csv\RDILP_CSV_50_10_1.csv'

# Read CSV file without header and with specified column names
node_data = pd.read_csv(csv_file_path, header=None, usecols=[1, 2, 3], names=['X-coordinate', 'Y-coordinate', 'Radius'])

# Extract node locations and radius from the CSV file
node_locations = node_data.values

# Beam angle for rotation
beam_angle = 15

# Generate powered nodes sets
powered_nodes_sets = generate_powered_nodes(node_locations, beam_angle)
