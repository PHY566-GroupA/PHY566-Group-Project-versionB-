# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 20:20:39 2015

@author: tong
@group member: Yingmei, Ankur, Aritro
"""
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from optparse import OptionParser
from random import randrange
#from random import random
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
    

def initial(nx,ny):
    #initial position of the two gas, -1 stands for gas A, 1 stands for gas B, and 0 stands for empty
    result=np.zeros((nx,ny))
    for i in range(0,nx/3):
        for j in range(0,ny):
            result[i,j]=-1
    for i in range(2*nx/3,nx):
        for j in range(0,ny):
            result[i,j]=1
    return result     

def choice(nx,ny,origin):
    # origin, stands the origin density of two gas
    # return the random choosed positon of  two kinds gas
    indexx=np.zeros(ny*ny)
    indexy=np.zeros(ny*ny)
    a=0
    for i in range(0,nx):
        for j in range(0,ny):
            if origin[i,j]!=0:
                indexx[a]=i
                indexy[a]=j
                a+=1
    random_index=randrange(0,ny*ny)
    resultx=indexx[random_index]
    resulty=indexy[random_index]
    return resultx,resulty

def move(nx,ny,i,j,origin):
    # move this gas according to the description of problem, 
    # then return the changed density matrix
    c=random()
    if 0.0  <= c <= 0.25:
        if i<nx-1:
            if origin[i+1,j] == 0:
                origin[i+1,j] = origin[i,j]
                origin[i,j]= 0 
    elif 0.25 < c <= 0.5:
        if i>0:
            if origin[i-1,j] == 0:
                origin[i-1,j]=origin[i,j]
                origin[i,j] = 0 
    elif 0.5 < c <= 0.75:
        if j<ny-1:
            if origin[i,j+1]== 0:
                origin[i,j+1] = origin[i,j]
                origin[i,j] = 0
    else: 
        if j>0:
            if origin[i,j-1] == 0:
                origin[i,j-1] = origin[i,j]
                origin[i,j] = 0 
    return origin
    
def choice2(nx,ny,origin):
    # in order to accerlerate the random case, we choose the empty states to move,
    # firstly choosed the position of any empty states. 
    indexx=np.zeros(nx*ny/3)
    indexy=np.zeros(nx*ny/3)
    a=0
    for i in range(0,nx):
        for j in range(0,ny):
            if origin[i,j]==0:
                indexx[a]=i
                indexy[a]=j
                a+=1
    random_index=randrange(0,nx*ny/3)
    resultx=indexx[random_index]
    resulty=indexy[random_index]
    return resultx,resulty


def choice3(nx,ny,origin):
    # choosing the empty states is still slow, in order to accerlerate the approch,
    # random choose the position which its neighbor has gas. 
   a=0 
   c=0
   x=np.zeros(nx*ny/3)
   y=np.zeros(nx*ny/3)
   for i in range(0,nx):
       for j in range(0,ny):
           if origin[i,j]==0:
               if i < nx-1:
                   if origin[i+1,j]!=0:
                       c=1
               if i >0:
                   if origin[i-1,j]!=0:
                       c=1
               if j< ny-1:
                   if origin[i,j+1]!=0:
                       c=1
               if j>0:
                   if origin[i,j-1]!=0:
                       c=1
               if c==1:
                   x[a]=i
                   y[a]=j
                   a+=1
                   c=0
   indexx=np.zeros(a)
   indexy=np.zeros(a)   
   for i in range (0,a):
       indexx[i]=x[i]
       indexy[i]=y[i]
   random_index=randrange(0,a)
   resultx=indexx[random_index]
   resulty=indexy[random_index]
   return resultx,resulty


    
def move2(nx,ny,i,j,origin):
    #corresponding to the move of choice 2 and choice 3,(the move of empty states.)
    #after that,return the charge density
    c=random()
    if 0.0  <= c <= 0.25:
        if i<nx-1:
            if origin[i+1,j]!= 0:
                origin[i,j]=origin[i+1,j]
                origin[i+1,j]= 0 
    elif 0.25 < c <= 0.5:
        if i>0:
            if origin[i-1,j] != 0:
                origin[i,j] = origin[i-1,j]
                origin[i-1,j] = 0 
    elif 0.5 < c <= 0.75:
        if j<ny-1:
            if origin[i,j+1]!= 0:
                origin[i,j]=origin[i,j+1]
                origin[i,j+1] = 0
    else: 
        if j>0:
            if origin[i,j-1] != 0:
                origin[i,j] = origin[i,j-1]
                origin[i,j-1] = 0 
    return origin
    
def solution(nx,ny,niter,method):
    origin_old=initial(nx,ny)
    if method==1:
        #random choose gas, then move it 
        for i in range (0,niter):
            x,y = choice(nx,ny,origin_old)
            origin_new = move(nx,ny,x,y,origin_old)
            origin_old = np.copy(origin_new)
    if method==2:
        #random choose empty, then move it
        for i in range (0,niter):
            x,y = choice2(nx,ny,origin_old)
            origin_new = move2(nx,ny,x,y,origin_old)
            origin_old = np.copy(origin_new)
    if method==3:
        #random choose empty whose neighbor have gas, then move it 
        for i in range (0,niter):
            x,y = choice3(nx,ny,origin_old)
            origin_new = move2(nx,ny,x,y,origin_old)
            origin_old = np.copy(origin_new)
    return origin_new
    


            
            

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

test=solution(60,40,10000,3)
test=np.transpose(test)
matshow(test)

#x,y,r,r2=random_walk(10000,100)
#xla=np.linspace(0,99,100)
#plt.plot(xla,r,'r')
#plt.plot(xla,r2,'b')
