
class QTable:

    def __init__(self, epsilon, lenght):
        self.epsilon = epsilon
        self.default_lenght = lenght

        self._table = {}

    def get(self, key):
        if key in self._table:
            return self._table[key]
        return [0] * self.default_lenght
    
    def set(self, key, data):
        self._table[key] = data


    