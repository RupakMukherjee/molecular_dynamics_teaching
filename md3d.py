#!/usr/bin/ python

"""
** Molecular Dynamics in 3D **

@file                md3d.py
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
show_anim = False  #Set "False" for no visualization
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
Lz  = 10.0  # System length in Z

Vxmax = 1.0 # Maximum velocity in X
Vymax = 1.0 # Maximum velocity in Y
Vzmax = 1.0 # Maximum velocity in Z

tmax = 10.0  # Final time
dt   = 0.010 # time step size
Nt   = round(tmax/dt) #number of time steps

svx  = 0.0  # velocity sum correction term in X
svy  = 0.0  # velocity sum correction term in Y
svz  = 0.0  # velocity sum correction term in Z

x  = np.empty(N, dtype=float)
y  = np.empty(N, dtype=float)
z  = np.empty(N, dtype=float)
vx = np.empty(N, dtype=float)
vy = np.empty(N, dtype=float)
vz = np.empty(N, dtype=float)
ux = np.empty(N, dtype=float)
uy = np.empty(N, dtype=float)
uz = np.empty(N, dtype=float)
ax = np.empty(N, dtype=float)
ay = np.empty(N, dtype=float)
az = np.empty(N, dtype=float)
time  = np.linspace(0,tmax,Nt)

data_num = np.arange(start=0, stop=Nt, step=datadt, dtype=int)

#==================== Animation Function===================
if (show_anim == True):
    def animate(i):
        file=DIR+'/data%d'%data_num[i]+'.txt'
        datax,datay,dataz = np.loadtxt(file, unpack=True)
        ax1.cla()
        img1 = ax1.scatter(datax,datay,dataz,marker='o',color='b',alpha=1.0,s=10)
        ax1.set_title('TimeSteps = %d'%i+'\n Phase Space')
        ax1.set_xlabel("$x$")
        ax1.set_ylabel("$y$")
        ax1.set_xlim([-Lx, Lx])
        ax1.set_ylim([-Ly, Ly])
        ax1.set_ylim([-Lz, Lz])

#=============== Initial Condition ==================

for i in range(N):
    x[i] = (random.random())*2.0*Lx - Lx
    y[i] = (random.random())*2.0*Ly - Ly
    z[i] = (random.random())*2.0*Lz - Lz
    vx[i] = (random.random())*Vxmax - Vxmax/2.0
    vy[i] = (random.random())*Vymax - Vymax/2.0
    vz[i] = (random.random())*Vzmax - Vzmax/2.0
    svx = svx + vx[i]
    svy = svy + vy[i]
    svz = svz + vz[i]

for i in range(N):
    vx[i] = vx[i] - svx/N
    vy[i] = vy[i] - svy/N
    vz[i] = vz[i] - svz/N


for i in range(N):
    ax[i] = 0.0
    ay[i] = 0.0
    az[i] = 0.0
    for j in range(N):
        if (i != j):
            xdiff = ( x[i]-x[j] ) - round((x[i]-x[j])/(2.0*Lx)) * 2.0*Lx
            ydiff = ( y[i]-y[j] ) - round((y[i]-y[j])/(2.0*Ly)) * 2.0*Ly
            zdiff = ( z[i]-z[j] ) - round((z[i]-z[j])/(2.0*Lz)) * 2.0*Lz
            r = math.sqrt(xdiff*xdiff + ydiff*ydiff + zdiff*zdiff)
            fx = xdiff/(r*r*r)
            fy = ydiff/(r*r*r)
            fz = zdiff/(r*r*r)
            ax[i] = ax[i] + fx
            ay[i] = ay[i] + fy
            az[i] = az[i] + fz

#======================== Time Loop ===============================
for t in range(len(time)):
    KE = 0.0
    for i in range(N):
        ux[i] = vx[i] + ax[i] * dt/2.0
        uy[i] = vy[i] + ay[i] * dt/2.0
        uz[i] = vz[i] + az[i] * dt/2.0
        x[i] = x[i] + ux[i] * dt
        y[i] = y[i] + uy[i] * dt
        z[i] = z[i] + uz[i] * dt
        x[i] = x[i] - (int(x[i]/Lx)) * 2.0 * Lx      # Periodic Boundary Condition
        y[i] = y[i] - (int(y[i]/Ly)) * 2.0 * Ly      # Periodic Boundary Condition
        z[i] = z[i] - (int(z[i]/Lz)) * 2.0 * Lz      # Periodic Boundary Condition

    for i in range(N):
        ax[i] = 0.0
        ay[i] = 0.0
        az[i] = 0.0
        for j in range(N):
            if (i != j):
                xdiff = ( x[i]-x[j] ) - round((x[i]-x[j])/(2.0*Lx)) * 2.0*Lx
                ydiff = ( y[i]-y[j] ) - round((y[i]-y[j])/(2.0*Ly)) * 2.0*Ly
                zdiff = ( z[i]-z[j] ) - round((z[i]-z[j])/(2.0*Lz)) * 2.0*Lz
                r = math.sqrt(xdiff*xdiff + ydiff*ydiff + zdiff*zdiff)
                fx = xdiff/(r*r*r)
                fy = ydiff/(r*r*r)
                fz = zdiff/(r*r*r)
                ax[i] = ax[i] + fx
                ay[i] = ay[i] + fy
                az[i] = az[i] + fz

    for i in range(N):
        vx[i] = ux[i] + ax[i] * dt / 2.0
        vy[i] = uy[i] + ay[i] * dt / 2.0
        vz[i] = uz[i] + az[i] * dt / 2.0
        KE = KE + ( vx[i]*vx[i] + vy[i]*vy[i] + vz[i]*vz[i] ) / 2.0

    #============ Diagnostics Write ===================
    if t%datadt==0:
        print('TimeSteps = %d'%int(t)+' of %d'%Nt)
        f = open('data/data%d'%int(t)+'.txt', 'w')
        for i in range(N):
            f.write("%f"%x[i]+" %f"%y[i]+" %f"%z[i]+"\n")
        f.close()
    #============  Thermostat =========================
    tau = 10.0*dt
    scl = math.sqrt(1.0 + (dt/tau) * ((Temp/(2.0*KE/(3.0*float(N)) )) -1.0))

    if (t <= tmax/2.0):
        for i in range(N):
            vx[i] = scl * vx[i]
            vy[i] = scl * vy[i]
            vz[i] = scl * vz[i]
    else:
        vx[i] = vx[i]
        vy[i] = vy[i]
        vz[i] = vz[i]

#==================== End of Time Loop ============================
#==================== Animation =======================
if (show_anim == True):
    # fig,ax1 = plt.subplots(1,1,1, projection='3d')
    fig = plt.figure(figsize=(6, 6))
    ax1 = plt.axes(projection ="3d")
    ani = animation.FuncAnimation(fig,animate,frames=len(data_num),interval=interval*1e+3,blit=False)
    plt.show()
