Framework for benchmarking of near-neighbor search methods for smoothed particle hydrodynamics
===========================================================

Introduction
-------------------

Turbofan engines are widely used in commercial aircraft.  New, more stringent requirements with regards to emissions, fuel consumption and noise pollution are putting pressure on aircraft engine manufacturers to increase the efficiency of their products. From a technical point of view, there are two options: increase the thermal efficiency of the turbine stage or increase the bypass ratio of the engine. The bypass ratio is the amount of air that passes around the turbine core rather than through it.  Generally, a higher bypass ratio results in a quieter, more efficient engine. To increase the bypass ratio, the diameter of the engine's fan blades must be increased.  However, increasing the fan diameter leads to an increase in the circumferential velocity of the fan blade tips.  At very high speeds, large increases in losses and noise emissions are observed.

In conventional turbofans, the fan and the low-pressure compressor and turbine which drives the fan are attached to single shaft.  In this configuration, the speed of the compressor stage is limited by the blade tip speeds to the fan.  With the addition of a gearbox between the fan and the compressor and turbine, the fan speed can be greatly reduced while the compressor and turbine can rotate much faster.  Both components can therefore operate at their optimal speeds, greatly increasing efficiency and reducing noise.

However, geared turbofans are not without drawbacks.  In addition to increased complexity and manufacturing cost, a significant amount of energy is lost as heat within the gearbox.  The cooling and lubrication of the gearbox are key challenges.  These functions are realized with oil jets arranged around the gears.  The interaction between the oil jets and the gear surfaces determines the cooling and lubrication performance as well as the further propagation of the oil within the gearbox.

Therefore, this interaction is a current focus of research at the Institute of Thermal Turbomachinery at the Karlsruhe Institute of Technology.  Experimental investigations in this area are difficult due to the small time scale and inaccessible location of the interactions. However, Computational Fluid Dynamics (CFD) methods offer possibilities for detailed investigation. One such method is Smoothed Particle Hydrodynamics (SPH), a particle-based method that is well-suited to modeling free surface flows and moving boundaries.  SPH, like other approaches to fluid dynamics modeling, is very computationally expensive. It is desirable to reduce the required computation time as much as possible. For this purpose, this work examines an approach to increasing the computational efficiency of the SPH solver and therefore reducing the required computation time. 


Motivation
-----------

Smoothed-particle hydrodynamics is a computational method which can be used to simulate mechanics of solids and fluids.  It is mesh-free and employs the Lagrangian approach, which makes it well-suited for complex problems with free surface flows and moving boundaries.

Compared to mesh-based methods, SPH requires a very large number of particles to ensure an equivalent resolution.  However, in applications where there is relatively little high-density fluid (e.g.  oil) in a computational space filled with low-density fluid (e.g.  air), the low-density phase cam be completely omitted.  This is results in a sparse computational domain, in which the amount of particles is small compared to the size of the domain.

During an SPH-method simulation, particles interact locally within a characteristic radius ("smoothing length").  In other words, each particle's behavior is influenced only by the particles surrounding it within a certain range.  Therefore, for each particle _p<sub>i</sub>_ in the domain, all points within a certain cut-off radius _r_ around the particle must be determined.  This type of search is called _fixed-radius near neighbor_ (frNN) search.

In the in-house code currently in use at the Institute for Thermal Turbomachinery, the fixed-radius near neighbors search is implemented using cell linked-lists (CLL, also cell lists, linked-cell method). In sparsely-filled computational domains as seen in simulations using the SPH method, other methods for frNN search may yield a performance advantage over the CLL method, in the form of reduced run time or memory use.

Fixed-Radius Near Neighbor Search
----------------------------------
For each point _p<sub>i</sub>_ within the computational domain, find all neighbors _p<sub>j</sub>_ that lie less than a cut-off radius _r = 3d<sub>x</sub>_ , away from the particle, where _d<sub>x</sub>_ is the mean particle spacing. This includes the particle _p<sub>1</sub>_ itself. The result is a set of interactions _p<sub>i</sub> <-> p<sub>j</sub>_, where  _p<sub>j</sub> <-> p<sub>i</sub>_ is considered identical to _p<sub>i</sub> <-> p<sub>j</sub>_ and is not repeated.}

Objective
-----------
The objective of this work is to compare alternative methods for solving the described fixed-radius near neighbor search problem to the existing solution using CLL. For this purpose, a benchmarking framework is created in which the a comparison can take place independently of the rest of the SPH code. Alternative solutions are researched and the most promising methods are implemented within the framework along with the CLL method. The benchmarks measure process runtime and memory use, which are then used to compare the search methods.

References
----------

1. [Smoothed-particle hydrodynamics](https://en.wikipedia.org/wiki/Smoothed-particle<sub>hydrodynamics). Wikipedia.
2. Hoetzlein, Rama (2014), ["Fast Fixed-Radius Nearest Neighbors: Interactive Million-Particle Fluids"](http://on-demand.gputechconf.com/gtc/2014/presentations/S4117-fast-fixed-radius-nearest-neighbor-gpu.pdf), GPU Technology Conference
3. Green, Simon (2012) [CUDA Particles](http://developer.download.nvidia.com/assets/cuda/files/particles.pdf), CUDA Toolkit Documentation. See also [here](https://docs.nvidia.com/cuda/cuda-samples/index.html#particles).
4. Mount, David (2010), [ANN Programming Manual](http://www.cs.umd.edu/~mount/ANN/Files/1.1.2/ANNmanual<sub>1.1.pdf)
