import numpy as np
from enum import Enum

class TileType(Enum):
    EMPTY = 0
    TREE = 1
    BURNING = 2
    BURNT = 3

class ForestFireModel:    
    def __init__(self, grid_size, p=0.05, f=0.001, density=0.5, neighborhood="von_neumann"):
        self.rows, self.cols = grid_size
        self.p = p
        self.f = f
        self.density = density
        self.neighborhood = neighborhood
        
        self.grid = np.zeros(grid_size, dtype=int)
        
        self.initialize_forest()
    
    def initialize_forest(self):
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        
        random_values = np.random.random(size=(self.rows, self.cols))
        self.grid[random_values < self.density] = TileType.TREE.value
        
        num_initial_fires = max(1, int(self.f * self.rows * self.cols))
        fire_positions = np.random.randint(0, self.rows, size=num_initial_fires), np.random.randint(0, self.cols, size=num_initial_fires)
        self.grid[fire_positions] = TileType.BURNING.value
    
    def get_neighbors(self, row, col):
        neighbors = []
        
        if self.neighborhood == "von_neumann":
            for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbors.append((nr, nc))
        elif self.neighborhood == "moore":
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue  # Skip the cell itself
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        neighbors.append((nr, nc))
        else:
            raise Exception("Invalid neighborhood type (von_neumann, moore)")
        
        return neighbors
    
    def update(self):
        new_grid = np.copy(self.grid)
        
        for row in range(self.rows):
            for col in range(self.cols):
                current_state = self.grid[row, col]
                
                # Rule 1: Empty area or burnt tree can become a tree with probability p
                if current_state == TileType.EMPTY.value or current_state == TileType.BURNT.value:
                    if np.random.random() < self.p:
                        new_grid[row, col] = TileType.TREE.value
                
                # Rule 2 & 3: Tree can catch fire from neighbors or spontaneously
                elif current_state == TileType.TREE.value:
                    neighbors = self.get_neighbors(row, col)
                    neighbor_burning = False
                    
                    for nr, nc in neighbors:
                        if self.grid[nr, nc] == TileType.BURNING.value:
                            neighbor_burning = True
                            break
                    
                    if neighbor_burning:
                        # Rule 2: Tree catches fire if a neighbor is burning
                        new_grid[row, col] = TileType.BURNING.value
                    elif np.random.random() < self.f:
                        # Rule 3: Tree catches fire spontaneously with probability f
                        new_grid[row, col] = TileType.BURNING.value
                
                # Rule 4: Burning tree turns into burnt tree
                elif current_state == TileType.BURNING.value:
                    new_grid[row, col] = TileType.BURNT.value
        
        self.grid = new_grid        
        return self.grid