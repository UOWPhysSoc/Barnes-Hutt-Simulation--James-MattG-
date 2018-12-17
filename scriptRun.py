# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 13:51:45 2018

@author: jia335
"""

import Barnes_Hutt_nbody_Simulation as bh
import sys
import time
import pickle

if __name__ == '__main__':
    
    script = sys.argv[1]
    
    with open(script, 'rb') as f:
        args = pickle.load(f)

    b = bh.BarnesHut(*args)
    
    t_start = time.time()
    while True:
        if b.quit == True:
            break
        b.step()
    t_final = time.time()
    t_total = t_final - t_start
    if t_total < 60:
        print(f"Time taken was {round(t_total, 3)} seconds")
    else:
        print(f"Time taken was {round(int(t_total/60), 3)}:{round(int(t_total%60), 3)} minutes")