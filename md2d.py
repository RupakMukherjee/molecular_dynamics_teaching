#!/usr/bin/ python

"""
** Molecular Dynamics in 2D **

@file                md2d.py
@author              Sayan Adhikari <sayan.adhikari@fys.uio.no>
@source              Rupak Mukherjee <rupakmukherjee06@gmail.com>
@date                03.09.2020

"""


import numpy as np
import pylab as plt
import random
import math
import matplotlib.animation as animation
import os

#========= Configuration ===========
show_anim = True  #Set "False" for no visualization
interval = 0.1    #in seconds (Interval of frames for animation)
datadt = 10       #Data dump period

#========== Data Directory Setup =============
if os.path.exists("data"):
    os.system('rm data/*')
else:
    os.system('mkdir data')

DIR ="data"
#========== Input Parameters ===========
random.seed(99999999)

Temp = 0.010

N   = 100   # Number of particles

Lx  = 10.0  # System length in X
Ly  = 10.0  # System length in Y

Vxmax = 1.0 # Maximum velocity in X
Vymax = 1.0 # Maximum velocity in Y

tmax = 10.0  # Final time
dt   = 0.010 # time step size
Nt   = round(tmax/dt) #number of time steps
svx  = 0.0  # velocity sum correction term in X
svy  = 0.0  # velocity sum correction term in Y

x  = np.empty(N, dtype=float)
y  = np.empty(N, dtype=float)
vx = np.empty(N, dtype=float)
vy = np.empty(N, dtype=float)
ux = np.empty(N, dtype=float)
uy = np.empty(N, dtype=float)
ax = np.empty(N, dtype=float)
ay = np.empty(N, dtype=float)
time  = np.linspace(0,tmax,Nt)

data_num = np.arange(start=0, stop=Nt, step=datadt, dtype=int)

#==================== Animation Function===================
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

#=============== Initial Condition ==================

for i in range(N):
    x[i] = (random.random())*2.0*Lx - Lx
    y[i] = (random.random())*2.0*Ly - Ly
    vx[i] = (random.random())*Vxmax - Vxmax/2.0
    vy[i] = (random.random())*Vymax - Vymax/2.0
    svx = svx + vx[i]
    svy = svy + vy[i]

for i in range(N):
    vx[i] = vx[i] - svx/N
    vy[i] = vy[i] - svy/N


for i in range(N):
    ax[i] = 0.0
    ay[i] = 0.0
    for j in range(N):
        if (i != j):
            xdiff = ( x[i]-x[j] ) -  round((x[i]-x[j])/(2.0*Lx)) * 2.0*Lx
            ydiff = ( y[i]-y[j] ) - round((y[i]-y[j])/(2.0*Ly)) * 2.0*Ly
            r = math.sqrt(xdiff*xdiff + ydiff*ydiff)
            fx = xdiff/(r*r*r)
            fy = ydiff/(r*r*r)
            ax[i] = ax[i] + fx
            ay[i] = ay[i] + fy

#======================== Time Loop ===============================
for t in range(len(time)):
    KE = 0.0
    for i in range(N):
        ux[i] = vx[i] + ax[i] * dt/2.0
        uy[i] = vy[i] + ay[i] * dt/2.0
        x[i] = x[i] + ux[i] * dt
        y[i] = y[i] + uy[i] * dt
        x[i] = x[i] - (int(x[i]/Lx)) * 2.0 * Lx      # Periodic Boundary Condition
        y[i] = y[i] - (int(y[i]/Ly)) * 2.0 * Ly      # Periodic Boundary Condition


    for i in range(N):
        ax[i] = 0.0
        ay[i] = 0.0
        for j in range(N):
            if (i != j):
                xdiff = ( x[i]-x[j] ) - round((x[i]-x[j])/(2.0*Lx)) * 2.0*Lx
                ydiff = ( y[i]-y[j] ) - round((y[i]-y[j])/(2.0*Ly)) * 2.0*Ly
                r = math.sqrt(xdiff*xdiff + ydiff*ydiff)
                fx = xdiff/(r*r*r)
                fy = ydiff/(r*r*r)
                ax[i] = ax[i] + fx
                ay[i] = ay[i] + fy

    for i in range(N):
        vx[i] = ux[i] + ax[i] * dt / 2.0
        vy[i] = uy[i] + ay[i] * dt / 2.0
        KE = KE + ( vx[i]*vx[i] + vy[i]*vy[i] ) / 2.0

    #============ Diagnostics Write ===================
    if t%datadt==0:
        print('TimeSteps = %d'%int(t)+' of %d'%Nt)
        f = open('data/data%d'%int(t)+'.txt', 'w')
        for i in range(N):
            f.write("%f"%x[i]+" %f"%y[i]+"\n")
        f.close()
    #============  Thermostat =========================
    tau = 10.0*dt
    scl = math.sqrt(1.0 + (dt/tau) * ((Temp/(2.0*KE/(3.0*float(N)) )) -1.0))

    if (t <= tmax/2.0):
        for i in range(N):
            vx[i] = scl * vx[i]
            vy[i] = scl * vy[i]
    else:
        vx[i] = vx[i]
        vy[i] = vy[i]

#==================== End of Time Loop ============================
#==================== Animation =======================
if (show_anim == True):
    fig,ax1 = plt.subplots(1,1,figsize=(6, 6))
    ani = animation.FuncAnimation(fig,animate,frames=len(data_num),interval=interval*1e+3,blit=False)
    plt.show()
