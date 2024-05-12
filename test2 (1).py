import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import Canvas, messagebox

def generate_powered_nodes(loc, beam_angle):
    num_nodes = len(loc)
    powered_nodes_sets = []

    for j in range(num_nodes):
        print(f"Node {j + 1} - Powered Nodes:")
        powered_nodes_list = []

        # Set transmitter position as the node's location
        transmitter_position = loc[j, :2]

        for angle in range(360):
            powered_nodes = set()

            for k in range(num_nodes):
                if j != k and is_node_in_beam(transmitter_position, loc[k, :2], angle, beam_angle, loc[k, 2]):
                    powered_nodes.add(k)

            print(f"  Angle ({angle}-{angle+beam_angle}) - {list(powered_nodes)}")
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
    return -beam_angle/2 < (node_angle - angle_rad) < beam_angle/2 and transmitter_distance <= radius

def visualize_network(node_locations, powered_nodes_sets):
    root = tk.Tk()
    root.title("Wireless Sensor Network Visualization")

    canvas = Canvas(root, width=1600, height=1600, bg="white")
    canvas.pack()

    # Draw nodes with their radius
    for i, (x, y, radius) in enumerate(node_locations):
        scale_factor = 5  # Adjust this factor based on the desired visualization
        canvas.create_oval(x-radius*scale_factor, y-radius*scale_factor, 
                           x+radius*scale_factor, y+radius*scale_factor,
                           outline="black", fill="white")
        canvas.create_text(x, y, text=f"Node {i + 1}", font=("Arial", 8))

    # Function to highlight powered nodes on click
    def on_node_click(event):
        x, y = event.x, event.y
        clicked_node = None

        # Check which node is clicked
        for i, (node_x, node_y, radius) in enumerate(node_locations):
            if (x - node_x)**2 + (y - node_y)**2 <= radius**2*scale_factor**2:
                clicked_node = i
                break

        if clicked_node is not None:
            # Show the powered nodes from the clicked node
            powered_nodes = powered_nodes_sets[clicked_node][0]  # Assuming 0-degree angle for simplicity
            messagebox.showinfo("Powered Nodes", f"Powered Nodes from Node {clicked_node + 1}: {list(powered_nodes)}")

    canvas.bind("<Button-1>", on_node_click)

    root.mainloop()

# Replace this line with your actual file path
csv_file_path = r'C:\Users\IIT_ROPAR_User\Desktop\MTP\dir_2023_dataset_ropar_csv\RDILP_CSV_50_10_1.csv'

# Read CSV file without header and with specified column names
node_data = pd.read_csv(csv_file_path, header=None, usecols=[1, 2, 3], names=['X-coordinate', 'Y-coordinate', 'Radius'])

# Extract node
