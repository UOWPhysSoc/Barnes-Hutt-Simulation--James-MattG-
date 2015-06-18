from .vector import *
from math import *
from random import *

class uniformSphere:  # MAKE SURE TO CHANGE THIS! AND ADD THE SAME FUNCTION
                   # NAME TO BARNESDIST_GUI.PY AND __INIT__.PY  

    def __init__(self):

        # Text name goes here. 'None' emmits from being imported
        self.name = 'Uniform Sphere'

        self.parameters = [
            {'pName':'Number', 'pType':'int', 'default':1, 'tooltip':'Number of masses in sphere'},
            {'pName':'Mass', 'pType':'numeric', 'default':1, 'tooltip':'Mass of each body in the sphere.'},
            {'pName':'Radius', 'pType':'numeric', 'default':1, 'tooltip':'Radius that all the mass is\ncontained within.'},
            {'pName':'Centre', 'pType':'vector', 'default':vector(0,0,0), 'tooltip':'Initial position of the central mass'},
            {'pName':'Net velocity','pType':'vector','default':vector(0,0,0),'tooltip':'Initial net velocity of group.\nOnly important for relative velocity\nbetween different distributions as\nthe total momentum is set to zero.'},
            ]

    def run(self, imports, dist, G):

        n = int(imports[0])
        m = float(imports[1])
        R = float(imports[2])  # radius of sphere
        r1 = strToVector(imports[3])    # centre of sphere
        v0 = strToVector(imports[4])    # net v
        vs = sqrt(G*m*n/R**3)   # scale velocity

        dist.n += n

        for i in range(0,n):
            r0 = R*pow(uniform(0,1),1.0/3)
            theta = acos(uniform(-1,1))
            phi = uniform(0,2*pi)
            r = r0*vector(sin(theta)*sin(phi),sin(theta)*cos(phi),cos(theta))
            vhat = perp(r)
            vhat.rotate(uniform(0,2*pi),r)
            dist.part.append({
                'pos-1':r1+r,
                'pos':r1+r,
                'mass':m,
                'vel':vhat*vs*mag(r0),
                'acc':vector(0,0,0),
                'num':dist.index
                })
            dist.index += 1

        
