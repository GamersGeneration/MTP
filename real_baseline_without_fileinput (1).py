import numpy as np

def generate_powered_nodes(loc, beam_angle):
    num_nodes = len(loc)
    powered_nodes_sets = []

    for j in range(num_nodes):
        print(f"Node {j + 1} - Powered Nodes:")
        powered_nodes_list = []

        for angle in range(360):
            powered_nodes = set()

            for k in range(num_nodes):
                if j != k and is_node_in_beam(loc[j], loc[k], angle, beam_angle):
                    powered_nodes.add(k)

            print(f"  Angle ({angle}-{angle+beam_angle}) - {list(powered_nodes)}")
            powered_nodes_list.append(powered_nodes)

        powered_nodes_sets.append(powered_nodes_list)

    return powered_nodes_sets

def is_node_in_beam(source, target, angle, beam_angle):
    angle_rad = np.deg2rad(angle)
    delta_x = target[0] - source[0]
    delta_y = target[1] - source[1]
    node_angle = np.arctan2(delta_y, delta_x)
    return -beam_angle/2 < (node_angle - angle_rad) < beam_angle/2

# Number of nodes
num_nodes = 4

# Grid size
grid_size = 100

# Set the seed for reproducibility
np.random.seed(42)

# Generate random coordinates for nodes within the grid
node_locations = np.random.rand(num_nodes, 2) * grid_size

# Beam angle for rotation
beam_angle = 15

# Generate powered nodes sets
powered_nodes_sets = generate_powered_nodes(node_locations, beam_angle)
