#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 17:01:44 2020

@author: divyang
"""

from numpy import array, sum, append, delete, shape, sqrt, linspace
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

#%%

class Energy:
    
    '''
        This class will calculate Kinetic, Potential, and Total Energy per particle.
    '''
    
    def __init__(self, M, N, x, y, Vx, Vy):
        
        self.M,  self.N  = M,  N
        self.x,  self.y  = x,  y
        self.Vx, self.Vy = Vx, Vy


    def Pot(self, x, y):
        
        W = 0
        
        for i in range(0, self.N):
            for j in range(0, self.N):
                if (i != j):
                    
                    r = ( (x[i] - x[j])**2 + (y[i] - y[j])**2 )**0.5
                    
                    W += - 0.5* self.M[i]* self.M[j]/ r

        return W
    

    def EnergyCalculations(self):

        # kinetic energy
        KE = 0
        for i in range(0, len(self.M)):
            KE += 0.5* self.M[i]* ( self.Vx[:,i]**2 + self.Vy[:,i]**2 )
        
        # KE = 0.5* sum( self.Vx**2 + self.Vy**2, axis=1)

        # electrostatic potential energy
        p, _ = shape( self.x )
        PE = array([])
        for i in range(0, p):
            PE_dt = self.Pot( self.x[i,:], self.y[i,:] )
            PE = append(PE, PE_dt)

        # Total energy
        E = KE + PE

        # Energy per particle
        E  = E / self.N
        KE = KE/ self.N
        PE = PE/ self.N

        return E, KE, PE

#%%

class PlotData:
    
    def __init__(self):

        # Read Data Files
        M    = pd.read_csv(r'Data/M.txt', header = None, sep = ' ')
        x    = pd.read_csv(r'Data/x.txt',  header = None, sep = ' ')
        y    = pd.read_csv(r'Data/y.txt',  header = None, sep = ' ')
        Vx   = pd.read_csv(r'Data/vx.txt', header = None, sep = ' ')
        Vy   = pd.read_csv(r'Data/vy.txt', header = None, sep = ' ')
        data = pd.read_csv('Inputs.txt', header = None, sep = '=')
        data = data[1].tolist()

        self.M    =  M.values.tolist()[0]
        self.N    = int(data[0])
        self.x    = array(x)
        self.y    = array(y)
        self.Vx   = array(Vx)
        self.Vy   = array(Vy)
        
        p, _ = shape(x)
        self.time = linspace(0, (p-1)* data[2], p)
        
        self.E, self.KE, self.PE = Energy(self.M, self.N, self.x, self.y, self.Vx, self.Vy).EnergyCalculations()

    def AnimamteParticles(self, Skip = 20):

        gs = GridSpec(1, 2)

        fig = plt.figure( figsize = (80, 60) )
        ax1 = fig.add_subplot( gs[0, 0] )
        ax2 = fig.add_subplot( gs[0, 1] )

        for frames, t in enumerate( self.time[::Skip] ):

            fS = frames* Skip

            # PLOT - 1: Particles
            ax1.clear()

            ax1.scatter( self.x[fS], self.y[fS], marker = 'o' )

            Vmag = ( self.Vx[fS]**2 + self.Vy[fS]**2 )**0.5

            ax1.quiver(  self.x[fS],  self.y[fS], \
                        self.Vx[fS], self.Vy[fS], \
                        Vmag, width = 0.003 )

            ax1.set_xlabel('x', fontsize = 16)
            ax1.set_ylabel('y', fontsize = 16)
            ax1.set_xlim([-1.5, 1.5])
            ax1.set_ylim([-1.5, 1.5])

            # PLOT - 2: Energy
            if (frames == 0):

                e  = self.E[fS]
                ke = self.KE[fS]
                pe = self.PE[fS]
                to = t

                ax2.scatter(to,  e, label = r'$E_{sys}$')
                ax2.scatter(to, ke, label = r'KE')
                ax2.scatter(to, pe, label = r'PE')

                ax2.legend()

            else:

                ax2.plot([to,t], [ e, self.E[fS]  ], color = 'blue')
                ax2.plot([to,t], [ke, self.KE[fS] ], color = 'orange')
                ax2.plot([to,t], [pe, self.PE[fS] ], color = 'green')

                e  = self.E[fS]
                ke = self.KE[fS]
                pe = self.PE[fS]
                to = t
            
            plt.pause(1e-11)


    def PlotEnergy(self):
        
        fig = plt.figure('Energy conservation')
        plt.plot( self.time, self.E,  label = r'$E_{sys}$')
        plt.plot( self.time, self.KE, label = r'KE')
        plt.plot( self.time, self.PE, label = r'PE')
        plt.legend()
        plt.grid()
        plt.show()


#%%

if __name__ == '__main__':

    DoMyWork = PlotData()
    # DoMyWork.AnimamteParticles(Skip = 25)
    DoMyWork.PlotEnergy()
