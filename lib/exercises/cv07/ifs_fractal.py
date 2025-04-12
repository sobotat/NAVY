import random
import numpy as np
from tqdm import tqdm
from typing import List, Tuple

class IFSFractal:
    def __init__(self, transformations: List[Tuple]):
        self.transformations = transformations
        self.num_transforms = len(transformations)
    
    def apply_transformation(self, point:np.ndarray, transform_idx:int) -> np.ndarray:
        a, b, c, d, e, f, g, h, i, j, k, l = self.transformations[transform_idx]
        x, y, z = point
        
        x_new = a * x + b * y + c * z + j
        y_new = d * x + e * y + f * z + k
        z_new = g * x + h * y + i * z + l
        
        return np.array([x_new, y_new, z_new])
    
    def generate_points(self, iterations:int, starting_point:np.ndarray=None) -> np.ndarray:
        if starting_point is None:
            current_point = np.array([0.0, 0.0, 0.0])
        else:
            current_point = starting_point
        
        points = np.zeros((iterations, 3))
        
        for i in tqdm(range(iterations), desc="Generating Point", colour='green'):
            transform_idx = random.choices(range(self.num_transforms), k=1)[0]            
            current_point = self.apply_transformation(current_point, transform_idx)
            
            points[i] = current_point
        
        return points


