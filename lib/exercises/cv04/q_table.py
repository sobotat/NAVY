
class QTable:

    def __init__(self, epsilon, action_count):
        self.epsilon = epsilon
        self.action_count = action_count

        self._table = {}

    def get(self, key):
        if key in self._table:
            return self._table[key]
        return [0] * self.action_count
    
    def set(self, key, data):
        self._table[key] = data


    