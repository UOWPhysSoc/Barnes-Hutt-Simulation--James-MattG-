from .vector import *
from random import *
from math import *

class kepler:

    def __init__(self):

        self.name = 'Kepler'
        self.parameters = [
            {'pName':'Central mass', 'pType':'numeric', 'default':1},
            {'pName':'Other masses', 'pType':'numeric', 'default':1},
            {'pName':'Total number', 'pType':'int', 'default':2},
            {'pName':'Mean distance', 'pType':'numeric', 'default':1},
            {'pName':'Centre', 'pType':'vector', 'default':vector(0,0,0)}]

    def run(self, imports, dist):

        m0 = float(imports[0])
        m = float(imports[1])
        n = int(imports[2])
        dist.n += n
        r0 = float(imports[3])
        origin = strToVector(imports[4])

        dist.part.append({
            'pos-1':origin,
            'pos':origin,
            'mass':m0,
            'vel':vector(0,0,0),
            'acc':vector(0,0,0),
            'num':dist.index
            })
        dist.index += 1

        for i in range(0,int(imports[2])-1):
            
            theta = uniform(0,2*pi)
            r = vector(r0,0,0)
            r.rotate(theta,vector(0,0,1))
            r *= gammavariate(2,1)
            M = m0 + m*n*(1-(mag(r)/r0 + 1)*exp(-mag(r)/r0))
            dist.part.append({
                'pos-1':r,
                'pos':r,
                'mass':m,
                'vel':cross(r/mag(r),vector(0,0,1))*pow(M/mag(r),0.5),
                'acc':vector(0,0,0),
                'num':dist.index
                })
            dist.index += 1

