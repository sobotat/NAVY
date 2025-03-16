import numpy as np
from lib.utils.progressbar import ProgressBar
from lib.exercises.activation_function import ActivationFunction

class Neuron:
    def __init__(self, num_inputs, random_state):
        np.random.seed(random_state)
        self.weights = np.random.uniform(-1, 1, num_inputs)
        self.bias = np.random.uniform(-1, 1)
        
        self.input_values = []
        self.output = 0
        self.delta = 0
    
    def feedforward(self, X_i, activation_function):
        func = ActivationFunction.get_activation_function(activation_function)

        self.input_values = np.array(X_i)
        total_input = np.dot(self.weights, self.input_values) + self.bias
        self.output = func(total_input)
        return self.output


class Layer:
    def __init__(self, num_neurons, num_inputs, activation_function='sigmoid'):
        self.num_neurons = num_neurons
        self.num_inputs = num_inputs
        self.activation_function = activation_function

        self.neurons = []

    def create_neurons(self, random_state):
        self.neurons = [Neuron(self.num_inputs, random_state) for _ in range(self.num_neurons)]
    
    def feedforward(self, inputs):
        return np.array([neuron.feedforward(inputs, self.activation_function) for neuron in self.neurons])


class NeuralNetwork:
    def __init__(self, layers, learning_rate = 0.1):
        self.learning_rate = learning_rate
        self.layers = layers
        self.total_errors = []
    
    def feedforward(self, X_i):
        for layer in self.layers:
            X_i = layer.feedforward(X_i)
        return X_i
    
    def backpropagate(self, y, predicted):        
        for i in reversed(range(len(self.layers))):
            layer = self.layers[i]
            func = ActivationFunction.get_activation_derivative_function(layer.activation_function)
            
            # Výpočet chyby
            is_last_layer = (i == len(self.layers) - 1)
            if is_last_layer:
                # Výpočet pro poslední vrstvu
                errors = y - predicted
                for j, neuron in enumerate(layer.neurons):
                    neuron.delta = errors[j] * func(neuron.output)
            else:
                # Výpočet pro hidden vrstvy
                next_layer = self.layers[i + 1]
                for j, neuron in enumerate(layer.neurons):
                    error = np.sum([next_layer.neurons[k].weights[j] * next_layer.neurons[k].delta for k in range(len(next_layer.neurons))])
                    neuron.delta = error * func(neuron.output)

            # Aktualizace Váh
            for j, neuron in enumerate(layer.neurons):
                neuron.weights += self.learning_rate * neuron.delta * neuron.input_values
                neuron.bias += self.learning_rate * neuron.delta
    
    def fit(self, X, y, epochs, random_state=10, verbose=True):
        np.random.seed(random_state)

        for layer in self.layers:
            layer.create_neurons(random_state)

        self.total_errors = []

        if verbose:
            p = ProgressBar(epochs, message='Running Epochs')

        for epoch in range(epochs):
            total_error = 0
            for X_i, y_i in zip(X, y):
                predicted = self.feedforward(X_i)                
                self.backpropagate(y_i, predicted)
                total_error += np.sum(0.5 * (y_i - predicted) ** 2)
                
            self.total_errors.append(total_error)

            if verbose:
                p.update(epoch + 1, message_behind=f" - TError[{total_error:5f}]")
    
    def predict(self, X):
        predicted = []
        for item in X:
            pred_y = self.feedforward(item)
            predicted.append(int(np.round(pred_y)))
        return np.array(predicted)
    
