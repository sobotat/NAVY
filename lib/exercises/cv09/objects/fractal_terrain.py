import random
from lib.exercises.cv09.objects.terrain_segment import TerrainSegment
from lib.exercises.cv09.objects.terrain_layer import TerrainLayer

class FractalTerrain:
    def __init__(self):
        self.layers = []
        
    def generate_layer(self, start_x, start_y, end_x, end_y, iterations, randomness=0.15, roughness=0.8):
        root_segment = TerrainSegment(start_x, start_y, end_x, end_y)
        segments = [root_segment]
        
        for i in range(iterations):
            new_segments = []
            current_randomness = randomness * (roughness ** i)
            
            for segment in segments:
                mid_x, mid_y = segment.midpoint()
                
                # Výpočet kolmého vektoru pro posunutí bodu
                dx = segment.end_x - segment.start_x
                dy = segment.end_y - segment.start_y
                length = segment.length()
                
                # Náhodné posunutí středového bodu kolmo k úsečce
                if length > 0:
                    perpendicular_x = -dy / length
                    perpendicular_y = dx / length
                    
                    direction = 1 if random.random() > 0.5 else -1
                    random_offset = direction * random.random() * current_randomness * length
                    
                    new_mid_x = mid_x + perpendicular_x * random_offset
                    new_mid_y = mid_y + perpendicular_y * random_offset
                    
                    left_segment = TerrainSegment(segment.start_x, segment.start_y, new_mid_x, new_mid_y)
                    right_segment = TerrainSegment(new_mid_x, new_mid_y, segment.end_x, segment.end_y)
                    
                    new_segments.append(left_segment)
                    new_segments.append(right_segment)
                    
                    segment.children = [left_segment, right_segment]
                else:
                    new_segments.append(segment)
            
            segments = new_segments
        
        return segments
    
    def add_layer(self, segments, color):
        layer = TerrainLayer(segments, color)
        self.layers.append(layer)
        return layer
    
    def remove_last_layer(self):
        if self.layers:
            return self.layers.pop()
        return None
