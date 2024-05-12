import numpy as np
import csv

def calculate_power(node, transmitter_position, beam_angle, beam_radius):
    distance = np.linalg.norm(np.array(node) - np.array(transmitter_position))
    if 0 <= beam_angle <= 360 and distance <= beam_radius:
        return 1
    else:
        return 0

def read_nodes_from_csv(csv_file):
    nodes = []
    radii = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            x, y, radius, _ = map(float, row)
            nodes.append((x, y))
            radii.append(radius)
    return nodes, radii

def place_transmitters(nodes, radii, area_size, grid_size, beam_radius, beam_angles):
    num_grids_x = int(np.ceil(area_size[0] / grid_size))
    num_grids_y = int(np.ceil(area_size[1] / grid_size))

    transmitters_per_grid = []  # To store the selected transmitters for each grid

    for grid_x in range(num_grids_x):
        for grid_y in range(num_grids_y):
            grid_origin = (grid_x * grid_size, grid_y * grid_size)
            grid_nodes = []

            for node, radius in zip(nodes, radii):
                node_position = np.array(node) + grid_origin

                if 0 <= node_position[0] < grid_size and 0 <= node_position[1] < grid_size:
                    if node_position[0] - radius < 0:
                        node_position[0] = radius
                    if node_position[1] - radius < 0:
                        node_position[1] = radius

                    grid_nodes.append((node_position, radius))

            if grid_nodes:
                # Find the transmitter with the maximum total power for this grid
                best_transmitter = max(grid_nodes, key=lambda transmitter: sum(
                    calculate_power(node[0], transmitter[0], beam_angle, beam_radius) for beam_angle in beam_angles))

                transmitters_per_grid.append(best_transmitter)

    return transmitters_per_grid

# Example usage
csv_file = 'C:\\Users\\IIT_ROPAR_User\\Desktop\\MTP\\dir_2023_dataset_ropar_csv\\RDILP_CSV_50_10_3.csv'  # Example CSV file with x, y, and radii columns
area_size = (50, 50)
grid_size = 20
beam_radius = 10
beam_angles = np.arange(0, 361, 45)

nodes, radii = read_nodes_from_csv(csv_file)
selected_transmitters = place_transmitters(nodes, radii, area_size, grid_size, beam_radius, beam_angles)

# Display the selected transmitters for each grid
for idx, transmitter in enumerate(selected_transmitters, 1):
    print(f"Grid {idx}: Transmitter at {transmitter[0]} with radius {transmitter[1]}")
