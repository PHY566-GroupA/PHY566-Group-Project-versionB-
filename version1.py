# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 20:20:39 2015

@author: tong
@group member: Yingmei, Ankur, Aritro
"""
import random
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser


#functions 
def random_walk(n_walks,n_steps):
    #variable definition: x: x position, y: y position
    # r2: <xn^2>   r: <xn>
    # n_walks: number of walks 
    # n_steps: number of steps per walk
    x=np.zeros((n_walks,n_steps))
    y=np.zeros((n_walks,n_steps))
    r2=np.zeros(n_steps)
    r=np.zeros(n_steps)
    for i in range (0,n_walks):
        for j in range (1,n_steps):
            c=random.random()
            if 0.0 <= c <= 0.25:
                x[i,j]=x[i,j-1]+1
                y[i,j]=y[i,j-1]
            elif 0.25 < c <=0.5:
                x[i,j]=x[i,j-1]-1
                y[i,j]=y[i,j-1]
            elif 0.5 < c <= 0.75:
                y[i,j]=y[i,j-1]+1
                x[i,j]=x[i,j-1]
            else:
                y[i,j]=y[i,j-1]-1
                x[i,j]=x[i,j-1]
            r[j]=r[j]+np.sqrt(x[i,j]**2+y[i,j]**2)
            r2[j]=r2[j]+x[i,j]**2+y[i,j]**2
    # normalize <xn> and <xn^2>
    r=r/float(n_walks)
    r2=r2/float(n_walks)
    return x,y,r,r2
    
    


#main
parser = OptionParser()
parser.description = "This tool solute the Group project#1 (version B)  " + \
                       "in PHY566."
parser.add_option("--nwalks", dest="walk", type="int", 
        default=1000, 
        help="Number of sampling points")
parser.add_option("--nsteps", dest="step", type="int", 
        default=100, 
        help="Number of states to be plotted")
# Variables are acessible via options.<variable name>
(options, args) = parser.parse_args() 



x,y,r,r2=random_walk(10000,100)
xla=np.linspace(0,99,100)
plt.plot(xla,r,'r')
plt.plot(xla,r2,'b')
