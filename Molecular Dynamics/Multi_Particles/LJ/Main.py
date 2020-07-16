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
        x    = pd.read_csv(r'Data/x.txt', header = None, sep = ' ')
        y    = pd.read_csv(r'Data/y.txt', header = None, sep = ' ')
        vx   = pd.read_csv(r'Data/vx.txt', header = None, sep = ' ')
        vy   = pd.read_csv(r'Data/vy.txt', header = None, sep = ' ')
        data = pd.read_csv('Inputs.txt', header = None, sep = '=')
        data = data[1].tolist()
        
        self.M  =  M.values.tolist()[0]
        self.x  =  x.values.tolist()[0]
        self.y  =  y.values.tolist()[0]
        self.vx = vx.values.tolist()[0]
        self.vy = vy.values.tolist()[0]  
        self.N  = int(data[0])
        self.T  = float(data[1])
        self.Δt = float(data[2])
        self.rm = float(data[3])
        self.ep = float(data[4])
        
        
    def Acc(self):
        
        Ax, Ay = [0]* self.N, [0]* self.N 
        
        for i in range(0, self.N):
            for j in range(0, self.N):
                if (i != j):
                    
                    r = ( (self.x[i] - self.x[j])**2 + (self.y[i] - self.y[j])**2 )**0.5
                    C = (12* self.ep/ self.rm**2)* ( (self.rm/ r)**14 - (self.rm/ r)**8 )/ self.M[i]
                    
                    Ax[i] += C* (self.x[i] - self.x[j])
                    Ay[i] += C* (self.y[i] - self.y[j])
        
        return Ax, Ay
    
    
    def Beeman(self):
        
        ListOfx  = open(r'Data/x.txt', 'w')
        ListOfy  = open(r'Data/y.txt', 'w')
        ListOfvx = open(r'Data/vx.txt', 'w')
        ListOfvy = open(r'Data/vy.txt', 'w')
        ListOft  = open(r'Data/t.txt', 'w')
        
        t = 0
        
        # Step - 1 : Initialization for Beeman
        aox, aoy = self.Acc()
        
        for i in range(0, self.N):
            
            self.vx[i] += aox[i]* self.Δt
            self.vy[i] += aoy[i]* self.Δt
            
            self.x[i] += self.vx[i]* self.Δt
            self.y[i] += self.vy[i]* self.Δt
        
        t += self.Δt
        
        a1x, a1y = self.Acc()
        
        np.savetxt(ListOfx,  np.array([self.x])  )
        np.savetxt(ListOfy,  np.array([self.y])  )
        np.savetxt(ListOfvx, np.array([self.vx]) )
        np.savetxt(ListOfvy, np.array([self.vy]) )
        
        
        # Step - 2 : Beeman Algorithm
        while (t <= self.T):
            
            for i in range(0, self.N):
                self.x[i] += self.vx[i]* self.Δt + (4* a1x[i] - aox[i])* self.Δt**2/ 6
                self.y[i] += self.vy[i]* self.Δt + (4* a1y[i] - aoy[i])* self.Δt**2/ 6
            
            a2x, a2y = self.Acc()
            
            for i in range(0, self.N):
                self.vx[i] += (5* a2x[i] + 8* a1x[i] - aox[i])* self.Δt/ 12
                self.vy[i] += (5* a2y[i] + 8* a1y[i] - aoy[i])* self.Δt/ 12
            
            np.savetxt(ListOfx,  np.array([self.x])  )
            np.savetxt(ListOfy,  np.array([self.y])  )
            np.savetxt(ListOfvx, np.array([self.vx]) )
            np.savetxt(ListOfvy, np.array([self.vy]) )
            
            aox, aoy = a1x, a1y
            a1x, a1y = a2x, a2y
            t += self.Δt
        
        
        ListOfx.close()
        ListOfy.close()
        ListOfvx.close()
        ListOfvy.close()


#%%

if __name__ == '__main__':
    
    Answer = Solver()
    Answer.Beeman()
