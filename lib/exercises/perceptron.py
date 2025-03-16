import numpy as np
from lib.utils.progressbar import ProgressBar
from lib.exercises.activation_function import ActivationFunction    

class Perceptron:

    def __init__(self, epochs, activation_function='signum', learning_rate=0.01):
        self.epochs = epochs
        self.activation_function = ActivationFunction.get_activation_function(activation_function)
        self.learning_rate = learning_rate

        self.weights = None
        self.bias = None

    def fit(self, X, y, random_state=13, verbose=True):
        np.random.seed(random_state)

        _, number_of_features = X.shape
        self.weights = np.random.uniform(-1, 1, number_of_features)
        self.bias = 0

        if verbose:
            p = ProgressBar(self.epochs, message='Running Epochs')

        for epoch in range(self.epochs):
            for i, item in enumerate(X):                
                guess_answer = self.activation_function(np.dot(item, self.weights) + self.bias)
                correct_answer = y[i]
                error = correct_answer - guess_answer

                # print(guess_answer, correct_answer, error, self.weights, self.bias)
                
                for wi in range(number_of_features):
                    self.weights[wi] += error * item[wi] * self.learning_rate
                self.bias += error * self.learning_rate                
            
            if verbose:
                p.update(epoch + 1)
        return        

    def predict(self, X):
        y_pred = []
        for item in X:
            quess = self.activation_function(np.dot(item, self.weights) + self.bias)
            y_pred.append(int(np.round(quess)))
        return np.array(y_pred)
