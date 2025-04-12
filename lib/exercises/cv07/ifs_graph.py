import pyvista as pv
import numpy as np

class IFSGraph:
    def __init__(self):
        self.plotter = pv.Plotter()
    
    def display(self, points:np.ndarray, point_size=1.0, color='lightgreen', title='IFS Fraktál', background_color='white'):
        cloud = pv.PolyData(points)
        self.plotter.background_color = background_color

        self.plotter.add_points(cloud, color=color, point_size=point_size, render_points_as_spheres=True)
        self.plotter.add_title(title, font_size=16)

        self.plotter.show_axes()
        self.plotter.show()