from .vector import *
from random import gauss, uniform, choice
from math import *

class MN: 

    def __init__(self):

        self.name = 'Miyamoto Nagai'
        self.parameters = [
            {'pName':'Mass', 'pType':'numeric', 'default':1, 'tooltip':''},
            {'pName':'Number', 'pType':'int', 'default':10, 'tooltip':''},
            {'pName':'Radius', 'pType':'numeric', 'default':1, 'tooltip':''},
            {'pName':'Flatness', 'pType':'numeric', 'default':1, 'tooltip':'b/a, 0 is flat, larger is rounder.'},
            {'pName':'Centre', 'pType':'vector', 'default':vector(0,0,0), 'tooltip':'Initial position of the central mass'},
            {'pName':'Net velocity','pType':'vector','default':vector(0,0,0),'tooltip':'Initial net velocity of group.\nOnly important for relative velocity\nbetween different distributions as\nthe total momentum is set to zero.'},
            {'pName':'Axis','pType':'vector','default':vector(0,0,1),'tooltip':'Axis about which the\ndistribution is symmetric.'}]

    def run(self, imports, dist, G):

        m = float(imports[0])
        n = int(imports[1])
        R = float(imports[2])
        ratio = float(imports[3])
        a = R/ratio
        b = R
        r1 = strToVector(imports[4]) # centre
        V0 = strToVector(imports[5]) # net velocity
        Z0 = norm(strToVector(imports[6])) # z axis
        R0 = perp(Z0) # x axis
        Y0 = cross(Z0, R0)

        coords = metropolisHastings(a, b, 2*R, n)

        dist.n += n

        for i in coords:
            theta = i[2]
            Rcoord = R0*1
            Rcoord.rotate(theta, Z0)
            z = choice([-1,1]) * abs(i[1])
            F = vector(0,0,0)

            for j in coords:
                if i != j:
                    jcoord = R0*j[0]
                    jcoord.rotate(j[2],Z0)
                    F += m*m*G/mag2(Rcoord*i[0] + Z0*z + -1*jcoord + -1*Z0*j[1])*norm(Rcoord*i[0] + Z0*z + -1*jcoord + -1*Z0*j[1])

            #dR = phi(i[0], i[1], a, b, n*m, G)**3 *i[0]/(G**2 * (n*m)**2)
            #dz = G*n*m*(a + sqrt(i[1]**2 + b**2))*i[1]/(sqrt(i[0]**2 + (a + sqrt(i[1]**2 + b**2))**2)**3 * sqrt(i[1]**2 + b**2))
            #F = sqrt(dR**2 + dz**2)
            Fm = mag(F)
            v_mag = sqrt(Fm*sqrt(i[0]**2 + i[1]**2)/m)
            #F_vec = -1*R0*dR*cos(theta) + -1*Y0*dR*sin(theta) + -1*Z0*dz
            v_dir = cross(norm(Rcoord),Z0)
                          #norm(R0*i[0]*cos(theta) + Y0*i[0]*sin(theta) + Z0*i[1]))
            
            dist.part.append({
                'pos-1':r1 + Rcoord*i[0] + Z0*z,
                'pos':r1 + Rcoord*i[0] + Z0*z,
                'mass':m,
                'vel':V0 + v_dir*v_mag,
                'acc':vector(0,0,0),
                'num':dist.index
                })
            dist.index += 1

        
def P(R, z, a, b):
    numerator = R*(a*R**2 + (a + 3*sqrt(z**2 + b**2))*(a + sqrt(z**2 + b**2))**2) # R added
    denominator = (R**2 + (a + sqrt(z**2 + b**2))**2)**(5/2) * (z**2 + b**2)**(3/2)
    return numerator / denominator
    
def gauss_2d(coord, sigma):
    if isinstance(sigma, float) or isinstance(sigma, int):
        return gauss(coord[0], sigma), gauss(coord[1], sigma)
    if isinstance(sigma, tuple) or isinstance(sigma, list):
        return gauss(coord[0], sigma[0]), gauss(coord[1], sigma[1])
    else:
        raise TypeError("Must be number or tuple/list")

    
def metropolisHastings(a, b, sigma, n):
    points = [(0.1*a,0.1*b)]
    while len(points) < n+1:
        x = gauss_2d(points[-1], sigma)
        a = P(x[0], x[1], a, b)/P(points[-1][0], points[-1][1], a, b)
        if x[0] > 0:
            if a >= 1:
                points.append((x[0], x[1], uniform(0,2*pi)))
                
            elif uniform(0, 1) < a:
                points.append((x[0], x[1], uniform(0,2*pi)))
            else:
                points.append((points[-1][0], points[-1][1], uniform(0,2*pi)))
                
    del points[0]
    return points

def phi(R, z, a, b, M, G):
    return -G*M/sqrt(R**2 + (a + sqrt(z**2 + b**2))**2)
