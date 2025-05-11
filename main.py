import numpy as np
import matplotlib.pyplot as plt

from lib.utils.menu import Menu, Color
from lib.exercises.cv01.perceptron import Perceptron
from lib.exercises.cv02.neural_network import NeuralNetwork, Layer
from lib.exercises.cv03.hopfield_app import HopfieldApp
from lib.exercises.cv04.qlearning_app import QLearningApp
from lib.exercises.cv06.l_system_app import LSystemApp
from lib.exercises.cv07.ifs_app import IFSApp
from lib.exercises.cv08.fractal_app import FractalApp
from lib.exercises.cv09.fractal_terrain_app import FractalTerrainApp
import lib.exercises.cv10.logistic_map as logistic_map
from lib.exercises.cv12.forest_fire_app import ForestFireApp

def perceptron_test():
    np.random.seed(13)
    X = np.random.uniform(-10, 10, (100, 2))
    y = np.where(X[:, 1] > 3 * X[:, 0] + 2, 1, np.where(X[:, 1] < 3 * X[:, 0] + 2, -1, 0))
    
    selected_function = Menu('Select Activation Function', ['signum', 'sigmoid', 'relu'], headingColor=Color.WHITE, selectedColor=Color.WHITE).select(False)
    if selected_function == None:
        return

    model = Perceptron(epochs=100, activation_function=selected_function)
    model.fit(X, y)
    predicted = model.predict(X)

    x_line = np.linspace(-10, 10, 100)
    y_line = 3 * x_line + 2
    plt.plot(x_line, y_line, color='black', label='y = 2x + 3')

    slope = -model.weights[0] / model.weights[1]
    intercept = -model.bias / model.weights[1]
    y_model = slope * x_line + intercept
    plt.plot(x_line, y_model, color='red', linestyle='--', label='Model Decision Boundary')

    plt.scatter(X[:, 0], X[:, 1], c=predicted, alpha=0.7)    
    plt.xlim(-10.5, 10.5)
    plt.ylim(-10.5, 10.5)
    plt.show()

def xor_problem_test():
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])    
    y = np.array([0, 1, 1, 0])

    layers = [
        Layer(2, 2, "sigmoid"),
        Layer(1, 2, "sigmoid")
    ]
    
    model = NeuralNetwork(layers)
    model.fit(X, y, epochs=20000)
    predicted = model.predict(X)
    
    for i, item in enumerate(X):
        print(f'{item} = {y[i]} -> Predicted [{predicted[i]}]')

    def plot_total_error(model):
        plt.plot(model.total_errors, label='Total Error')
        plt.xlabel('Epoch')
        plt.ylabel('Total Error')
        plt.title('Total Error per Epoch')
        plt.show()

    def plot_decision_boundaries(model, X, y):
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                            np.arange(y_min, y_max, 0.1))
        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        plt.contourf(xx, yy, Z, alpha=0.8)
        plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', marker='o')
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.title('Decision Boundary of Neural Network')
        plt.show()

    plot_total_error(model)
    plot_decision_boundaries(model, X, y)

def main():
    mainMenu = Menu("Select Exercise", [
        'Perceptron',
        'XOR problem',
        'Hopfield',
        'QLearning',
        'LSystem',
        'IFS',
        'TEA',
        'Fractal Terrain Generation',
        'Logistic Map',
        'Forest Fire Cellular Automaton',
        'Exit'
    ])

    while(True):
        try:
            match(mainMenu.select()):
                case 'perceptron':
                    perceptron_test()
                case 'xor-problem':
                    xor_problem_test()
                case 'hopfield':
                    HopfieldApp().run()
                case 'qlearning':
                    QLearningApp().run()
                case 'lsystem':
                    LSystemApp().run()
                case 'ifs':
                    IFSApp().run()
                case 'tea':
                    FractalApp()
                case 'fractal-terrain-generation':
                    FractalTerrainApp()
                case 'logistic-map':
                    logistic_map.run()
                case 'forest-fire-cellular-automaton':
                    ForestFireApp()
                case None | 'exit':
                    break
        except KeyboardInterrupt:
            print("Stopped")
    
if __name__ == "__main__":
    main()
    print('Exiting ...')