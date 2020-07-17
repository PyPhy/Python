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
        vx   = pd.read_csv(r'Data/vx.txt', header = None, sep = ' ')
        vy   = pd.read_csv(r'Data/vy.txt', header = None, sep = ' ')
        data = pd.read_csv('Inputs.txt', header = None, sep = '=')
        data = data[1].tolist()
        
        self.M  =  M.values.tolist()[0]
        self.Q  =  Q.values.tolist()[0]
        self.x  =  x.values.tolist()[0]
        self.y  =  y.values.tolist()[0]
        self.Vx = vx.values.tolist()[0]
        self.Vy = vy.values.tolist()[0]  
        self.N  = int(data[0])
        self.T  = float(data[1])
        self.Δt = float(data[2])
        self.Bz = float(data[3])
        
        
    def E(self):
        
        Ex, Ey = [0]* self.N, [0]* self.N 
        
        for i in range(0, self.N):
            for j in range(0, self.N):
                if (i != j):
                    
                    r3 = ( (self.x[i] - self.x[j])**2 + (self.y[i] - self.y[j])**2 )**1.5
                    
                    Ex[i] += self.Q[j]* (self.x[i] - self.x[j])/ r3
                    Ey[i] += self.Q[j]* (self.y[i] - self.y[j])/ r3
        
        return Ex, Ey
    
    
    def Boris(self):
        
        ListOfx  = open(r'Data/x.txt', 'w')
        ListOfy  = open(r'Data/y.txt', 'w')
        
        
        # Step - 1 : Half step velocity
        Ex, Ey = self.E()
        
        for i in range(0, self.N):
            self.Vx[i] += ( (self.Q[i]/self.M[i])* (Ex[i] + self.Bz* self.Vy[i]) )* (self.Δt/2)
            self.Vy[i] += ( (self.Q[i]/self.M[i])* (Ey[i] - self.Bz* self.Vx[i]) )* (self.Δt/2)
        
        
        # Step - 2 : Boris Algorithm
        t  = 0
        qd = [0]* self.N
        for i in range(0, self.N):
            qd[i] = (self.Q[i]* self.Δt)/ (2* self.M[i])
        
        
        while (t <= self.T):
            
            for i in range(0, self.N):
                
                hz  = qd[i]* self.Bz
                Sz  = 2* hz/ (1 + hz**2)
                
                Ux  = self.Vx[i] + qd[i]* Ex[i]
                Uy  = self.Vy[i] + qd[i]* Ey[i]
                
                Ux_d = Ux + Sz* (Uy - hz* Ux)
                Uy_d = Uy - Sz* (Ux + Uy* hz)
                
                self.Vx[i] = Ux_d + qd[i]* Ex[i]
                self.Vy[i] = Uy_d + qd[i]* Ey[i]
                
                self.x[i] += self.Vx[i]* self.Δt
                self.y[i] += self.Vy[i]* self.Δt
                
            Ex, Ey = self.E()
            
            np.savetxt(ListOfx, np.array([self.x]) )
            np.savetxt(ListOfy, np.array([self.y]) )
            
            t += self.Δt        
        
        ListOfx.close()
        ListOfy.close()


#%%

if __name__ == '__main__':
    
    Answer = Solver()
    Answer.Boris()
