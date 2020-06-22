#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from numpy.linalg import norm
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.gridspec import GridSpec

#%%

class MrDynamics:
    
    def __init__(self, ε, rm, m, Tmax, Δt, r, v):
        
        self.ε, self.rm = ε, rm
        
        # list of position, velocity, and time
        self.ListOfr = [ r ]
        self.ListOfv = [ v ]
        self.time    = []
        
        # accelaration
        self.Acc = lambda r, ε, rm, m : (12* ε/ rm**2)* ( (rm/r)**14 - (rm/r)**8 )* r/ m
        
        # Run the algorithm
        self.Beeman(ε, rm, m, Tmax, Δt, r, v)
        
        # Energy
        self.KE = 0.5* m* np.array(self.ListOfv)**2
        self.PE = np.array([ε* ( (rm/r)**12 - 2*(rm/r)**6 ) for r in self.ListOfr])
        self.E  = self.KE + np.array(self.PE)
        
    
    def Beeman(self, ε, rm, m, Tmax, Δt, r, v):
        
        t = 0
        
        # Step - 1 : Initialization
        ao = self.Acc(r, ε, rm, m)
        
        v += ao* Δt
        r += v* Δt
        t += Δt
        
        a1 = self.Acc(r, ε, rm, m)
        
        self.ListOfr.append(r)
        self.ListOfv.append(v)
        
        # Step - 2 : Beeman Algorithm
        while (t <= Tmax):
            
            r += v* Δt + (4* a1 - ao)* Δt**2/ 6
            
            a2 = self.Acc(r, ε, rm, m)
            
            v += (5* a2 + 8* a1 - ao)* Δt/ 12
            
            self.ListOfr.append(r)
            self.ListOfv.append(v)
            
            ao = a1
            a1 = a2
            t += Δt
        
        self.time = np.linspace(0, t, len(self.ListOfr))
        

    def PlotTrajectory(self):
        
        fig = plt.figure( figsize = (80, 60) )
        gs = GridSpec(1, 2)
        
        ax1 = fig.add_subplot( gs[0, 0] )
        ax2 = fig.add_subplot( gs[0, 1] )
        
        # PLOT - 2: Energy        
        ax2.scatter(self.time[0], self.E[0], label = r'$E_{sys}$')
        ax2.scatter(self.time[0], self.KE[0], label = r'KE')
        ax2.scatter(self.time[0], self.PE[0], label = r'PE')
        ax2.legend()
        
                
        for i in range(1, len(self.time) ):
            
            # PLOT - 1: Model
            ax1.clear()
            
            ax1.scatter(self.ListOfr[i], 0, color = 'blue', marker = 'o', 
                        s = 500, alpha = 0.8)
            ax1.set_xlim([0, 3])
            ax1.set_xlabel('X', fontweight = 'bold', fontsize = 14)
            ax1.set_ylabel('Y', fontweight = 'bold', fontsize = 14)
            ax1.grid()
            
            # Potential energy curve
            r = np.linspace(0.8, 3, 100)
            U = np.array(self.ε* ((self.rm/r)**12 - 2*(self.rm/r)**6))
            ax1.plot(r, U, 'r', label = 'LJ potential')
            ax1.legend()
            
            # PLOT - 2: Energy 
            ax2.plot([ self.time[i-1], self.time[i] ], [ self.E[i-1], self.E[i] ], color = 'blue')
            ax2.plot([ self.time[i-1], self.time[i] ], [ self.KE[i-1], self.KE[i] ], color = 'orange')
            ax2.plot([ self.time[i-1], self.time[i] ], [ self.PE[i-1], self.PE[i] ], color = 'green')
            
            plt.pause(1E-11)


#%%

if __name__ == '__main__':
    
    ε, rm, m = 2, 1, 1
    Tmax, Δt = 8E-1, 5E-3
    r, v     = 1.5, -2
    
    Answer = MrDynamics(ε, rm, m, Tmax, Δt, r, v)
    Answer.PlotTrajectory()
