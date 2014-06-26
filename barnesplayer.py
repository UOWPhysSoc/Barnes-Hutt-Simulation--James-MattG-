'''
Player for the barnes-Hutt N-body simulation created by Matt Griffiths and James Archer.
Player Written by Matt Griffiths.

REQUIRES VPYTHON TO RUN

Avaliable for use under a GPL v3 licence.
'''

#Import dependent libraries
from visual import *
import pickle


class player():
#Player Class containing unpacker and ply function

    
    def __init__(self,filename):
    #Unpacks data from file

        #Open file, set up data structures for incoming data
        self.file = open(filename+'.barnes','rb')
        self.steps = []
        self.scene = display(width = 1920, height = 1080)
        self.particles = []

        #Unpack data into pre-existing data structures
        while True:
            try:
                for i in pickle.load(self.file):
                    self.steps.append(i)
            except:
                break

        #Create visual representations
        for i in self.steps[0]:
            self.particles.append(sphere(pos = (i[0],i[1],i[2]),radius = math.log(i[3]+1)))
        self.scene.autoscale = False
        
    def play(self,rte):
    #Play function

        #Set iteration pos to zero
        i = 0

        #Loop through steps
        while i <= len(self.steps):

            #set refresh rate
            rate(60)

            #Move spheres to relavent posiions
            for j in range(0,len(self.particles)):
                self.particles[j].pos = (self.steps[i][j][0],self.steps[i][j][1],self.steps[i][j][2])

            #Step player
            i = i + rte

            #Handle looping
            if i >= len(self.steps):
                i = 0


if __name__ == '__main__':
#If this is executed as standalone give input options
    ifn = input('Input file name: ')
    p = player(ifn)
    pbr = int(input('Playback rate: '))
    p.play(pbr)
    print('fin')
