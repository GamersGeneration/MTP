import time

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

def generate_results(iteration, grids, neighbor_grids):
    print(f"Iteration {iteration} ({len(grids)} grid(s) in 8 directions)")
    for row_index, row in enumerate(grids):
        for col_index, grid in enumerate(row):
            print(f"Grid {col_index}, {row_index} -", end="")
            search_neighbors((col_index, row_index), neighbor_grids)
            print()

def record_execution_time(start_time):
    execution_time = time.time() - start_time
    print("Execution Time:", execution_time)
    return execution_time



# Example usage
area_size = (10, 10)
grid_size = 1
nodes = [Node(1, 3, 1), Node(5, 5, 1), Node(8, 8, 1)]  # Example nodes
grids = create_grids(area_size, grid_size)
populate_grids(nodes, grids, grid_size)

start_time = time.time()
iteration = 1
while len(grids) > 1:
    neighbor_grids = merge_grids(grids)
    generate_results(iteration, grids, neighbor_grids)
    grids = neighbor_grids
    iteration += 1

execution_time = record_execution_time(start_time)