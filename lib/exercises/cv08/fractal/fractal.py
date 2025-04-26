
class Fractal:
    def __init__(self, width, height, max_iter=100):
        self.width = width
        self.height = height
        self.max_iter = max_iter
        self.image = None
        self.x_min = -2.0
        self.x_max = 1.0
        self.y_min = -1.5
        self.y_max = 1.5
        
    def compute(self):
        pass
        
    def zoom(self, x, y, zoom_factor):
        x_range = self.x_max - self.x_min
        y_range = self.y_max - self.y_min
        
        cx = self.x_min + x / self.width * x_range
        cy = self.y_min + y / self.height * y_range
        
        new_x_range = x_range * zoom_factor
        new_y_range = y_range * zoom_factor
        
        self.x_min = cx - new_x_range / 2
        self.x_max = cx + new_x_range / 2
        self.y_min = cy - new_y_range / 2
        self.y_max = cy + new_y_range / 2
        
        self.compute()
        
    def get_image(self):
        return self.image