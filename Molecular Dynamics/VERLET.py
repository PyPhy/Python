#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

#%%

class MrDynamics:
    
    '''
    This object - MrDynamics will generate list of co-ordinate and velocity of a 
    particle.
    
    m is a mass of the particle.
    
    Tmax is the simulation time.
    Δt is the time step which act as a accuracy of Borish scheme.
    
    x and V are the initial position and velocity, respectively.
    
    '''
    
    def __init__(self, m, k, Tmax, Δt, x, V):
        
        # list of position, velocity, and time
        self.ListOfx = [ x ]
        self.ListOfV = [ V ]
        self.time    = []
        
        # accelaration
        self.a = lambda x, k, m : -(k/m)* x
        
        # numerical approch : Verlet
        self.Verlet(m, k, Tmax, Δt, x, V)
        
        # analytical result
        omg = (k/ m)**0.5
        self.Position = x* np.cos(omg* self.time)
        self.Velocity =-x* omg* np.sin(omg* self.time)
        
        # Error
        δx = 100* ( np.array(self.Position[1:]) - np.array(self.ListOfx[1:]) )/ np.array(self.Position[1:])
        δV = 100* ( np.array(self.Velocity[1:]) - np.array(self.ListOfV[1:]) )/ np.array(self.Velocity[1:])
        
        print( 'Median error in position ' + str(np.median( abs(δx) )) + ' %' )
        print( 'Median error in velocity ' + str(np.median( abs(δV) )) + ' %' )


    def Verlet(self, m, k, Tmax, Δt, x, V):
        
        t = 0
        
        # Step - 1 : Initialization for verlet
        xo = x
        
        V += self.a(xo, k, m)* Δt
        x1 = xo + V* Δt
        t += Δt
        
        self.ListOfx.append(x1)
        
        # Step - 2 : Verlet Algorithm
        while (t <= Tmax):
            
            x2 = 2* x1 - xo + self.a(x1, k, m)* Δt**2
            
            self.ListOfx.append(x2)
            
            xo = x1
            x1 = x2
            t += Δt
        
        # Step - 3 : Velocity
        Vel = lambda Pos, Δt : [(Pos[i+2] - Pos[i])/ (2* Δt) for i in range(0, len(Pos) - 2)]
        
        self.ListOfV = self.ListOfV + Vel( self.ListOfx, Δt )
        self.ListOfx = self.ListOfx[:-1]
        self.time    = np.linspace(0, t, len(self.ListOfx))
        
        
    def PlotTrajectory(self):
        
        fig = plt.figure( figsize = (80, 60) )
        gs = GridSpec(2, 1)
        
        ax1 = fig.add_subplot( gs[0, 0] )
        ax2 = fig.add_subplot( gs[1, 0] )
        
        ax1.plot(self.time, self.Position, label = 'Analytical')
        ax1.plot(self.time, self.ListOfx, 'ro', alpha = 0.5, label = 'Verlet')
        ax1.set_ylabel('x(t)', fontweight = 'bold', fontsize = 14)
        ax1.grid()
        ax1.legend()
        
        ax2.plot(self.time, self.Velocity)
        ax2.plot(self.time, self.ListOfV, 'ro', alpha = 0.5)
        ax2.set_xlabel('time', fontweight = 'bold', fontsize = 14)
        ax2.set_ylabel('v(t)', fontweight = 'bold', fontsize = 14)
        ax2.grid()
        
        plt.show()

#%%

if __name__ == '__main__':
    
    m, k     = 1, 1        # Mass and Spring constant
    Tmax, Δt = 100, 0.2
    x, V     = 1, 0

    Answer = MrDynamics(m, k, Tmax, Δt, x, V)
    Answer.PlotTrajectory()
