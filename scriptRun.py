# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 13:51:45 2018

@author: jia335
"""

import Barnes_Hutt_nbody_Simulation as bh
import sys
import time
import pickle
import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = 'Run the Barnes Hutt sim as a script.')
    parser.add_argument('Config', metavar='f', type=str,
                    help='The config file to load.')
    parser.add_argument('--filesize', type=int, help = 'Int for the size of files (x2 mb)')
    args = parser.parse_args()

    with open(args.Config, 'rb') as f:
        b_args = pickle.load(f)

    if args.filesize:
        b = bh.BarnesHut(*b_args, fileScale=args.filesize)
    else:
        b = bh.BarnesHut(*b_args)
    
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