#!/usr/bin/python3

####################################################################################################
# Orion
# 
# Copyright (C) 2020, Roshan J. Samuel
#
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#     3. Neither the name of the copyright holder nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
####################################################################################################

# Import all necessary modules
from orion import globalVars as gv
import multiprocessing as mp
import numpy as np
import time

if gv.uniformGrid:
    if gv.planar:
        from orion.solvers import fluidSolverUG_d2 as fs
    else:
        from orion.solvers import fluidSolverUG_d3 as fs
else:
    if gv.planar:
        from orion.solvers import fluidSolverNU_d2 as fs
    else:
        from orion.solvers import fluidSolverNU_d3 as fs


####################################################################################################


# Main segment of code.
def main():
    gv.checkParams()

    if not gv.uniformGrid:
        fs.grid.initializeGrid()
        fs.grid.calculateMetrics()

    fs.initFields()
    gv.printParams()

    tStart = time.process_time()

    if gv.testPoisson:
        runMGTest()
    else:
        timeIntegrate()

    tEnd = time.process_time()
    tElap = tEnd - tStart
    
    print("Time elapsed = ", tElap)
    print("Simulation completed")

####################################################################################################


def runMGTest():
    if gv.planar:
        mgRHS = np.ones((fs.grid.L + 2, fs.grid.N + 2))
    else:
        mgRHS = np.ones((fs.grid.L + 2, fs.grid.M + 2, fs.grid.N + 2))

    mgLHS = np.zeros_like(mgRHS)
    
    if gv.solveMethod[0:2] == 'MG':
        fs.ps.multigrid(mgRHS, mgLHS)


####################################################################################################


def timeIntegrate():
    ndTime = 0.0
    fwTime = 0.0

    while True:
        if abs(fwTime - ndTime) < 0.5*gv.dt:
            fs.writeSoln(ndTime)
            fwTime += gv.fwInt

        fs.euler()

        maxDiv = fs.getDiv()
        if maxDiv[1] > 10.0:
            print("ERROR: Divergence has exceeded permissible limits. Aborting")
            quit()

        gv.iCnt += 1
        ndTime += gv.dt
        if gv.iCnt % gv.opInt == 0:
            print("Time: {0:9.5f}".format(ndTime))
            if gv.planar:
                print("Maximum divergence: {0:8.5f} at ({1:d}, {2:d})\n".format(maxDiv[1], maxDiv[0][0], maxDiv[0][1]))
            else:
                print("Maximum divergence: {0:8.5f} at ({1:d}, {2:d}, {3:d})\n".format(maxDiv[1], maxDiv[0][0], maxDiv[0][1], maxDiv[0][2]))

        if ndTime > gv.tMax:
            break


####################################################################################################


if __name__ == "__main__":
    main()

