from lib.exercises.cv09.objects.fractal_terrain import FractalTerrain

class TerrainGenerator:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.terrain = FractalTerrain()
        
    def generate_layer(self, start_x, start_y, end_x, end_y, iterations, color):
        segments = self.terrain.generate_layer(start_x, start_y, end_x, end_y, iterations)
        layer = self.terrain.add_layer(segments, color)
        self.draw_layer(layer)
        return layer
    
    def draw_layer(self, layer):
        for segment in layer.segments:
            line_id = self.canvas.create_line(
                segment.start_x, segment.start_y,
                segment.end_x, segment.end_y,
                fill=layer.color, width=2, tags=f"layer_{len(self.terrain.layers)}"
            )
            layer.canvas_items.append(line_id)
        
        if layer.segments:
            self.fill_terrain_area(layer)
    
    def fill_terrain_area(self, layer):
        sorted_segments = sorted(layer.segments, key=lambda seg: min(seg.start_x, seg.end_x))
        
        terrain_profile = {}
        for segment in sorted_segments:
            if segment.start_x != segment.end_x:
                if segment.start_x < segment.end_x:
                    x1, y1 = segment.start_x, segment.start_y
                    x2, y2 = segment.end_x, segment.end_y
                else:
                    x1, y1 = segment.end_x, segment.end_y
                    x2, y2 = segment.start_x, segment.start_y
                
                slope = (y2 - y1) / (x2 - x1)
                
                for x in range(int(x1), int(x2) + 1):
                    y = y1 + slope * (x - x1)
                    if x not in terrain_profile or y < terrain_profile[x]:
                        terrain_profile[x] = y
        
        bottom_y = self.height
        
        sorted_points = [(x, y) for x, y in terrain_profile.items()]
        sorted_points.sort(key=lambda p: p[0])
        
        polygon_points = []
        polygon_points.extend(sorted_points)
        
        right_most_x = sorted_points[-1][0]
        left_most_x = sorted_points[0][0]
        polygon_points.append((right_most_x, bottom_y))
        polygon_points.append((left_most_x, bottom_y))
        
        if len(polygon_points) >= 3:
            flat_points = [coord for point in polygon_points for coord in point]
            polygon_id = self.canvas.create_polygon(
                flat_points, fill=layer.color, outline="", 
                tags=f"layer_{len(self.terrain.layers)}", stipple="gray12"
            )
            layer.canvas_items.append(polygon_id)
    
    def remove_last_layer(self):
        layer = self.terrain.remove_last_layer()
        if layer:
            for item_id in layer.canvas_items:
                self.canvas.delete(item_id)
            return True
        return False
    
    def clear_all(self):
        self.canvas.delete("all")
        self.terrain.layers = []