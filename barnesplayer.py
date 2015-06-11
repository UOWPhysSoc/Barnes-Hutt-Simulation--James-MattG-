'''
Player for the barnes-Hutt N-body simulation created by Matt Griffiths and James Archer.
Player Written by Matt Griffiths.

REQUIRES VPYTHON TO RUN

Avaliable for use under a GPL v3 licence.
'''

#Import dependent libraries
import pickle


class player():
#Player Class containing unpacker and ply function

    
    def __init__(self,filename):
    #Unpacks data from file
        self.rate = int(input('Playback rate: '))
        self.index = 1
        self.scene = display(width = 500, height = 500)
        self.trail = True
        while True:
            try:
                self.file = open(filename + str(self.index) + '.barnes','rb')
                print("Opened file " + filename + str(self.index))
                self.index += 1
            except:
                print('Ended trying to open file ' + str(self.index))
                break
            #Open file, set up data structures for incoming data
            
            self.steps = []
            self.particles = []

            #Unpack data into pre-existing data structures
            self.steps = pickle.load(self.file)
            self.file.close()

        #print('Number of steps is ' + str(len(self.steps)))

        #Create visual representations
            for i in self.steps[0]:
                self.particles.append(sphere(pos = (i[0],i[1],i[2]),radius = 0.1*pow(i[3],0.33)))#
                if self.trail:
                    self.particles[-1].trail = curve()
            if self.index == 1:
                self.scene.autoscale = True
            else:
                #self.scene.autoscale = False
                pass
            self.play()
        
    def play(self):
    #Play function

        #Set iteration pos to zero
        i = 0
        #print('f called')
        #Loop through steps
        while i < len(self.steps):

            #set refresh rate
            rate(self.rate)
            #Move spheres to relavent posiions
            for j in range(0,len(self.particles)):
                self.particles[j].pos = (self.steps[i][j][0],self.steps[i][j][1],self.steps[i][j][2])
                if self.trail:
                    self.particles[j].trail.append(pos = self.particles[j].pos)

            #Step player
            i += 1

            #Handle looping
            #if i >= len(self.steps):
            #    i = 0
        for i in self.particles:
            i.visible = False
            del i


if __name__ == '__main__':
    from visual import *
#If this is executed as standalone give input options
    while True:
        try:
            ifn = input('Input file name: ')
            break
        except:
            pass
    p = player(ifn)
    print('fin')
