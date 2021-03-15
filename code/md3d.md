# Code Description

## md3d.f95

Simple three dimensional molecular dynamics code for point particles interacting via coulomb potential.

```fortran
program molecular_dynamics_3d
implicit none
integer N,i,j,p
real*8 Lx,Ly,Lz,Vxmax,Vymax,Vzmax,tmax,dt,svx,svy,svz,fx,fy,fz,scl,KE,Temp,t,xdiff,ydiff,zdiff,r,tau
real, dimension (100) :: x,y,z,vx,vy,vz,ux,uy,uz,ax,ay,az
integer, parameter :: seed = 99999999
call srand(seed)

Temp = 0.010d0

N = 100

Lx = 10.0d0
Ly = 10.0d0
Lz = 10.0d0

Vxmax = 1.0d0
Vymax = 1.0d0
Vzmax = 1.0d0

tmax = 1.0d0
dt = 0.010d0

svx = 0.0d0
svy = 0.0d0
svz = 0.0d0

!=============== Initial Condition ==================

do i = 1,N
  x(i) = (rand())*2.0d0*Lx - Lx
  y(i) = (rand())*2.0d0*Ly - Ly
  z(i) = (rand())*2.0d0*Lz - Lz
  vx(i) = (rand())*Vxmax - Vxmax/2.0d0
  vy(i) = (rand())*Vymax - Vymax/2.0d0
  vz(i) = (rand())*Vzmax - Vzmax/2.0d0
  svx = svx + vx(i)
  svy = svy + vy(i)
  svz = svz + vz(i)
enddo  

do i = 1,N
  vx(i) = vx(i) - svx/dfloat(N)
  vy(i) = vy(i) - svy/dfloat(N)
  vz(i) = vz(i) - svz/dfloat(N)
enddo

do i = 1,N
  ax(i) = 0.0d0
  ay(i) = 0.0d0
  az(i) = 0.0d0
    do j = 1,N
      if (i .ne. j) then
        xdiff = ( x(i)-x(j) ) - nint ((x(i)-x(j))/(2.0d0*Lx)) * 2.0d0*Lx
        ydiff = ( y(i)-y(j) ) - nint ((y(i)-y(j))/(2.0d0*Ly)) * 2.0d0*Ly
        zdiff = ( z(i)-z(j) ) - nint ((z(i)-z(j))/(2.0d0*Lz)) * 2.0d0*Lz
        r = dsqrt (xdiff*xdiff + ydiff*ydiff + zdiff*zdiff)
        fx = xdiff/(r*r*r)
        fy = ydiff/(r*r*r)
        fz = zdiff/(r*r*r)
        ax(i) = ax(i) + fx
        ay(i) = ay(i) + fy
        az(i) = az(i) + fz
      endif
    enddo 
enddo

!=============== Time Loop =======================

do t = 0.0d0+dt, tmax, dt

KE = 0.0d0

  do i = 1,N 
    ux(i) = vx(i) + ax(i) * dt / 2.0d0
    uy(i) = vy(i) + ay(i) * dt / 2.0d0
    uz(i) = vz(i) + az(i) * dt / 2.0d0
    x(i) = x(i) + ux(i) * dt
    y(i) = y(i) + uy(i) * dt
    z(i) = z(i) + uz(i) * dt
    x(i) = x(i) - (int(x(i)/Lx)) * 2.0d0 * Lx      ! Periodic Boundary Condition
    y(i) = y(i) - (int(y(i)/Ly)) * 2.0d0 * Ly      ! Periodic Boundary Condition
    z(i) = z(i) - (int(z(i)/Lz)) * 2.0d0 * Lz      ! Periodic Boundary Condition
  enddo


  do i = 1,N
    ax(i) = 0.0d0
    ay(i) = 0.0d0
    az(i) = 0.0d0 
       do j = 1,N
        if (i .ne. j) then
          xdiff = ( x(i)-x(j) ) - nint ((x(i)-x(j))/(2.0d0*Lx)) * 2.0d0*Lx
          ydiff = ( y(i)-y(j) ) - nint ((y(i)-y(j))/(2.0d0*Ly)) * 2.0d0*Ly
          zdiff = ( z(i)-z(j) ) - nint ((z(i)-z(j))/(2.0d0*Lz)) * 2.0d0*Lz
          r = dsqrt (xdiff*xdiff + ydiff*ydiff + zdiff*zdiff)
          fx = xdiff/(r*r*r)
          fy = ydiff/(r*r*r)
          fz = zdiff/(r*r*r)
          ax(i) = ax(i) + fx
          ay(i) = ay(i) + fy
          az(i) = az(i) + fz
        endif
      enddo
  enddo


  do i = 1,N
    vx(i) = ux(i) + ax(i) * dt / 2.0d0
    vy(i) = uy(i) + ay(i) * dt / 2.0d0
    vz(i) = uz(i) + az(i) * dt / 2.0d0
    KE = KE + ( vx(i)*vx(i) + vy(i)*vy(i) + vz(i)*vz(i)) / 2.0d0
  enddo

  do i = 1,N
    p = int(t/dt)
    write (p+100,*) x(i), y(i), z(i)
  enddo

  tau = 10.0d0 * dt
  scl = dsqrt (1.0d0 + (dt/tau) * ((Temp/(2.0d0*KE/(3.0d0*dfloat(N)) )) -1.0d0))
  
  if (t .le. tmax/2.0d0) then
    do i = 1,N
      vx(i) = scl * vx(i)
      vy(i) = scl * vy(i) 
      vz(i) = scl * vz(i)
    enddo
  else
    do i = 1,N
      vx(i) = vx(i)
      vy(i) = vy(i)
      vz(i) = vz(i)
    enddo
  endif

enddo !time

end program molecular_dynamics_3d

```
