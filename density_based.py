import csv
import math

def read_csv(file_path):
    nodes = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip header
        for row in reader:
            x, y, radius = map(float, row[1:4])
            nodes.append({'x': x, 'y': y, 'radius': radius, 'powered': False})
    return nodes

def calculate_density(nodes, point, radius):
    count = sum(1 for node in nodes if math.sqrt((node['x'] - point['x'])**2 + (node['y'] - point['y'])**2) <= radius)
    return count

def find_high_density_regions(nodes, radius):
    high_density_regions = []
    for node in nodes:
        density = calculate_density(nodes, node, radius)
        high_density_regions.append({'point': node, 'density': density})
    return high_density_regions

def place_transmitter(nodes, radius, beam_angle):
    high_density_regions = find_high_density_regions(nodes, radius)
    powered_nodes = []

    for region in high_density_regions:
        max_density_point = region['point']
        max_density = region['density']

        for angle in range(0, 360):
            powered_nodes_for_angle = []

            for node in nodes:
                if math.sqrt((node['x'] - max_density_point['x'])**2 + (node['y'] - max_density_point['y'])**2) <= radius:
                    angle_diff = abs(math.atan2(node['y'] - max_density_point['y'], node['x'] - max_density_point['x']) - math.radians(angle))
                    if angle_diff <= math.radians(beam_angle / 2):
                        powered_nodes_for_angle.append(node)

            if len(powered_nodes_for_angle) > len(powered_nodes):
                powered_nodes = powered_nodes_for_angle

    return powered_nodes

def main():
    file_path = r'C:\Users\IIT_ROPAR_User\Desktop\MTP\dir_2023_dataset_ropar_csv\RDILP_CSV_50_10_1.csv'  # Replace with the actual path to your dataset
    nodes = read_csv(file_path)

    radius_of_transmitter = 10
    beam_angle_of_transmitter = 30

    powered_nodes = place_transmitter(nodes, radius_of_transmitter, beam_angle_of_transmitter)

    print("Powered Nodes:")
    for node in powered_nodes:
        print(f"x: {node['x']}, y: {node['y']}")

if __name__ == "__main__":
    main()
