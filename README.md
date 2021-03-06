# Orion - Python finite-difference solver

Orion is a Navier-Stokes solver written in Python.
It uses finite-difference method for calculating spatial derivatives and parallelized geometric multigrid method for solving
the pressure Poisson equation.

The solver is written in separate modules, which are listed below:

* ``main.py`` - This is the main file which needs to be executed to run the solver.
* ``fluidSolverNU.py`` - This is the solver called by main when computing hydrodynamics simulation on non-uniform grids.
* ``fluidSolverUG.py`` - This is the solver called by main when computing hydrodynamics simulation on uniform grids.
* ``globalVars.py`` - All the global parameters which the user needs to set are contained in this file.
* ``calculateFD.py`` - This module contains the functions to compute first and second derivatives of field variables.
* ``meshData.py`` - Grid data, like coordinates of collocated and staggered points, and grid transformation metrics are stored in this module.
* ``poissonSolverNU.py`` - The geometric multi-grid solver used to compute pressure correction on non-uniform grids is written in this module.
* ``poissonSolverUG.py`` - The geometric multi-grid solver used to compute pressure correction on uniform grids is written in this module.
* ``writeData.py`` - This module offers options to write solution data in either ASCII or HDF5 format.
* ``boundaryConditions.py`` - The boundary conditions to be applied on velocity and pressure are written in this module.
* ``vortexLES.py`` - The stretched spiral vortex LES model is implemented in this module to compute sub-grid stress terms.

## Installing Orion

To install ``Orion``, you need to first clone the git repository into your local machine

`git clone https://github.com/roshansamuel/orion.git`

``Orion`` is compatible with Python3, and can be executed by one of the following commands at the root folder of the solver, in the terminal.

`./main.py`

or

`python main.py`

Before executing the solver, please set the appropriate parameters for the Navier-Stokes problem by editing the `globalVars.py` file.
Brief descriptions of the parameters are given in comments within the file.

Please make sure that the following Python modules are installed before executing the solver.

* ``numpy`` - All array manipulations are performed using NumPy
* ``h5py`` - Solution files can be written in HDF5 format using this module
* ``multiprocessing`` - Parallel processing is performed using this module (parallelization is under development)

## License

``Orion`` is an open-source package made available under the New BSD License.

## References

Below is a list of useful articles that explains the multigrid-method used by ``Orion``

### Articles on multi-grid methods

1. http://math.mit.edu/classes/18.086/2006/am63.pdf
2. http://www.mgnet.org/mgnet-tuts.html
