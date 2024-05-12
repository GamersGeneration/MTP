import csv
import math
import time
import matplotlib.pyplot as plt

# Define the classes and functions for the first approach

class Node:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

def create_grids(area_size, grid_size):
    num_cols = area_size[0] // grid_size
    num_rows = area_size[1] // grid_size
    grids = [[[] for _ in range(num_cols)] for _ in range(num_rows)]
    return grids

def populate_grids(nodes, grids, grid_size):
    for node in nodes:
        node_grid_x = node.x // grid_size
        node_grid_y = node.y // grid_size
        grids[node_grid_y][node_grid_x].append(node)

def search_neighbors(grid, neighbor_grids):
    # Search in right, left, up, down, and diagonal directions
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            neighbor_x = grid[0] + dx
            neighbor_y = grid[1] + dy
            if 0 <= neighbor_x < len(neighbor_grids[0]) and 0 <= neighbor_y < len(neighbor_grids):
                for node in neighbor_grids[neighbor_y][neighbor_x]:
                    pass  # In real implementation, perform desired operations

def merge_grids(grids):
    # Merge adjacent grid cells to form larger cells
    merged_grids = []
    for row_index in range(0, len(grids), 2):
        row = grids[row_index]
        merged_row = []
        for col_index in range(0, len(row), 2):
            merged_row.append([node for subgrid in row[col_index:col_index+2] for node in subgrid])
        merged_grids.append(merged_row)
    return merged_grids

def approach1(area_size, grid_size, nodes):
    grids = create_grids(area_size, grid_size)
    populate_grids(nodes, grids, grid_size)

    iteration = 1
    while len(grids) > 1:
        neighbor_grids = merge_grids(grids)
        grids = neighbor_grids
        iteration += 1

# Define the functions for the second approach

GRID_SIZE = 10
BEAM_ANGLE = 15

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def is_in_beam_angle(angle, angle_range):
    return angle_range[0] <= angle <= angle_range[1] or (angle + 360) <= angle_range[1]

def approach2(nodes):
    powered_nodes = {}
    
    for node in nodes:
        node_id, node_x, node_y, node_radius = node
        powered_nodes[node_id] = []
    
        for angle in range(0, 360):
            powered_at_angle = set()
    
            for other_node in nodes:
                other_node_id, other_x, other_y, other_radius = other_node
    
                if other_node_id != node_id:
                    dist = distance(node_x, node_y, other_x, other_y)
    
                    if dist <= node_radius and is_in_beam_angle(angle, (angle, angle + BEAM_ANGLE)):
                        powered_at_angle.add(other_node_id)
    
            powered_nodes[node_id].append((angle, tuple(sorted(powered_at_angle))))
    
    all_powered_nodes = set()
    
    for _, powered_at_each_angle in powered_nodes.items():
        for _, powered_set in powered_at_each_angle:
            all_powered_nodes.update(powered_set)
    
    min_transmitters_required = 20-len(all_powered_nodes)+1
    return min_transmitters_required

# Define the main function to evaluate both approaches

def main():
    area_size = (10, 10)
    grid_size = 1
    nodes = [(1, 1, 3, 1), (2, 5, 5, 1), (3, 8, 8, 1)]  # Example nodes

    start_time = time.time()
    approach1(area_size, grid_size, [Node(*node[1:]) for node in nodes])
    approach1_time = time.time() - start_time

    start_time = time.time()
    min_transmitters_required = approach2(nodes)
    approach2_time = time.time() - start_time

    print("Approach 1 Execution Time:", approach1_time)
    print("Approach 2 Execution Time:", approach2_time)
    print("Minimum Transmitters Required (Approach 2):", min_transmitters_required)

    # Plotting
    approach_labels = ['Grid Approach', 'Baseline']
    execution_times = [approach1_time, approach2_time]
    transmitters_required = [0, min_transmitters_required]

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.bar(approach_labels, execution_times, color=['blue', 'orange'])
    plt.xlabel('Approach')
    plt.ylabel('Execution Time (s)')
    plt.title('Comparison of Execution Time')

    plt.subplot(1, 2, 2)
    plt.bar(approach_labels, transmitters_required, color=['blue', 'orange'])
    plt.xlabel('Approach')
    plt.ylabel('Transmitters Required')
    plt.title('Comparison of Transmitters Required')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
