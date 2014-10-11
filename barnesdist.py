'''
Distribution function module for Barnes-Hutt n-body simulation developed by Matt Griffiths and James Archer.
Example distribution written by Matt Griffiths, list idea concieved by James Archer.
Special thanks to Matt Sanderson for ideas regarding distribution implementation.

Avaliable for use under a GPL v3 licence.
'''

#Import dependent libraries
from random import *
from visual import *

class distributions():

    def __init__(self, dist_name):
        self.dist_name = dist_name
        self.part = []
        self.n = 0

    def call(self):
        for i in self.dist_name:
            getattr(self, i)()
        return self.part

    def uniform_cube(self):
        self.n += int(input('Number of bodies: '))
        #x_range = float(input('X range: '))
        #y_range = float(input('Y range: '))
        #z_range = float(input('Z range: '))
        x_range = 10
        y_range = 10
        z_range = 10
        for i in range(self.n):
            r = random_vect(x_range,y_range,z_range)
            self.part.append({
                'pos-1':r,
                'pos':r,
                'mass':1/self.n,
                'vel':random_vect(x_range*0.1,y_range*0.1,z_range*0.1),
                'acc':vector(0,0,0),
                'num':i
                })


    def ring(index,posd,veld,centralmass):
#Ring type distribution around a massive central body

        n = int(input('Number of bodies: '))
        posd
        #For first index, create central body
        if index == 0:
            return({
                    'pos-1':vector(0,0,0),
                    'pos':vector(0,0,0),
                    'mass':centralmass,
                    'vel':vector(0,0,0),
                    'acc':vector(0,0,0),
                    'num':0
                })

        #For further indexes, add smaller orbiting bodies to a ring
        else:
            zunit = vector(0,0,1)
            tempvect = vector(0,0,0)
            temptheta = uniform(0,2*pi)
            rad = gauss(posd,posd/10)
            tempvect.x = rad*math.cos(temptheta)
            tempvect.y = rad*math.sin(temptheta)
            tempvect.z = gauss(posd/10,posd/10)
            tempvel =  math.sqrt(centralmass/posd)*(tempvect/abs(tempvect)).cross(zunit) 
            tempm = 1      
            return  ({
                    'pos-1':tempvect,
                    'pos':vector(0,0,0),
                    'mass':tempm,
                    'vel':tempvel,
                    'acc':vector(0,0,0),
                    'num':index
                    })

def random_vect(dx, dy, dz):
    return vector(uniform(-dx/2, dx/2),uniform(-dy/2,dy/2),uniform(-dz/2,dz/2))
                
