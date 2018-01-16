''' 

Copyright 2018 University of Li�ge

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. 

'''

#! /usr/bin/env python
# -*- coding: latin-1; -*-
# $Id: $

import sys, os, os.path

runPath = os.path.dirname(sys.modules[__name__].__file__)
filePath = os.path.abspath(os.path.dirname(sys.argv[0]))
fileName = os.path.splitext(os.path.basename(__file__))[0]

import pfem

import pfemtools as wt
import viewer as v
    
w = None

class Module:
    def __init__(self, w, msh, pbl, scheme, extManager, gui):
       self.w = w
       self.msh = msh
       self.pbl = pbl       
       self.scheme = scheme
       self.extManager = extManager
       self.gui = gui

def getPfem():
    global w
    if w: return w
    w = pfem
    
    mshFile = runPath+os.sep+'waterColoumnWithElasticGate_Mtf_Pfem.msh'
    
    rho0 = 1000.
    mu = 0.001
    
    pbl = w.Problem()
    pbl.rho0 = rho0
    pbl.mu = mu
    pbl.nonLinAlgorithm = 1
    pbl.solScheme = 1
    pbl.alpha = 1.3
    pbl.extP = 0.
    pbl.scalingU = 2.0
    pbl.bodyForceY = -9.81
    
    msh = w.MshData(pbl)
    msh.load(mshFile)
    print msh
    
    scheme = w.BackwardEuler(msh, pbl)
    
    # w.Medium(msh, 100, 0., 0., 0., 4)
    w.Medium(msh, 17, mu, rho0, 3)
    w.Medium(msh, 16, mu, rho0, 1)
    w.Medium(msh, 20, mu, rho0, 1)
    
    # boundaries
    w.Boundary(msh, 18, 3, pbl.extP)
    w.Boundary(msh, 16, 1, 0.0)
    w.Boundary(msh, 16, 2, 0.0)
    w.Boundary(msh, 17, 1, -1.0e-15)
    w.Boundary(msh, 17, 2, -1.0e-15)
    
    scheme.savefreq=1
    scheme.nthreads=3
    scheme.gamma = 0.5
    scheme.omega = 0.5
    scheme.addRemoveNodesOption = True
    
    #Results
    extManager = w.ExtractorsManager(msh)
    extManager.add(1,w.PositionExtractor(msh,9))
    extManager.add(3,w.IntForceExtractor(msh,17))
    '''extManager.add(2,w.IntForceExtractor(msh,1))
    extManager.add(3,w.ExtForceExtractor(msh,1))
    extManager.add(4,w.IneForceExtractor(msh,1))
    extManager.add(5,w.IntForceExtractor(msh,6))
    extManager.add(6,w.ExtForceExtractor(msh,6))
    extManager.add(7,w.IneForceExtractor(msh,6))
    extManager.add(8,w.PressureExtractor(msh,1))
    extManager.add(9,w.VelocityExtractor(msh,"Water"))
    extManager.add(10,w.MassExtractor(msh,"Water"))
    extManager.add(11,wt.KineticEnergyExtractor(msh,pbl,"Water"))
    extManager.add(12,wt.ViscousEnergyExtractor(msh,pbl,scheme,"Water"))'''
    
    gui = v.MeshViewer(msh, scheme, True) 
    
    return Module(w, msh, pbl, scheme, extManager, gui)

def getRealTimeExtractorsList(pfem):
    
    extractorsList = []

    # --- Extractors list starts --- #
    # --- Extractors list ends --- #

    return extractorsList