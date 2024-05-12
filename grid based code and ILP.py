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

def generate_results(iteration, grids):
    print(f"Iteration {iteration} ({len(grids)} grid(s) in 8 directions)")
    for row_index, row in enumerate(grids):
        for col_index, grid in enumerate(row):
            print(f"Grid {col_index}, {row_index} - Nodes: ", end="")
            if grid:  # Check if the grid has nodes
                for node in grid:
                    print(f"({node.x}, {node.y})", end="")
            else:
                print("None", end="")
            print()

# Example usage
area_size = (10, 10)
grid_size = 1
nodes = [Node(1, 3, 1), Node(5, 5, 1), Node(8, 8, 1)]  # Example nodes
grids = create_grids(area_size, grid_size)
populate_grids(nodes, grids, grid_size)

iteration = 1
while len(grids) > 1:
    generate_results(iteration, grids)
    iteration += 1
    # For simplicity, let's just remove the first row and column in each iteration
    grids = [row[1:] for row in grids[1:] if row[1:]]
from pulp import LpVariable, LpProblem, LpMinimize, lpSum

# Define nodes and grids
nodes = [(1, 3), (5, 5), (8, 8)]  # Example nodes
grids = [(i, j) for i in range(10) for j in range(10)]  # All possible grids

# Create LP problem
prob = LpProblem("GridSelection", LpMinimize)

# Define decision variables
x = LpVariable.dicts("Grid", grids, 0, 1, LpBinary)

# Add coverage constraints
for node in nodes:
    prob += lpSum(x[grid] for grid in grids if node[0] >= grid[0] and node[1] >= grid[1] and node[0] < grid[0] + grid_size and node[1] < grid[1] + grid_size) >= 1

# Add grid selection constraint
prob += lpSum(x[grid] for grid in grids) == len(grids)

# Define objective function
prob += lpSum(x.values())

# Solve ILP
prob.solve()

# Print results
print("Minimum number of selected grids:", int(prob.objective.value()))


