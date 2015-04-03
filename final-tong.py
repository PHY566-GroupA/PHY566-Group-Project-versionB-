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
from scipy import optimize
import Image
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
    xn=np.zeros(n_steps)
    xn2=np.zeros(n_steps)
    for i in range (0,n_walks):
        for j in range (1,n_steps):
            c=random()
            if 0.0 <= c <= 0.25:   #+x direction
                x[i,j]=x[i,j-1]+1
                y[i,j]=y[i,j-1]
            elif 0.25 < c <=0.5:   #-x direction
                x[i,j]=x[i,j-1]-1
                y[i,j]=y[i,j-1]
            elif 0.5 < c <= 0.75:  #+y direction
                y[i,j]=y[i,j-1]+1
                x[i,j]=x[i,j-1]
            else:                  #-y direction
                y[i,j]=y[i,j-1]-1
                x[i,j]=x[i,j-1]
            r[j]=r[j]+np.sqrt(x[i,j]**2+y[i,j]**2)
            r2[j]=r2[j]+x[i,j]**2+y[i,j]**2
            xn[j]=xn[j]+x[i,j]
            xn2[j]=xn2[j]+x[i,j]**2
    # normalize <xn> and <xn^2>
    r=r/float(n_walks)
    r2=r2/float(n_walks)
    xn=xn/float(n_walks)
    xn2=xn2/float(n_walks)
    return xn,xn2,r,r2
    

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
    

def choice4(nx,ny,origin):
    #same difinition as choice5, but the choice of the gas states which its neighbour have an empty states, return the coordinate
    c=0
    while True:
        x=randrange(0,nx)
        y=randrange(0,ny)
        if origin[x,y] != 0 : 
            if x < nx-1:
                if origin[x+1,y]==0:
                    c=1
            if x >0:
                if origin[x-1,y]==0:
                    c=1
            if y< ny-1:
                if origin[x,y+1]==0:
                    c=1
            if y>0:
                if origin[x,y-1]==0:
                    c=1
            if c==1:
                c=0
                break
    return x,y

def choice5(nx,ny,origin):
    #randomly choice the empty states which its neighbour have an gas states, return their coordinate
    #nx:dimension of x 
    #ny:dimension of y
    #origin: the matrix of all gas and empty states(-1 stands for gas A, 0 stands for empty, 1 stands for gas B)    
    c=0              # the flag used to check if its neighbour have gas states
    while True:
        x=randrange(0,nx)
        y=randrange(0,ny)         # random choose the x and y coordinates
        if origin[x,y] == 0 :     # choose the empty states first 
            if x < nx-1:          # for those not +x boundary states, if their +x direction have an gas stats, put c to 1
                if origin[x+1,y]!=0:
                    c=1
            if x >0:
                if origin[x-1,y]!=0:
                    c=1
            if y< ny-1:
                if origin[x,y+1]!=0:
                    c=1
            if y>0:
                if origin[x,y-1]!=0:
                    c=1
            if c==1:               #after check all directions, if c is equal to 1, then change c to 0 and break, return the x and y coordinates
                c=0
                break
    return x,y
    
def move2(nx,ny,i,j,origin):
    #corresponding to the move of choice 5 ,(the move of empty states.)
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
    
def solution(nx,ny,niter,origin_old,method):
    if method==1:
        #random choose gas, then move it 
        for i in range (0,niter):
            x,y = choice(nx,ny,origin_old)
            origin_new = move(nx,ny,x,y,origin_old)
            origin_old = np.copy(origin_new)
    if method==2:
        #random choose gas whose neighbor have empty states, then move it
        for i in range (0,niter):
            x,y = choice4(nx,ny,origin_old)
            origin_new = move2(nx,ny,x,y,origin_old)
            origin_old = np.copy(origin_new)
    if method==3:
        #random choose empty whose neighbor have gas, then move it 
        for i in range (0,niter):
            x,y = choice5(nx,ny,origin_old)
            origin_new = move2(nx,ny,x,y,origin_old)
            origin_old = np.copy(origin_new)
    return origin_new
    

def density(nx,ny,origin):
    # return the density of one step, density difines as 
    resultA=np.zeros(nx)
    resultB=np.zeros(nx)
    for i in range(0,nx):
        for j in range(0,ny):
            if origin[i,j]==1:
                resultA[i]=resultA[i]+1
            if origin[i,j]==-1:
                resultB[i]=resultB[i]+1
    resultA=resultA/float(nx*ny/3)
    resultB=resultB/float(nx*ny/3)
    return resultA,resultB
            
