# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 15:01:49 2018

@author: jia335
"""
import numpy as np
import bpy
from mathutils import Vector
import pickle

if __name__ == "__main__":
    
    scene = bpy.context.scene

    base_star = bpy.data.objects["Star_Template"]

    #file = r'C:\Users\jia335\Dropbox\PhD\Blender renders\FOD_simulation\output_test_photon.txt'
    filename = r'C:\Users\jia335\projects\Barnes-Hutt-Simulation--James-MattG-\untitled'
    
    index = 1
    frame = 1
    particles = []
    
    while True:
        try:
            file = open(filename + str(index) + '.barnes','rb')
            print("Opened file " + filename + str(index))
            index += 1
        except:
            print('Ended trying to open file ' + str(index))
            break
        #Open file, set up data structures for incoming data
        
        steps = []

        #Unpack data into pre-existing data structures
        steps = pickle.load(file)
        file.close()
        
        if particles == []:
            
            for i in steps[0]:
                new_star = base_star.copy()
                new_star.data = base_star.data.copy()
                new_star.scale = Vector([1,1,1]) * i[3] * 0.01
                bpy.context.scene.objects.link(new_star)
                particles.append(new_star)
                
        for i in steps:
            
            for j, part in enumerate(particles):
                part.location = Vector([i[j][0], i[j][1], i[j][2]])
                part.keyframe_insert(data_path="location")
                
            frame += 1
            scene.frame_set(frame)