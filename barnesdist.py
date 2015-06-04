'''
Distribution function module for Barnes-Hutt n-body simulation developed by Matt Griffiths and James Archer.
Example distribution written by Matt Griffiths, list idea concieved by James Archer.
Special thanks to Matt Sanderson for ideas regarding distribution implementation.

Avaliable for use under a GPL v3 licence.
'''

#Import dependent libraries
from random import *
#from visual import *
from math import *

class distributions():

    def __init__(self, dist_name, G):
        self.dist_name = dist_name
        self.part = []
        self.n = 0
        self.index = 0
        self.G = G

    def call(self):
        for i in self.dist_name:
            try:
                getattr(self, i)()
            except:
                pass
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
                'num':self.index
                })
            self.index += 1


    def ring_old(index,posd,veld,centralmass):
#Ring type distribution around a massive central body
        # NOT APPROPRIATED FOR NEW DISTRIBUTION SYSTEM

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

    def kepler(self):
        n_new = int(input('Number of bodies: '))
        self.n += n_new
        cent_mass = float(input('Central body mass: '))
        other_mass = float(input('Other masses: '))
        mean_r = float(input('Mean radius: '))
        self.part.append({
                'pos-1':vector(0,0,0),
                'pos':vector(0,0,0),
                'mass':cent_mass,
                'vel':vector(0,0,0),
                'acc':vector(0,0,0),
                'num':self.index
                })
        self.index += 1
        for i in range(0,n_new - 1):
            r = vector(1,0,0) * expovariate(1./mean_r)
            r = rotate(r, uniform(0, 2*pi), vector(0,0,1))
            self.part.append({
                'pos-1':r,
                'pos':r,
                'mass':other_mass,
                'vel':cross(r/mag(r),vector(0,0,1))*pow(self.G*(cent_mass + n_new*other_mass*(1-exp(-mag(r)/mean_r)))/mag(r),0.5),
                'acc':vector(0,0,0),
                'num':self.index
                })
            self.index += 1

    def two_body(self):
        self.n += 2
        mass1 = float(input('First body mass: '))
        mass2 = float(input('Second body mass: '))
        r = vector(1,0,0)*float(input('Separation distance: '))
        mu = mass1 * mass2 /(mass1 + mass2)
        self.part.append({
            'pos-1':vector(0,0,0),
            'pos':vector(0,0,0),
            'mass':mass1,
            'vel':sqrt(mass2**2/(mag(r)*(mass1 + mass2))) * vector(0,1,0),
            'acc':vector(0,0,0),
            'num':self.index
            })
        self.index += 1
        self.part.append({
            'pos-1':r,
            'pos':r,
            'mass':mass2,
            'vel':sqrt(mass1**2/(mag(r)*(mass1 + mass2))) * vector(0,-1,0),
            'acc':vector(0,0,0),
            'num':self.index
            })
        self.index += 1
        

        

def random_vect(dx, dy, dz):
    return vector(uniform(-dx/2, dx/2),uniform(-dy/2,dy/2),uniform(-dz/2,dz/2))
                


#james rules 
