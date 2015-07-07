from math import *
from random import gauss, uniform
import time

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
    points = [(0.1,0.1)]
    while len(points) < n:
        x = gauss_2d(points[-1], sigma)
        a = P(x[0], x[1], a, b)/P(points[-1][0], points[-1][1], a, b)
        if x[0] > 0:
            if a >= 1:
                points.append(x)
                
            elif uniform(0, 1) < a:
                points.append(x)
                
    del points[0]
    return points

t = time.time()    
metpoints = metropolisHastings(1, 1, (7, 2), 100)
t = time.time() - t

