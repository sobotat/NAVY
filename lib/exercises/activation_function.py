import numpy as np

class ActivationFunction:
    @staticmethod
    def signum(X):
        return np.sign(X)
    
    @staticmethod
    def sigmoid(X):
        X = np.clip(X, -500, 500)
        return 1 / (1 + np.exp(-X))
    
    @staticmethod
    def relu(X):
        return np.maximum(0, X)
    
    @staticmethod
    def derivative_signum(X):
        return np.zeros_like(X)
    
    @staticmethod
    def derivative_sigmoid(X):
        sigmoid_X = ActivationFunction.sigmoid(X)
        return sigmoid_X * (1 - sigmoid_X)
    
    @staticmethod
    def derivative_relu(X):
        return np.where(X > 0, 1, 0)
    
    @staticmethod
    def get_activation_function(name):
        return {
            'signum': ActivationFunction.signum, 
            'sigmoid': ActivationFunction.sigmoid, 
            'relu': ActivationFunction.relu
        }[name]
    
    @staticmethod
    def get_activation_derivative_function(name):
        return {
            'signum': ActivationFunction.derivative_signum, 
            'sigmoid': ActivationFunction.derivative_sigmoid, 
            'relu': ActivationFunction.derivative_relu
        }[name]