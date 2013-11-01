
class AdventureScorer:
    def __init__(self):
        self._investments = 0
        self._score = -20

    def score(self):
        return self._score * self._investments

    def put(self, value):
        if self._investments == 0:
            self._investments += 1

        if value == 'i':
            self._investments += 1
        else:
            self._score += value
        
