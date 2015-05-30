'''
N-body simulation using a Barnes-Hutt algorithm approximation reducing the complexity from O(n^2) to O(n log n).
Written in collaboration by James Archer and Matt Griffiths.

Note: This sim normalizes to an arbitrary set of values.

REQUIRES VPYTHON TO WORK

Avaliable for use under a GPL v3 licence.
'''

#Dependant library imports
from visual import *
from barnesdist import *
import barnesplayer
import pickle
import time


class BarnesHut():
#Barnes Hutt Class containing all sim information and algorithms
    
    def __init__(self,dist,dt,timelim,filename):
    #Initialization function handling distribution and simulation settings
        
        #Sim settings
        self.bodies = []
        self.dist = dist
        self.bodies = self.dist.call()
        self.n = self.dist.n
        self.timelim = timelim
        self.dt = dt
        self.filename = filename
        self.outputsize = (10.0/72.5)*1E5/(self.n)
        self.file_no = 1
        
        #Constants and global values
        self.time = 0
        self.P = vector(0,0,0)
        self.M = 1
        self.COM = vector(0,0,0)
        self.G = 1
        self.epsilon = 0.1
        self.theta = 0.25
        self.quit = False
        
        #Data Structures prior to initial data generation
        self.outputbus = []
        self.t = None       #Tree will be calculated later
        
        #Initial data generation
        #self.gen()
        self.verletfirst()
        self.detrange()    
        self.t = self.tree(10+self.R,self.bodies)

    def gen(self):
        pass
    #Generation function using the external distributions

        #Determine the initial net momentum, total mass and centre of mass
##        for i in self.bodies:
##            self.P += i['mass']*i['vel']
##            self.M += i['mass']
##            self.COM = (self.COM*self.M + i['mass']*i['pos-1'])/(self.M + i['mass'])
##
##        #Normalize velocity using the net momentum and total mass so that there is no net movement and centre sim at the COM
##        for i in self.bodies:
##            i['vel'] -= self.P/self.M
##            i['pos-1'] -= self.COM

    def verletfirst(self):
    #The zeroth step for Verlet numerical integration
        
        for i in self.bodies:   
            #Calculate a temprary force vector for each body
            self.tempforce = vector(0,0,0)
            for j in self.bodies:
                if i != j and i['pos-1'] != j['pos-1']:
                    self.tempforce += (((self.G*i['mass']*j['mass'])/abs(i['pos-1']-j['pos-1'])**2)*(j['pos-1']-i['pos-1']))

            #Apply appropriate acceleration to each body
            i['acc'] = self.tempforce/i['mass']

            #Calculate the n+1 position using the zeroth step Verlet method
            i['pos'] = i['pos-1'] + i['vel']*self.dt + 0.5*i['acc']*self.dt**2
                    
    def verlet(self,body):
    #Standard Verlet method for numercal integration
        
        self.verlettemp = 2*body['pos'] - body['pos-1'] + body['acc']*self.dt**2
        body['pos-1'] = body['pos']
        body['pos'] = self.verlettemp

    def getacc(self,body,node):
    #Determine the acceleration of a body using the Barnes-Hutt recursive method applied to a custom tree data structure
        
        #Temporary vector to be returned
        ret = vector(0,0,0)
        
        #If node is empty, add nothing to temp vector
        if node.total == 0:
            pass

        #If node contains only one 'non-self' body, determine force
        elif node.total == 1:
            if body['num'] == node.data[0]['num']:
                pass
            else:
                ret += self.force(node.data[0]['pos'],body['pos'],node.data[0]['mass'])

        #If node contains multiple bodies, use Barnes-Hutt method
        elif node.total >= 2:
            if abs(node.xr[1]-node.xr[0])/abs(body['pos']-node.com) < self.theta:
                ret += self.force(node.com,body['pos'],node.mass)
            else:
                for i in node.subnodes:
                    ret += self.getacc(body,i)
        #Return net acceleration
        return ret
                
    def force(self,posn,posi,mass):
    #Use standard universal gravitation to determine force
        
        #posn is the position of the particle in the node , posi is the position of the particle for which the force is being calc upon
        return ((self.G*mass)/(abs(posn-posi)+self.epsilon)**2)*((posn - posi)/abs(posn - posi))

    def detrange(self):
    #Determine the radius of the simulation as to dynamically shift simulation boundaries
        
        self.R = 0
        for i in self.bodies:
            if mag(i['pos']) >= self.R:
                self.R = mag(i['pos'])
            
    def tree(self,simrange,lis):
    #construct tree over sim range and add all bodies to tree
        
        self.root = node(-simrange,simrange,-simrange,simrange,-simrange,simrange)
        for i in lis:
            self.root.add(i)

    def write(self,ty = 'norm'):
    #Write data to pickled file, for later use

        #create clean temp step bus
        stepbus = []
        #print(self.bodies)
        #Write cartesian coords and mass to step bus 
        for i in self.bodies:
            stepbus.append([float(i['pos-1'].x),float(i['pos-1'].y),float(i['pos-1'].z),float(i['mass'])*self.M])
        
        #Write step bus to output bus
        self.outputbus.append(list(stepbus))

        #If sim finishes or output bus reaches et size, write bus to file and clear bus
        if len(self.outputbus) == self.outputsize or ty == 'fin':
            self.file = open(self.filename + str(self.file_no) + '.barnes','wb')
            pickle.dump(self.outputbus,self.file)
            #print(self.outputbus)
            self.outputbus = []
            self.file.close()
            self.file_no += 1

    def step(self):
    #Step function to handle all function calling each step


        #Check sim length
        if self.time > self.timelim:
            self.write('fin')
            self.quit = True

        else:
            self.write()
            
        #Determine sim range and dynamically construct tree
        self.detrange()
        self.t = self.tree(10+self.R,self.bodies)

        #Determine accelerations
        for i in self.bodies:
            i['acc'] = self.getacc(i,self.root)

        #Run Verlet integration
        for i in self.bodies:
            self.verlet(i)

        #Print progress percentage
        if round((self.time/self.timelim)*100,5) %1 == 0 and (self.time/self.timelim)*100<=100:
            print(str(round((self.time/self.timelim)*100,2))+'% done')

        #Iterate timing
        self.time += self.dt

        
