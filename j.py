class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
                    print(f"Grid {grid} - Node at ({node.x}, {node.y})")

def generate_results(grids, neighbor_grids):
    for row_index, row in enumerate(grids):
        for col_index, grid in enumerate(row):
            print(f"Grid {col_index}, {row_index} - nodes: ", end="")
            for node in grid:
                print(f"({node.x}, {node.y}), ", end="")
            print()
            search_neighbors((col_index, row_index), neighbor_grids)

# Example usage
area_size = (4, 4)
grid_size = 1
nodes = [Node(1, 3), Node(3, 4), Node(1, 2)]  # Example nodes
grids = create_grids(area_size, grid_size)
populate_grids(nodes, grids, grid_size)
generate_results(grids, grids)
