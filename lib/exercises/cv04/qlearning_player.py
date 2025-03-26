from lib.exercises.cv04.q_table import QTable
from lib.exercises.cv04.map import Map, TileType
from lib.exercises.cv04.direction import Direction

class QLearningPlayer:

    def __init__(self, x, y, map:Map):
        self.map = map
        self.x = x
        self.y = y
        self.table = QTable(0.7, 5) #Left_Right_Top_Bottom_TresurePickup

    def move(self):        
        map = self.map

        current_state = self.get_state()
        print(current_state, self.table.get(current_state))

        if map.is_valid_position(self.x - 1, self.y):
            self.x -= 1

    def get_state(self):
        left_tile   = map.get_tile(self.x - 1, self.y) if map.is_valid_position(self.x - 1, self.y) else TileType.Wall
        right_tile  = map.get_tile(self.x + 1, self.y) if map.is_valid_position(self.x + 1, self.y) else TileType.Wall
        top_tile    = map.get_tile(self.x, self.y - 1) if map.is_valid_position(self.x, self.y - 1) else TileType.Wall
        bottom_tile = map.get_tile(self.x, self.y + 1) if map.is_valid_position(self.x, self.y + 1) else TileType.Wall
        center_tile = map.get_tile(self.x, self.y) if map.is_valid_position(self.x, self.y) else TileType.Wall
        tresure_dir = self.get_direction_to_tresure()

        key = f"{left_tile.name}_{right_tile.name}_{top_tile.name}_{bottom_tile.name}_{center_tile.name}_{tresure_dir.name if tresure_dir is not None else None}"
        return key
        
    def get_direction_to_tresure(self) -> Direction | None:
        def get_tresure_location():
            for x in range(self.map.size_x):
                for y in range(self.map.size_y):
                    tile = self.map.get_tile(x, y)
                    if tile == TileType.Tresure:
                        return x, y
            return None
        
        location = get_tresure_location()
        if location is None:
            return None
        
        tresure_x, tresure_y = location
        distance_x = abs(self.x - tresure_x)
        distance_y = abs(self.y - tresure_y)
        if distance_x == 0 and distance_y == 0:
            return None
        if distance_x > distance_y:
            return Direction.Left if self.x > tresure_x else Direction.Right
        else:
            return Direction.Top if self.y > tresure_y else Direction.Bottom
