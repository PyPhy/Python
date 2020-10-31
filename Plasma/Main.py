#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 13:46:48 2020

@author: divyang
"""

import pandas as pd
import numpy as np

#%%

class Solver:
    
    def __init__(self):
        
        M    = pd.read_csv(r'Data/M.txt', header = None, sep = ' ')
        Q    = pd.read_csv(r'Data/Q.txt', header = None, sep = ' ')
        x    = pd.read_csv(r'Data/x.txt', header = None, sep = ' ')
        y    = pd.read_csv(r'Data/y.txt', header = None, sep = ' ')
        z    = pd.read_csv(r'Data/z.txt', header = None, sep = ' ')
        vx   = pd.read_csv(r'Data/vx.txt', header = None, sep = ' ')
        vy   = pd.read_csv(r'Data/vy.txt', header = None, sep = ' ')
        vz   = pd.read_csv(r'Data/vz.txt', header = None, sep = ' ')
        data = pd.read_csv('Inputs.txt', header = None, sep = '=')
        data = data[1].tolist()
        
        self.M  =  M.values.tolist()[0]
        self.Q  =  Q.values.tolist()[0]
        self.x  =  x.values.tolist()[0]
        self.y  =  y.values.tolist()[0]
        self.z  =  z.values.tolist()[0]
        self.Vx = vx.values.tolist()[0]
        self.Vy = vy.values.tolist()[0]
        self.Vz = vz.values.tolist()[0]
        self.N  = int(data[0])
        self.T  = float(data[1])
        self.Δt = float(data[2])
        

    def E(self):
        
        Ex, Ey, Ez = [0]* self.N, [0]* self.N, [0]* self.N
        
        # Case - 1 : Constant field
        # for i in range(0, self.N):
        #     Ex[i] += 1
        #     Ey[i] += 0
        #     Ez[i] += 0
        
        # Case - 2 : Nonuniform E Field
        for i in range(0, self.N):
            Ex[i] += 1* np.cos(2* self.x[i])
            Ey[i] += 0
            Ez[i] += 0
            
        # Case - 3 : Interaction field
        # for i in range(0, self.N):
        #     for j in range(0, self.N):
        #         if (i != j):
                    
        #             r3 = ( (self.x[i] - self.x[j])**2 + (self.y[i] - self.y[j])**2 + (self.z[i] - self.z[j])**2 )**1.5
                    
        #             Ex[i] += self.Q[j]* (self.x[i] - self.x[j])/ r3
        #             Ey[i] += self.Q[j]* (self.y[i] - self.y[j])/ r3
        #             Ez[i] += self.Q[j]* (self.z[i] - self.z[j])/ r3
        
        return Ex, Ey, Ez
    
    def B(self):
        
        Bx, By, Bz = [0]* self.N, [0]* self.N, [0]* self.N
        
        # Case - 1 : Constant B field
        # Bz = [1]* self.N
        
        # Case - 2 : Constant Grad - B
        # for i in range(0, self.N):
        #     Bz[i] = 3 + self.y[i]* 2
        
        # Case - 3 : Constant B theta field
        # Bt = 3
        
        # for i in range(0, self.N):
        #     t = np.arctan2(self.y[i], self.x[i])
            
        #     Bx[i] = - Bt* np.sin(t)
        #     By[i] =   Bt* np.cos(t)
        
        # Case - 4 : Magnetic Mirror
        # Bzo    = 1
        # dBz_dz = 1
        
        # for i in range(0, self.N):
            
        #     r = ( self.x[i]**2 + self.y[i]**2 )**0.5
        #     t = np.arctan2(self.y[i], self.x[i])
            
        #     Br = - 0.5* r* dBz_dz
            
        #     Bx[i] = Br* np.cos(t)
        #     By[i] = Br* np.sin(t)
        #     Bz[i] = Bzo + self.z[i]* dBz_dz

        return Bx, By, Bz
    
    
    def Boris(self):
        
        ListOfx = open(r'Data/x.txt', 'w')
        ListOfy = open(r'Data/y.txt', 'w')
        ListOfz = open(r'Data/z.txt', 'w')
        
        
        # Step - 1 : Half step velocity
        Ex, Ey, Ez = self.E()
        Bx, By, Bz = self.B()
        
        for i in range(0, self.N):
            
            QM = self.Q[i]/self.M[i]
            
            self.Vx[i] += QM* (Ex[i] + Bz[i]* self.Vy[i] - By[i]* self.Vz[i])* self.Δt /2
            self.Vy[i] += QM* (Ey[i] + Bx[i]* self.Vz[i] - Bz[i]* self.Vx[i])* self.Δt /2
            self.Vz[i] += QM* (Ez[i] + By[i]* self.Vx[i] - Bx[i]* self.Vy[i])* self.Δt /2
        
        
        # Step - 2 : Boris Algorithm
        t  = 0
        qd = [0]* self.N
        hx, hy, hz = [0]* self.N, [0]* self.N, [0]* self.N
        Sx, Sy, Sz = [0]* self.N, [0]* self.N, [0]* self.N
        Ux, Uy, Uz = [0]* self.N, [0]* self.N, [0]* self.N
        Ux_d, Uy_d, Uz_d = [0]* self.N, [0]* self.N, [0]* self.N
        
        for i in range(0, self.N):
            qd[i] = (self.Q[i]* self.Δt)/ (2* self.M[i])
        
        
        while (t <= self.T):
            
            for i in range(0, self.N):
            
                hx[i]   = qd[i]* Bx[i]
                hy[i]   = qd[i]* By[i]
                hz[i]   = qd[i]* Bz[i]
                
                Sx[i]   = 2* hx[i]/ (1 + ( hx[i]**2 + hy[i]**2 + hz[i]**2 ) )
                Sy[i]   = 2* hy[i]/ (1 + ( hx[i]**2 + hy[i]**2 + hz[i]**2 ) )
                Sz[i]   = 2* hz[i]/ (1 + ( hx[i]**2 + hy[i]**2 + hz[i]**2 ) )
                
                Ux[i]   = self.Vx[i] + qd[i]* Ex[i]
                Uy[i]   = self.Vy[i] + qd[i]* Ey[i]
                Uz[i]   = self.Vz[i] + qd[i]* Ez[i]
                
                Ux_d[i] = Ux[i] + Sz[i]* ( Uy[i] + Uz[i]*hx[i] - hz[i]*Ux[i] ) - Sy[i]* ( Uz[i] + Ux[i]*hy[i] - hx[i]*Uy[i] )
                Uy_d[i] = Uy[i] + Sx[i]* ( Uz[i] + Ux[i]*hy[i] - hx[i]*Uy[i] ) - Sz[i]* ( Ux[i] + Uy[i]*hz[i] - hy[i]*Uz[i] )
                Uz_d[i] = Uz[i] + Sy[i]* ( Ux[i] + Uy[i]*hz[i] - hy[i]*Uz[i] ) - Sx[i]* ( Uy[i] + Uz[i]*hx[i] - hz[i]*Ux[i] )
                
                self.Vx[i] = Ux_d[i] + qd[i]* Ex[i]
                self.Vy[i] = Uy_d[i] + qd[i]* Ey[i]
                self.Vz[i] = Uz_d[i] + qd[i]* Ez[i]
                
                self.x[i] += self.Vx[i]* self.Δt
                self.y[i] += self.Vy[i]* self.Δt
                self.z[i] += self.Vz[i]* self.Δt
                
            Ex, Ey, Ez = self.E()
            Bx, By, Bz = self.B()
            
            np.savetxt(ListOfx, np.array([self.x]) )
            np.savetxt(ListOfy, np.array([self.y]) )
            np.savetxt(ListOfz, np.array([self.z]) )
            
            t += self.Δt        
        
        ListOfx.close()
        ListOfy.close()
        ListOfz.close()


#%%

if __name__ == '__main__':
    
    Answer = Solver()
    Answer.Boris()
