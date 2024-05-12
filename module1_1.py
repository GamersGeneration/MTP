import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

def calculate_density(node_locations):
    kmeans = KMeans(n_clusters=1)  # Assuming you want to find the overall density
    kmeans.fit(node_locations[:, :2])  # Considering only X and Y coordinates for clustering
    density = len(kmeans.labels_) / kmeans.inertia_
    return density

def place_transmitters(node_locations, num_transmitters):
    kmeans = KMeans(n_clusters=num_transmitters)
    kmeans.fit(node_locations[:, :2])
    transmitter_locations = kmeans.cluster_centers_
    return transmitter_locations

# Replace this line with your actual file path
csv_file_path = r'C:\Users\IIT_ROPAR_User\Desktop\MTP\dir_2023_dataset_ropar_csv\RDILP_CSV_100_20_3.csv'

# Read CSV file without header and with specified column names
node_data = pd.read_csv(csv_file_path, header=None, usecols=[1, 2, 3], names=['X-coordinate', 'Y-coordinate', 'Radius'])

# Extract node locations and radius from the CSV file
node_locations = node_data.values

# Calculate node density
density = calculate_density(node_locations)
print(f"Node Density: {density}")

# Set the desired number of transmitters
num_transmitters = 3  # You can adjust this based on your requirements

# Place transmitters based on density
transmitter_locations = place_transmitters(node_locations, num_transmitters)
print(f"Transmitter Locations based on Density:\n{transmitter_locations}")