class node():
#custom node type data structure
    
    def __init__(self,xs,xe,ys,ye,zs,ze,assignment = 0):
    #Initialize a node
        
        self.data = []
        self.subnodes = []
        self.total = 0
        self.mass = 0
        self.com = vector(0,0,0)
        self.xr = (xs,xe)
        self.yr = (ys,ye)
        self.zr = (zs,ze)
        self.assignment = assignment

    def add(self,body):
    #Defining the addition of an object to the node
        
        self.data.append(body)
        self.total += 1
        self.mass += body['mass']
        self.com = (self.com*self.mass + body['pos']*body['mass'])/(self.mass+body['mass'])
        self.check()

    def check(self):
    #Check that a node is only containing a single object and ensuring that subnodes are assigned if multiple bodies are added

        #If there is only one body do nothing
        if self.total == 1:
            pass

        #If there are two bodies, create sub octants and distribute bodies
        elif self.total == 2 and len(self.subnodes) == 0:
            self.octantgen()
            self.sort(self.data[0])
            self.sort(self.data[1])
            self.data = []

        #If there are three bodies, distribute body to pre-existing subnodes
        elif self.total >=3:
            self.sort(self.data[0])
            self.data = []
            
    def sort(self,particle):
    #Sort body into apropriate subnode
        
            for j in self.subnodes:
                if particle['pos'].x >= j.xr[0] and particle['pos'].x < j.xr[1]:
                    if particle['pos'].y >= j.yr[0] and particle['pos'].y < j.yr[1]:
                        if particle['pos'].z >= j.zr[0] and particle['pos'].z < j.zr[1]:
                            j.add(particle)
                            break

    def octantgen(self):
    #Create sub octants based of dimensions of previous parent octant
        
            self.subnodes.append(node(self.xr[0],(self.xr[1]+self.xr[0])/2,
                                      self.yr[0],(self.yr[1]+self.yr[0])/2,
                                      self.zr[0],(self.zr[1]+self.zr[0])/2,
                                 1))
                                 
            self.subnodes.append(node((self.xr[1]+self.xr[0])/2,self.xr[1],
                                      self.yr[0],(self.yr[1]+self.yr[0])/2,
                                      self.zr[0],(self.zr[1]+self.zr[0])/2,
                                 2))
                                 
            self.subnodes.append(node(self.xr[0],(self.xr[1]+self.xr[0])/2,
                                      (self.yr[1]+self.yr[0])/2,self.yr[1],
                                      self.zr[0],(self.zr[1]+self.zr[0])/2,
                                 3))
                                 
            self.subnodes.append(node((self.xr[1]+self.xr[0])/2,self.xr[1],
                                      (self.yr[1]+self.yr[0])/2,self.yr[1],
                                      self.zr[0],(self.zr[1]+self.zr[0])/2,
                                 4))

            self.subnodes.append(node(self.xr[0],(self.xr[1]+self.xr[0])/2,
                                      self.yr[0],(self.yr[1]+self.yr[0])/2,
                                      (self.zr[1]+self.zr[0])/2,self.zr[1],
                                 5))
                                 
            self.subnodes.append(node((self.xr[1]+self.xr[0])/2,self.xr[1],
                                      self.yr[0],(self.yr[1]+self.yr[0])/2,
                                      (self.zr[1]+self.zr[0])/2,self.zr[1],
                                 6))
                                 
            self.subnodes.append(node(self.xr[0],(self.xr[1]+self.xr[0])/2,
                                      (self.yr[1]+self.yr[0])/2,self.yr[1],
                                      (self.zr[1]+self.zr[0])/2,self.zr[1],
                                 7))
                                 
            self.subnodes.append(node((self.xr[1]+self.xr[0])/2,self.xr[1],
                                      (self.yr[1]+self.yr[0])/2,self.yr[1],
                                      (self.zr[1]+self.zr[0])/2,self.zr[1],
                                8))

        
if __name__ == '__main__':

    #Inputs
    ofn = str(input('Output file name: '))
    dti = float(input('dt value: '))
    sml = float(input('Sim length: '))

    print('Expected sim length is ' + str(sml/dti))

    dist_name = str(input('Distribution to use: '))
    dist_name = dist_name.split(',')
    dist = distributions(dist_name)

    #Define Sim and run
    b = BarnesHut(dist,dti,sml,ofn)
    #print(b.n)
    while True:
        if b.quit == True:
            break
        b.step()

    #Play sim
    plyr = barnesplayer.player(ofn)
 #   pbr = int(input('Playback rate: '))
    plyr.play()
