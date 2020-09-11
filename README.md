Molecular Dynamics Simulation
==============================
A repository of molecular dynamics algorithm for teaching purpose.

Instructor: [Dr. Rupak Mukherjee](https://github.com/RupakMukherjee)

Contributor: [Dr. Sayan Adhikari](https://github.com/sayanadhikari)

A series of lectures (in [Hinglish](https://en.wikipedia.org/wiki/Hinglish)) are available on youtube based on the materials archived in this repository. Click on the link provided below to access the lectures.


[Webinar on "Pseudo Spectral Method"](https://www.youtube.com/playlist?list=PLbX_ZyxeXxSJWJw99-baWL3Xk5qoHKfGM)

[![Webinar on "Pseudo Spectral Method"](http://img.youtube.com/vi/vdv5kXVna0I/0.jpg)](https://www.youtube.com/embed/videoseries?list=PLbX_ZyxeXxSJWJw99-baWL3Xk5qoHKfGM)

# Code Description

## md2d.f95
At the beginning of the discussion, I started from Newton's law, concept of potential, classical collision / scattering of particles, simple harmonic motion, few numerical ODE solvers and delineated the basic molecular dynamics algorithm explicitly by hand. Starting from the idea of numerically solving the motion of one classical point particle in one dimension, I generelized to multiple classical point particles in one dimension and further towards multiple dimensions, explicitly working out the individual quantities (force, velocity etc.) by hand. The natural extension for multi-particle and in multiple dimensions is stressed in the rest of the part of the discussion while I was actually implementing it in the form of a baby test-code. Further I showed some movies of two dimensional and three dimensional simulation stressing few open problems in mind.

## md3d.f95
The first one third part of the discussion went into a different general topic of interest, talking about the wave equaitons in ideal compressible fluids, and relating them to plasmas crudely. In the middle part, I showed how easy it was to move to three dimensional from the two dimensional baby code that we developed in the last week. Then at the end, I talked about the periodic, reflecting boundary condition, implementation of different potentials (all binary), few references on normalization, touched upon few numerical caveats, quick idea about configurational temperature, time solvers for velocity dependent forces or in presence of magnetic fields and finally briefly outlined OpenMP or OpenACC parallelization. Thankfully, I did not have to work out the OpenMP and OpenACC architechture of the three dimensional version of the code explicitly. It was presented as a surprise gift to me on the next day! I really felt happy from the bottom of my heart!
