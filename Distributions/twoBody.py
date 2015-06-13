from .vector import *

class twoBody:

    def __init__(self):

        self.name = 'Two Body'
        self.parameters = [
            {'pName':'Mass 1', 'pType':'numeric', 'default':1, 'tooltip':None},
            {'pName':'Mass 2', 'pType':'numeric', 'default':1, 'tooltip':None},
            {'pName':'Separation', 'pType':'numeric', 'default':1, 'tooltip':'Initial distance between the masses'},
            {'pName':'First mass position', 'pType':'vector','default':vector(0,0,0), 'tooltip':'Initial position of the first mass'},
            {'pName':'Net velocity','pType':'vector','default':vector(0,0,0),'tooltip':'Initial net velocity of group.\nOnly important for relative velocity\nbetween different distributions as\nthe total momentum is set to zero.'},
            {'pName':'Axis','pType':'vector','default':vector(0,0,1),'tooltip':'Axis about which the\ndistribution is symmetric.'}]

    def run(self, list_of_stuff, dist, G):

        mass1 = float(list_of_stuff[0])
        mass2 = float(list_of_stuff[1])
        r = float(list_of_stuff[2])
        r1 = strToVector(list_of_stuff[3])
        v0 = strToVector(list_of_stuff[4])
        R = norm(strToVector(list_of_stuff[5]))
        Rp = perp(R)

        dist.n += 2

        mu = mass1 * mass2 /(mass1 + mass2)
        dist.part.append({
            'pos-1':r1,
            'pos':r1,
            'mass':mass1,
            'vel':sqrt(G*mass2**2/(r*(mass1 + mass2))) * cross(Rp,R) + v0,
            'acc':vector(0,0,0),
            'num':dist.index
            })
        dist.index += 1
        dist.part.append({
            'pos-1':Rp*r + r1,
            'pos':Rp*r+r1,
            'mass':mass2,
            'vel':sqrt(G*mass1**2/(r*(mass1 + mass2))) * cross(R,Rp) + v0,
            'acc':vector(0,0,0),
            'num':dist.index
            })
        dist.index += 1

        
