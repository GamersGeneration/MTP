import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def generate_powered_nodes(loc, beam_angle):
    num_nodes = len(loc)
    powered_nodes_sets = []

    for j in range(num_nodes):
        qmin, qmax = 0, beam_angle
        cnt = 0
        powered_nodes = set()

        for i in range(360 - (beam_angle - 1)):
            count = 0
            node_ids = set()

            for k in range(num_nodes):
                angle = (180 / np.pi) * np.arcsin((loc[j][1] - loc[k][1]) / np.sqrt((loc[j][0] - loc[k][0])**2 + (loc[j][1] - loc[k][1])**2))

                if (qmin < angle < qmax) or (j == k):
                    count += 1
                    node_ids.add(k)

                if qmin < angle < qmax:
                    cnt += 1

            if count != 1:
                powered_nodes.update(node_ids)

            qmin += 1
            qmax += 1

        if cnt == 0:
            powered_nodes.add(j)

        powered_nodes_sets.append(powered_nodes)

    return powered_nodes_sets

def visualize_network(loc, powered_nodes_sets):
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 100])

    # Plot nodes
    ax.scatter(loc[:, 0], loc[:, 1], label='Nodes')

    # Plot powered nodes for each node at different angles
    for j, powered_nodes in enumerate(powered_nodes_sets):
        for angle, powered_set in enumerate(powered_nodes):
            if len(powered_set) > 0:  # Check if there are powered nodes for this angle
                powered_nodes_loc = loc[list(powered_set)]
                circle = Circle(loc[j], radius=5, alpha=0.3, label=f"Powered Nodes (Angle: {angle}°)")
                ax.add_patch(circle)

    plt.legend()
    plt.show()

# Number of nodes
num_nodes = 40

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

# Visualize the network state
visualize_network(node_locations, powered_nodes_sets)

# Output nodes' locations for each angle from 0 to 360
for angle, powered_nodes in enumerate(powered_nodes_sets):
    print(f"Angle {angle}° - Powered Nodes:")
    for j, powered_set in enumerate(powered_nodes):
        print(f"Node {j + 1}: {list(powered_set)}")