def n_density(nx,ny,niter,ntime):
    # average density after niter times, 
    #niter: number of trials
    #ntime: iteration number of mixing 
    resultA=np.zeros(nx)
    resultB=np.zeros(nx)
    for step in range(0,niter):
        print step
        ini=initial(nx,ny)
        origin=solution(nx,ny,ntime,ini,3)
        for i in range(0,nx):
            for j in range(0,ny):
                if origin[i,j]==1:
                    resultA[i]=resultA[i]+1
                if origin[i,j]==-1:
                    resultB[i]=resultB[i]+1
    resultA=resultA/float(nx*ny*niter/3)
    resultB=resultB/float(nx*ny*niter/3)
    return resultA,resultB            

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

#Problem 3 part a and part b
#origin=initial(60,40)
#xla=np.linspace(1,60,60)
#v_new=solution(60,40,5000000,origin,3)
#nx,ny=density(60,40,v_new)
#v_new=np.transpose(v_new)
#matshow(v_new)
#plt.savefig('M15-6.pdf')
#plt.clf()
#plt.plot(xla,nx,'r',label="$n(A)$")
#plt.plot(xla,ny,'b',label="$n(B)$")
#plt.legend(loc="best",fontsize=12)
#plt.xlabel("$x\ grid$",fontsize=16)
#plt.ylabel("$Probability$",fontsize=16)
#plt.savefig('D15-6.pdf')


#v_old=initial(150,100)
#xla=np.linspace(1,150,150)
#for i in range(0,3):
#    print i
#    v_new=solution(600,400,100000,v_old,3)
#    v_old=np.copy(v_new)
#    nx,ny=density(600,400,v_new)
#    v_new=np.transpose(v_new)
#    matshow(v_new)
#    name1="M%i.pdf" %i
#    name2="D%i.pdf" %i
#    plt.savefig(name1)
#    plt.clf()
#    plt.plot(xla,nx,'r',label="$n(A)$")
#    plt.plot(xla,ny,'b',label="$n(B)$")
#    plt.legend(loc="best",fontsize=12)
#    plt.xlabel("$x\ grid$",fontsize=16)
#    plt.ylabel("$Probability$",fontsize=16)
#    plt.savefig(name2)
    


#Problem3 part C
#xla=np.linspace(1,60,60)
#nA,nB=n_density(60,40,100,5000000)
#nA,nB=n_density(60,40,100,100000)
#plt.plot(xla,nA,'r',label="$n(A)$")
#plt.plot(xla,nB,'b',label="$n(B)$")
#plt.legend(loc="best",fontsize=12)
#plt.xlabel('$x grid$',fontsize=16)
#plt.ylabel('$Probability$',fontsize=16)
#plt.savefig('P3-3-v4.pdf')

# Problem 1.
#xn,xn2,r,r2=random_walk(10000,100)
#xla=np.linspace(1,100,100)

#def fit1(x,a,b):
#    return a*x+b
#guess=np.array([1.0,0.0])
#a,b=optimize.curve_fit(fit1,xla,r2,guess)
#print a
#yla=a[0]*xla+a[1]
    
#plt.clf()
#plt.plot(xla,xn,'r',label="$<x_n>$")
#plt.plot(xla,xn2,'b',label="$<(x_n)^2>$")
#plt.ylim([-5,60])
#plt.xlim([1,100])
#plt.legend(loc="best",fontsize=12)
#plt.xlabel('$n$',fontsize=16)
#plt.ylabel('$Arbs.$',fontsize=16)
#plt.savefig('P1-1.pdf')


#plt.clf()
#plt.plot(xla,r2,'r',label="$<r^2>\ from \ calculated$")
#plt.plot(xla,yla,'b',label="$fit \ curve$")
#plt.legend(loc="best",fontsize=12)
#toWrite= "y = %f*x - %f" % (a[0],-a[1])
#plt.text(5,60,toWrite)
#plt.xlabel('$Times (n)$', fontsize=16)
#plt.ylabel('$<r^2>$',fontsize=16)
#plt.savefig('P1-2.pdf')