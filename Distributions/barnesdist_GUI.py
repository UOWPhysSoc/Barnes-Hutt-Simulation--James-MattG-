#1 python3
from vector import *



DISTRIBUTIONS = [
            {'fname':'twoBody', 'name':'Two Body'},
            {'fname':'kepler', 'name':'Kepler System'}
            ]
        
class distributions:

    def __init__(self, G):
        self.part = []
        self.n = 0
        self.index = 0
        self.G = G

    def call(self):

        return self.part
