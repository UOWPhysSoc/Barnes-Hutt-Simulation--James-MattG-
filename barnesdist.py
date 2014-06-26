'''
Distribution function module for Barnes-Hutt n-body simulation developed by Matt Griffiths and James Archer.
Example distribution written by Matt Griffiths, list idea concieved by James Archer.
Special thanks to Matt Sanderson for ideas regarding distribution implementation.

Avaliable for use under a GPL v3 licence.
'''

#Import dependent libraries
from random import *
from visual import *

##~~~~~~~~~~~~~~~!!! EXAMPLE DISTRIBUTION !!!~~~~~~~~~~~~~~~  :

def ring(index,posd,veld,centralmass):
#Ring type distribution around a massive central body

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


##~~~~~~~~~~~~~~~!!! ADD USER DISTRIBUTION FUNCTIONS BELOW THIS POINT !!!~~~~~~~~~~~~~~~      
