#1 python3



DISTRIBUTIONS = [
            {'fname':'twoBody', 'name':'Two Body'},
            {'fname':'kepler', 'name':'Kepler System'},
            {'fname':'uniformSphere', 'name':'Uniform Sphere'},
            {'fname':'MN','name':'Miyamoto Nagai'}
            ]
        
class distributions:

    def __init__(self, G):
        self.part = []
        self.n = 0
        self.index = 0
        self.G = G

    def call(self):

        return self.part
