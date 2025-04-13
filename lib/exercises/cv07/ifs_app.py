from lib.exercises.cv07.ifs_fractal import IFSFractal
from lib.exercises.cv07.ifs_graph import IFSGraph

class IFSApp():

    def run(self):
        IFSApp.model1()
        IFSApp.model2()

    def model1():
        transformations = [
            (0.00, 0.00, 0.01, 0.00, 0.26, 0.00, 0.00, 0.00, 0.05, 0.00, 0.00, 0.00),
            (0.20, -0.26, -0.01, 0.23, 0.22, -0.07, 0.07, 0.00, 0.24, 0.00, 0.80, 0.00),
            (-0.25, 0.28, 0.01, 0.26, 0.24, -0.07, 0.07, 0.00, 0.24, 0.00, 0.22, 0.00),
            (0.85, 0.04, -0.01, -0.04, 0.85, 0.09, 0.00, 0.08, 0.84, 0.00, 0.80, 0.00)
        ]
        
        fractal = IFSFractal(transformations)        
        points = fractal.generate_points(iterations=5000)
        
        graph = IFSGraph()
        graph.display(points, point_size=15, title="Model 1")


    def model2():
        transformations = [
            (0.05, 0.00, 0.00, 0.00, 0.60, 0.00, 0.00, 0.00, 0.05, 0.00, 0.00, 0.00),
            (0.45, -0.22, 0.22, 0.22, 0.45, 0.22, -0.22, 0.22, -0.45, 0.00, 1.00, 0.00),
            (-0.45, 0.22, -0.22, 0.22, 0.45, 0.22, 0.22, -0.22, 0.45, 0.00, 1.25, 0.00),
            (0.49, -0.08, 0.08, 0.08, 0.49, 0.08, 0.08, -0.08, 0.49, 0.00, 2.00, 0.00)
        ]
        
        fractal = IFSFractal(transformations)
        points = fractal.generate_points(iterations=5000)
        
        graph = IFSGraph()
        graph.display(points, point_size=15, title="Model 2")