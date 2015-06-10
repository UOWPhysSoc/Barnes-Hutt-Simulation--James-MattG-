from .vector import *

class twoBody:

    def __init__(self):

        self.name = 'Two Body'
        self.parameters = [
            {'pName':'Mass 1', 'pType':'numeric', 'default':1},
            {'pName':'Mass 2', 'pType':'numeric', 'default':1},
            {'pName':'Separation', 'pType':'numeric', 'default':1},
            {'pName':'First mass position', 'pType':'vector','default':vector(0,0,0)}]

    def run(self, list_of_stuff, dist):

        mass1 = float(list_of_stuff[0])
        mass2 = float(list_of_stuff[1])
        r = vector(1,0,0)*float(list_of_stuff[2])
        r1 = strToVector(list_of_stuff[3])

        dist.n += 2

        mu = mass1 * mass2 /(mass1 + mass2)
        dist.part.append({
            'pos-1':r1,
            'pos':r1,
            'mass':mass1,
            'vel':sqrt(mass2**2/(mag(r)*(mass1 + mass2))) * vector(0,1,0),
            'acc':vector(0,0,0),
            'num':dist.index
            })
        dist.index += 1
        dist.part.append({
            'pos-1':r+r1,
            'pos':r+r1,
            'mass':mass2,
            'vel':sqrt(mass1**2/(mag(r)*(mass1 + mass2))) * vector(0,-1,0),
            'acc':vector(0,0,0),
            'num':dist.index
            })
        dist.index += 1

        
