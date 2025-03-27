from lib.exercises.cv04.q_table import QTable
from lib.exercises.cv04.map import Map, TileType
from lib.exercises.cv04.direction import Direction
from enum import Enum
import random

class Action(Enum):
    GoLeft = 0
    GoRight = 1
    GoTop = 2
    GoBottom = 3
    PickupTresure = 4
actions = [Action.GoLeft, Action.GoRight, Action.GoTop, Action.GoBottom, Action.PickupTresure]

class QLearningPlayer:

    def __init__(self, x, y, table:QTable, map:Map, learning_rate=0.1):
        self.map = map
        self.x = x
        self.y = y
        self.spawn_x = x
        self.spawn_y = y

        self.table = table #Left_Right_Top_Bottom_TresurePickup
        self.learning_rate = learning_rate

        self.last_state = self.get_state()
        self.last_action = None

    def update(self):
        map = self.map

        if self.map.get_tile(self.x, self.y) == TileType.Trap:
            self.x = self.spawn_x
            self.y = self.spawn_y
            print("Stepped on Trap")
            return

        current_state = self.get_state()
        current_state_data = self.table.get(current_state)
        print(current_state, current_state_data)

        selected_action = None
        selected_by_random = False
        if random.random() <= self.table.epsilon:
            selected_action = random.choice(actions)
            selected_by_random = True
        else:            
            selected_value = -1
            for i, s_value in enumerate(current_state_data):
                if s_value > selected_value:
                    selected_action = actions[i]
                    selected_value = s_value

        max_value = current_state_data[0]
        for value in current_state_data:
            if value > max_value:
                max_value = value

        # print(f"Selected [{selected_action}] by Random [{selected_by_random}]")

        if self.last_action != None:
            reward = self.get_reward(self.last_action, self.last_state)

            last_state_data = self.table.get(self.last_state)
            last_value = last_state_data[actions.index(self.last_action)]            
            new_value = (1 - self.learning_rate) * last_value + self.learning_rate * (reward + max_value * 0.6)
            last_state_data[actions.index(self.last_action)] = new_value
            self.table.set(self.last_state, last_state_data)

            print(f"Rewared [{reward}] for [{self.last_state}] with [{self.last_action.name}]")

        self.run_action(selected_action)

        self.last_state = current_state
        self.last_action = selected_action
        
    def get_reward(self, last_action, last_state) -> int:
        tile_left, tile_right, tile_top, tile_bottom, tile_center, tresure_dir = last_state.split('_')
        tile_left, tile_right, tile_top, tile_bottom, tile_center = TileType[tile_left], TileType[tile_right], TileType[tile_top], TileType[tile_bottom], TileType[tile_center]
        tresure_dir = Direction[tresure_dir] if tresure_dir != "None" else None

        reward = -1
        if last_action == Action.GoLeft and tresure_dir == Direction.Left:
            reward += 5
        if last_action == Action.GoRight and tresure_dir == Direction.Right:
            reward += 5
        if last_action == Action.GoTop and tresure_dir == Direction.Top:
            reward += 5
        if last_action == Action.GoBottom and tresure_dir == Direction.Bottom:
            reward += 5
        
        if last_action == Action.PickupTresure and tile_center == TileType.Tresure:
            reward += 10
        elif last_action == Action.PickupTresure and tile_center != TileType.Tresure:
            reward -= 10

        if last_action == Action.GoLeft and tile_left in [TileType.Trap, TileType.Wall]:
            reward -= 5
        if last_action == Action.GoRight and tile_right in [TileType.Trap, TileType.Wall]:
            reward -= 5
        if last_action == Action.GoTop and tile_top in [TileType.Trap, TileType.Wall]:
            reward -= 5
        if last_action == Action.GoBottom and tile_bottom in [TileType.Trap, TileType.Wall]:
            reward -= 5

        return reward

    def run_action(self, action:Action):
        match(action):
            case Action.GoLeft:
                if self.map.is_valid_position(self.x - 1, self.y) and self.map.get_tile(self.x - 1, self.y) != TileType.Wall:
                    self.x -= 1
            case Action.GoRight:
                if self.map.is_valid_position(self.x + 1, self.y) and self.map.get_tile(self.x + 1, self.y) != TileType.Wall:
                    self.x += 1
            case Action.GoTop:
                if self.map.is_valid_position(self.x, self.y - 1) and self.map.get_tile(self.x, self.y - 1) != TileType.Wall:
                    self.y -= 1
            case Action.GoBottom:
                if self.map.is_valid_position(self.x, self.y + 1) and self.map.get_tile(self.x, self.y + 1) != TileType.Wall:
                    self.y += 1
            case Action.PickupTresure:
                if self.map.get_tile(self.x, self.y) == TileType.Tresure:
                    self.map.set_tile(self.x, self.y, TileType.Empty)
                    print("Tresure Picked")
                else:
                    print("No Tresure to Pickup")

    def get_state(self) -> str:
        map = self.map

        left_tile   = map.get_tile(self.x - 1, self.y) if map.is_valid_position(self.x - 1, self.y) else TileType.Wall
        right_tile  = map.get_tile(self.x + 1, self.y) if map.is_valid_position(self.x + 1, self.y) else TileType.Wall
        top_tile    = map.get_tile(self.x, self.y - 1) if map.is_valid_position(self.x, self.y - 1) else TileType.Wall
        bottom_tile = map.get_tile(self.x, self.y + 1) if map.is_valid_position(self.x, self.y + 1) else TileType.Wall
        center_tile = map.get_tile(self.x, self.y) if map.is_valid_position(self.x, self.y) else TileType.Wall
        tresure_dir = self.get_direction_to_tresure()

        state = f"{left_tile.name}_{right_tile.name}_{top_tile.name}_{bottom_tile.name}_{center_tile.name}_{tresure_dir.name if tresure_dir is not None else None}"
        return state
    
        
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
