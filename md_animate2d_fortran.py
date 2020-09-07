#!/usr/bin/ python

import numpy as np
import pylab as plt
import random
import math
import matplotlib.animation as animation
import os
#========= Configuration ===========
show_anim = True
interval = 0.1#in seconds
datadt = 10
DIR ="data"
Lx = 10.0
Ly = 10.0

tmax = 10.0
dt   = 0.010
Nt   = round(tmax/dt)

#========== Data Directory Setup =============
if os.path.exists("data_omp") and os.path.exists("data_omp/fort.101"):
    if os.path.exists("data_omp/fort.101"):
        print('Data exists')
    else:
        os.system('mv fort.* data_omp')
elif os.path.exists("data_omp") and os.path.exists("fort.101"):
    os.system('rm data_omp/fort.*')
    os.system('mv fort.* data_omp')
elif not os.path.exists("data_omp"):
    if os.path.exists("fort.101"):
        os.system('mkdir data_omp')
        os.system('mv fort.* data_omp')
    else:
        raise Exception("No data found. Please use the executable to generate data")
else:
    raise Exception("No data found. Please use the executable to generate data")

DIR ="data_omp"


data_num = np.arange(start=101, stop=Nt, step=datadt, dtype=int)

if (show_anim == True):
    def animate(i):
        file=DIR+'/fort.%d'%data_num[i]
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
