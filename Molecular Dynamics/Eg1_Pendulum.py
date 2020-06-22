#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.gridspec import GridSpec

#%%

class MrDynamics:
    
    '''
    This object - MrDynamics will generate list of co-ordinate and velocity of a 
    particle.
    
    g is the gravitational accelaration
    l is the length of an arm
    m is a mass of the particle.
    
    Tmax is the simulation time.
    Δt is the time step which act as a accuracy of Borish scheme.
    
    θ and ω are the initial angle and angular velocity, respectively.
    
    '''
    
    def __init__(self, g, l, m, Tmax, Δt, θ, ω):
        
        self.l = l
        
        # list of position, velocity, and time
        self.ListOfθ = [ θ ]
        self.ListOfω = [ ω ]
        self.time    = []
        
        # accelaration
        self.Acc = lambda θ, g, l : -(g/l)* np.sin(θ)
        
        # Run the algorithm
        self.Beeman(g, l, Tmax, Δt, θ, ω)
        
        # Energy
        self.KineticEnergy   = 0.5* m* ( l* np.array(self.ListOfω) )**2
        self.PotentialEnergy =-m* g* l* np.cos( np.array( self.ListOfθ ) )
        self.TotalEnergy     = self.KineticEnergy + self.PotentialEnergy

    def Beeman(self, g, l, Tmax, Δt, θ, ω):
        
        t = 0
        
        # Step - 1 : Initialization
        ao = self.Acc(θ, g, l)
        
        ω += ao* Δt
        θ += ω* Δt
        t += Δt
        
        a1 = self.Acc(θ, g, l)
        
        self.ListOfω.append(ω)
        self.ListOfθ.append(θ)
        
        
        # Step - 2 : Beeman Algorithm
        while (t <= Tmax):
            
            θ += ω* Δt + (4* a1 - ao)* Δt**2/ 6
            
            a2 = self.Acc(θ, g, l)
            
            ω += (5* a2 + 8* a1 - ao)* Δt/ 12
            
            self.ListOfω.append(ω)
            self.ListOfθ.append(θ)
            
            ao = a1
            a1 = a2
            t += Δt
        
        self.time = np.linspace(0, t, len(self.ListOfθ))
        

    def PlotTrajectory(self):
        
        fig = plt.figure( figsize = (80, 60) )
        gs = GridSpec(1, 2)
        
        ax1 = fig.add_subplot( gs[0, 0] )
        ax2 = fig.add_subplot( gs[0, 1] )
        
        # PLOT - 2: Energy        
        ax2.scatter(self.time[0], self.TotalEnergy[0], label = r'$E_{sys}$')
        ax2.scatter(self.time[0], self.KineticEnergy[0], label = r'KE')
        ax2.scatter(self.time[0], self.PotentialEnergy[0], label = r'PE')
        ax2.legend()
        
                
        for i in range(1, len(self.ListOfθ) ):
            
            # PLOT - 1: Model
            ax1.clear()
            
            x, y = self.l* np.sin(self.ListOfθ[i]), - self.l* np.cos(self.ListOfθ[i])
            
            ax1.plot([0, x], [0, y], linewidth = 3)
            ax1.scatter(x, y, color = 'red', marker = 'o', 
                        s = 500, alpha = 0.8)
            ax1.set_xlabel('X', fontweight = 'bold', fontsize = 14)
            ax1.set_ylabel('Y', fontweight = 'bold', fontsize = 14)
            ax1.set_xlim([-self.l - 0.5, self.l + 0.5])
            ax1.set_ylim([-self.l - 0.5, self.l + 0.5])
            
            # PLOT - 2: Energy 
            ax2.plot([ self.time[i-1], self.time[i] ], [ self.TotalEnergy[i-1], self.TotalEnergy[i] ], color = 'blue')
            ax2.plot([ self.time[i-1], self.time[i] ], [ self.KineticEnergy[i-1], self.KineticEnergy[i] ], color = 'orange')
            ax2.plot([ self.time[i-1], self.time[i] ], [ self.PotentialEnergy[i-1], self.PotentialEnergy[i] ], color = 'green')
            
            plt.pause(1E-11)


#%%

if __name__ == '__main__':
    
    g, l, m  = 10, 1, 1
    Tmax, Δt = 2, 1E-2
    θ, ω     = np.pi/4, 0
    
    Answer = MrDynamics(g, l, m, Tmax, Δt, θ, ω)
    Answer.PlotTrajectory()
