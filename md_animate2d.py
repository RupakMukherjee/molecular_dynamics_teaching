#!/usr/bin/ python

import numpy as np
import pylab as plt
import random
import math
import matplotlib.animation as animation

#========= Configuration ===========
show_anim = True
interval = 0.1#in seconds
datadt = 10
DIR ="data"
Lx = 10.0
Ly = 10.0

tmax = 100.0
dt   = 0.010
Nt   = round(tmax/dt)


data_num = np.arange(start=0, stop=Nt, step=datadt, dtype=int)

if (show_anim == True):
    def animate(i):
        file=DIR+'/data%d'%data_num[i]+'.txt'
        datax1,datav1 = np.loadtxt(file, unpack=True)

        ax1.cla()
        img1 = ax1.scatter(datax1,datav1,s=1,marker='o',color='b',alpha=1.0)
        ax1.set_title('TimeSteps = %d'%i+'\n Phase Space')
        ax1.set_xlabel("$x$")
        ax1.set_ylabel("$y$")
        ax1.set_xlim([-Lx, Lx])
        ax1.set_ylim([-Ly, Ly])



if (show_anim == True):
    fig,ax1 = plt.subplots(1,1,figsize=(6, 6))
    ani = animation.FuncAnimation(fig,animate,frames=len(data_num),interval=interval*1e+3,blit=False)
    plt.show()
