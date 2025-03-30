import numpy as np

class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        self.weights = None
        self.pattern_weights = None
    
    def train(self, patterns):
        self.weights = np.zeros((self.size, self.size))
        self.pattern_weights = []
        
        for pattern in patterns:
            pattern = np.where(pattern.flatten() > 0, 1, -1).reshape(-1, 1)
            pattern_weight = pattern @ pattern.T
            self.weights += pattern_weight
            self.pattern_weights.append(pattern_weight)
        np.fill_diagonal(self.weights, 0)
        
    def recover(self, pattern, steps=5, async_method=False):
        pattern = pattern.flatten()

        if async_method:
            for _ in range(steps):
                for i in range(self.size):
                    pattern[i] = np.sign(np.dot(self.weights[i], pattern))
        else:
            for _ in range(steps):
                pattern = np.sign(self.weights @ pattern)
        
        return pattern.reshape(int(np.sqrt(self.size)), -1)