Nearest-neighbor search for smoothed particle hydrodynamics
===========================================================

Introduction to SPH
-------------------
Smoothed-particle hydrodynamics is a computational method which can be used to simulate mechanics of solids and fluids. It is mesh-free and employs the Lagrangian approach, which makes it well-suited for complex problems with free surface flows and moving boundaries. For fluid dynamics, it offers several key benefits:
- conservation of mass without extra computations
- pressure calculated locally instead of through solving a system of equations
- no explicit tracking of fluid boundaries necessary

Compared to mesh-based methods, SPH requires a very large number of particles to ensure an equivalent resolution. This is less of an issue in applications where there is relatively little high-density fluid (e.g. water) in a computational space filled with low-density fluid (e.g. air).

Particle interaction and nearest-neighbor search
------------------------------------------------
During an SPH-method simulation, particles interact locally within a characteristic radius ("smoothing length"). In other words, each particle's behavior is influenced only by the particles surrounding it within a certain range. Therefore, for each particle _p_ in the domain, all points within a certain radius _r_ (in three-dimensions) must be determined. This is called **fixed-radius near neighbors**.

#### Interesting note:
> Although the size of the smoothing length can be fixed in both space and time, this does not take advantage of the full power of SPH. By assigning each particle its own smoothing length and allowing it to vary with time, the resolution of a simulation can be made to automatically adapt itself depending on local conditions. For example, in a very dense region where many particles are close together, the smoothing length can be made relatively short, yielding high spatial resolution. Conversely, in low-density regions where individual particles are far apart and the resolution is low, the smoothing length can be increased, optimising the computation for the regions of interest. 
[Source](https://en.wikipedia.org/wiki/Smoothed-particle_hydrodynamics#Interpolations)

Objective
----------

For each point _p<sub>1</sub>_ within the computational domain (given in a list), find all neighbors _p<sub>2</sub>_ that lie less than three times the mean particle spacing _dx_ (~particle Diameter) away from the particle. This includes the particle itself. 

### Problem properties:
- low-dimensional (2D/3D)
- large N (~10e6 points)
- static for time step, but dynamic over time
- exact/approximate? FIXME

Since the neighbors must be found for all points, we can use the fact that, if we know that _p<sub>b</sub>_ is a neighbor of _p<sub>a</sub>_ then _p<sub>a</sub>_ is also a neighbor of _p<sub>b</sub>_.   

ANN Library
-----------

### Fixed-radius k-nearest neighbor search with ANN

From the ANN Progrograming Manual (page 7):
> In order to produce a true fixed-radius search,  first set k = 0 and run the procedure in order to obtain the number k' of points that lie within the radius bound. Then, allocate index and distance arrays of size k' each, and repeat the fixed-radius search by setting k = k' and passing in these two arrays.

References
----------

1. [Smoothed-particle hydrodynamics](https://en.wikipedia.org/wiki/Smoothed-particle_hydrodynamics). Wikipedia.
2. Hoetzlein, Rama (2014), ["Fast Fixed-Radius Nearest Neighbors: Interactive Million-Particle Fluids"](http://on-demand.gputechconf.com/gtc/2014/presentations/S4117-fast-fixed-radius-nearest-neighbor-gpu.pdf), GPU Technology Conference
3. Green, Simon (2012) [CUDA Particles](http://developer.download.nvidia.com/assets/cuda/files/particles.pdf), CUDA Toolkit Documentation. See also [here](https://docs.nvidia.com/cuda/cuda-samples/index.html#particles).
4. Mount, David (2010), [ANN Programming Manual](http://www.cs.umd.edu/~mount/ANN/Files/1.1.2/ANNmanual_1.1.pdf)