from .vector import *
from random import *
from math import *

class kepler:

    def __init__(self):

        self.name = 'Kepler'
        self.parameters = [
            {'pName':'Central mass', 'pType':'numeric', 'default':1, 'tooltip':'Mass of the main body holding the system together'},
            {'pName':'Other masses', 'pType':'numeric', 'default':1, 'tooltip':'Mass of each other body orbiting the central mass' },
            {'pName':'Total number', 'pType':'int', 'default':2, 'tooltip':'Total number of masses in this system, including central'},
            {'pName':'Mean distance', 'pType':'numeric', 'default':1, 'tooltip':'Average distance from central body to others.\nIs gamma distributed'},
            {'pName':'Centre', 'pType':'vector', 'default':vector(0,0,0), 'tooltip':'Initial position of the central mass'},
            {'pName':'Net velocity','pType':'vector','default':vector(0,0,0),'tooltip':'Initial net velocity of group.\nOnly important for relative velocity\nbetween different distributions as\nthe total momentum is set to zero.'},
            {'pName':'Axis','pType':'vector','default':vector(0,0,1),'tooltip':'Axis about which the\ndistribution is symmetric.'}]

    def run(self, imports, dist, G):

        m0 = float(imports[0])
        m = float(imports[1])
        n = int(imports[2])
        dist.n += n
        r0 = float(imports[3])
        origin = strToVector(imports[4])
        v0 = strToVector(imports[5])
        R = norm(strToVector(imports[6]))
        Rp = perp(R)

        dist.part.append({
            'pos-1':origin,
            'pos':origin,
            'mass':m0,
            'vel':v0,
            'acc':vector(0,0,0),
            'num':dist.index
            })
        dist.index += 1

        for i in range(0,n-1):
            
            theta = uniform(0,2*pi)
            r = Rp * r0
            r.rotate(theta,R)
            r *= gammavariate(2,1)
            M = m0 + m*n*(1-(mag(r)/r0 + 1)*exp(-mag(r)/r0))
            dist.part.append({
                'pos-1':r+origin,
                'pos':r+origin,
                'mass':m,
                'vel':cross(r/mag(r),R)*pow(G*M/mag(r),0.5) + v0,
                'acc':vector(0,0,0),
                'num':dist.index
                })
            dist.index += 1

