import csv
import math

GRID_SIZE = 100
MIN_BEAM_ANGLE = 20
MAX_BEAM_ANGLE = 120
BEAM_ANGLE_INCREMENT = 1

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def is_in_beam_angle(angle, angle_range):
    return angle_range[0] <= angle <= angle_range[1] or (angle + 360) <= angle_range[1]

def main():
    # Step 1: Read input from CSV file
    input_file_path = r'C:\Users\IIT_ROPAR_User\Desktop\MTP\dir_2023_dataset_ropar_csv\RDILP_CSV_50_10_3.csv'
    nodes = []

    with open(input_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            nodes.append((int(row[0]), float(row[1]), float(row[2]), float(row[3])))

    # Step 2: Process nodes and find powered nodes
    powered_nodes = {}

    for node in nodes:
        node_id, node_x, node_y, node_radius = node
        powered_nodes[node_id] = []

        for beam_angle in range(MIN_BEAM_ANGLE, MAX_BEAM_ANGLE + 1, BEAM_ANGLE_INCREMENT):
            for angle in range(0, 360, BEAM_ANGLE_INCREMENT):
                powered_at_angle = set()

                for other_node in nodes:
                    other_node_id, other_x, other_y, other_radius = other_node

                    if other_node_id != node_id:
                        dist = distance(node_x, node_y, other_x, other_y)

                        if dist <= node_radius and is_in_beam_angle(angle, (angle, angle + beam_angle)):
                            powered_at_angle.add(other_node_id)

                powered_nodes[node_id].append((angle, beam_angle, tuple(sorted(powered_at_angle))))

    # Step 3: Print powered nodes and node location for each node, angle, and beam angle
    for node_id, powered_at_each_angle in powered_nodes.items():
        print(f"Node {node_id} - Location: ({nodes[node_id][1]}, {nodes[node_id][2]}):")
        for angle, beam_angle, powered_set in powered_at_each_angle:
            print(f"  Angle {angle}-{(angle + beam_angle) % 360} (Beam Angle {beam_angle}): {powered_set}")

    # Step 4: Find the minimum number of transmitters required
    max_powered_nodes_count = 0
    max_powered_nodes_set = set()

    for _, powered_at_each_angle in powered_nodes.items():
        for _, _, powered_set in powered_at_each_angle:
            if len(powered_set) > max_powered_nodes_count:
                max_powered_nodes_count = len(powered_set)
                max_powered_nodes_set = powered_set

    min_transmitters_required = int(row[0]) - len(max_powered_nodes_set) + 1
    print(f"\nMinimum number of transmitters required: {min_transmitters_required}")

if __name__ == "__main__":
    main()
