import math

class TerrainSegment:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.children = []
        
    def midpoint(self):
        mid_x = (self.start_x + self.end_x) / 2
        mid_y = (self.start_y + self.end_y) / 2
        return mid_x, mid_y
    
    def length(self):
        return math.sqrt((self.end_x - self.start_x)**2 + (self.end_y - self.start_y)**2)