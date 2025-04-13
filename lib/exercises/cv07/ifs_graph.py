import matplotlib.pyplot as plt
import numpy as np

class IFSGraph:
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
    
    def display(self, points:np.ndarray, point_size=1.0, color='lightgreen', title='IFS Fraktál', background_color='white'):
        x = points[:, 0]
        y = points[:, 1]
        z = points[:, 2] if points.shape[1] > 2 else np.zeros_like(x)
        
        self.fig.patch.set_facecolor(background_color)
        self.ax.set_facecolor(background_color)
        
        self.ax.scatter(x, y, z, s=point_size, c=color, marker='o')
        
        self.ax.set_title(title, fontsize=16)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        
        plt.tight_layout()
        plt.show()