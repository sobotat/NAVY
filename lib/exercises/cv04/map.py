from enum import Enum

class TileType(Enum):
    Empty = 0
    Wall = 1,
    Tresure = 2,
    Trap = 3,
    Player = 4   

class Map:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y

        self.map = [([TileType.Empty] * size_x)  for _ in range(size_y)]

    def set_tile(self, x, y, type:TileType):
        if type in {TileType.Tresure}:
            for row in self.map:
                for i, t in enumerate(row):
                    if t == type:
                        row[i] = TileType.Empty

        self.map[y][x] = type

    def get_tile(self, x, y) -> TileType:
        return self.map[y][x]
    
    def is_valid_position(self, x, y) -> bool:
        if x < 0 or y < 0:
            return False
        if x >= self.size_x:
            return False
        if y >= self.size_y:
            return False
        return True
    
    def contains_tile(self, type:TileType):
        for row in self.map:
            for tile in row:
                if tile == type:
                    return True
        return False