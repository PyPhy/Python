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
    charged particle.
    
    q and m are the charge and mass of the particle.
    
    Tmax is the simulation time.
    Δt is the time step which act as a accuracy of Borish scheme.
    
    r and V are the initial position and velocity, respectively.
    
    E and B are electro-static field and magnetic field, respectively.
    
    '''
    
    def __init__(self, q, m, Tmax, Δt, r, V, E, B):
        
        # list of position and velocity
        self.ListOfx,  self.ListOfy,  self.ListOfz  = [ r[0] ],  [ r[1] ],  [ r[2] ]
        self.ListOfVx, self.ListOfVy, self.ListOfVz = [ V[0] ],  [ V[1] ],  [ V[2] ]
        
        self.Boris(q, m, Tmax, Δt, r, V, E, B)
        
        
    def Boris(self, q, m, Tmax, Δt, r, V, E, B):
        
        x,   y,  z = r
        Vx, Vy, Vz = V
        Ex, Ey, Ez = E
        Bx, By, Bz = B
        
        # Step - 1 : Half step velocity
        Vx += ( (q/m)* (Ex + Bz* Vy - By* Vz) )* (Δt/2)
        Vy += ( (q/m)* (Ey + Bx* Vz - Bz* Vx) )* (Δt/2)
        Vz += ( (q/m)* (Ez + By* Vx - Bx* Vy) )* (Δt/2)
        
        # Step - 2 : Boris Algorithm
        t  = 0
        qd = (q* Δt)/ (2* m)
        
        while (t <= Tmax):
            
            hx  = qd* Bx
            hy  = qd* By
            hz  = qd* Bz
            
            Sx  = 2* hx/ (1 + ( hx**2 + hy**2 + hz**2 ) )
            Sy  = 2* hy/ (1 + ( hx**2 + hy**2 + hz**2 ) )
            Sz  = 2* hz/ (1 + ( hx**2 + hy**2 + hz**2 ) )
            
            Ux  = Vx + qd* Ex
            Uy  = Vy + qd* Ey
            Uz  = Vz + qd* Ez
            
            Ux_d = Ux + Sz* ( Uy + Uz*hx - hz*Ux ) - Sy* ( Uz + Ux*hy - hx*Uy )
            Uy_d = Uy + Sx* ( Uz + Ux*hy - hx*Uy ) - Sz* ( Ux + Uy*hz - hy*Uz )
            Uz_d = Uz + Sy* ( Ux + Uy*hz - hy*Uz ) - Sx* ( Uy + Uz*hx - hz*Ux )
            
            Vx = Ux_d + qd* Ex
            Vy = Uy_d + qd* Ey
            Vz = Uz_d + qd* Ez
            
            x += Vx* Δt
            y += Vy* Δt
            z += Vz* Δt
            
            self.ListOfx.append(x)
            self.ListOfy.append(y)
            self.ListOfz.append(z)
            
            t += Δt
        
        
        # Step - 3 : Find velocity
        
        Vel = lambda Pos, Δt : [(Pos[i+2] - Pos[i])/ (2* Δt) for i in range(0, len(Pos) - 2)]
        
        self.ListOfVx = self.ListOfVx + Vel( self.ListOfx, Δt )
        self.ListOfVy = self.ListOfVy + Vel( self.ListOfy, Δt )
        self.ListOfVz = self.ListOfVz + Vel( self.ListOfz, Δt )
        
        self.ListOfx = self.ListOfx[:-1]
        self.ListOfy = self.ListOfy[:-1]
        self.ListOfz = self.ListOfz[:-1]
        

    def PlotTrajectory(self):
        
        fig = plt.figure( figsize = (80, 60) )
        
        gs = GridSpec(2, 2)
        
        ax1 = fig.add_subplot( gs[0, 0], projection = '3d' )
        ax2 = fig.add_subplot( gs[0, 1] )
        ax3 = fig.add_subplot( gs[1, 0] )
        ax4 = fig.add_subplot( gs[1, 1] )
        
        ax1.plot(self.ListOfx, self.ListOfy, self.ListOfz, c = 'r', linewidth = 2)
        ax1.scatter(self.ListOfx[0], self.ListOfy[0], self.ListOfz[0])
        
        ax1.set_xlabel('X', fontsize = 12, fontweight = 'bold')
        ax1.set_ylabel('Y', fontsize = 12, fontweight = 'bold')
        ax1.set_zlabel('Z', fontsize = 12, fontweight = 'bold')
        
        ax2.plot(self.ListOfx, self.ListOfVx)
        ax2.scatter(self.ListOfx[0], self.ListOfVx[0], color = 'r')
        ax2.set_title('x | Vx')
        ax2.grid()
        
        ax3.plot(self.ListOfy, self.ListOfVy)
        ax3.scatter(self.ListOfy[0], self.ListOfVy[0], color = 'r')
        ax3.set_title('y | Vy')
        ax3.grid()
        
        ax4.plot(self.ListOfz, self.ListOfVz)
        ax4.scatter(self.ListOfz[0], self.ListOfVz[0], color = 'r')
        ax4.set_title('z | Vz')
        ax4.grid()

#%%

if __name__ == '__main__':

    q, m = 1, 1
    Δt, Tmax = 1E-2, 5
    
    r = [0, 0, 0]
    V = [1, 0, 1]
    
    E = [0, 0, 0]
    B = [0, 0, 10]

    Answer = MrDynamics(q, m, Tmax, Δt, r, V, E, B)
    
    Answer.PlotTrajectory()
