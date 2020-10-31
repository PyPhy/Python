#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from numpy.random import normal
import pandas as pd

#%%

class MakeDataFiles:
    
    def __init__(self):
        
        # Example - 1 : Positive charge in magnetic field
        # self.x,  self.y,  self.z  = [0], [0], [0]
        # self.Vx, self.Vy, self.Vz = [1], [0], [0]
        # self.M,  self.Q           = [1], [1]
        
        # Example - 2 : Negative charge in magnetic field
        # self.x,  self.y,  self.z  = [0], [0], [0]
        # self.Vx, self.Vy, self.Vz = [1], [0], [0]
        # self.M,  self.Q           = [1], [-1]
        
        # Example - 3 : Positive charge with Vx and Vz
        # self.x,  self.y,  self.z  = [0], [0], [0]
        # self.Vx, self.Vy, self.Vz = [2], [0], [0.5]
        # self.M,  self.Q           = [1], [-1]
        
        # Example - 4 : E X B drift
        # self.x,  self.y,  self.z  = [0], [0], [0]
        # self.Vx, self.Vy, self.Vz = [1], [1], [0]
        # self.M,  self.Q           = [1], [1]
        
        # Example - 5 : Grad - B Drift  (Nonuniform B field)
        # self.x,  self.y,  self.z  = [0], [0], [-4]
        # self.Vx, self.Vy, self.Vz = [1], [0], [1]
        # self.M,  self.Q           = [1], [1]
        
        # Example - 6 : Curvature Drift (Nonuniform B field)
        # self.x,  self.y,  self.z  = [3], [0], [0]
        # self.Vx, self.Vy, self.Vz = [1], [1], [0]
        # self.M,  self.Q           = [1], [1]
        
        # Example - 7 : Magnetic Mirror (Nonuniform B field)
        # self.x,  self.y,  self.z  = [0], [0], [0]
        # self.Vx, self.Vy, self.Vz = [1], [1], [0]
        # self.M,  self.Q           = [1], [1]
        
        # Example - 8 : Nonuniform E field
        self.x,  self.y,  self.z  = [0], [0], [0]
        self.Vx, self.Vy, self.Vz = [1], [0], [0]
        self.M,  self.Q           = [1], [1]


    def WriteDataFiles(self):
        
        M_data  = open(r'Data/M.txt', 'w')
        Q_data  = open(r'Data/Q.txt', 'w')
        x_data  = open(r'Data/x.txt', 'w')
        y_data  = open(r'Data/y.txt', 'w')
        z_data  = open(r'Data/z.txt', 'w')
        vx_data = open(r'Data/vx.txt','w')
        vy_data = open(r'Data/vy.txt','w')
        vz_data = open(r'Data/vz.txt','w')
        
        np.savetxt(M_data,  np.array([self.M])  )
        np.savetxt(Q_data,  np.array([self.Q])  )
        np.savetxt(x_data,  np.array([self.x])  )
        np.savetxt(y_data,  np.array([self.y])  )
        np.savetxt(z_data,  np.array([self.z])  )
        np.savetxt(vx_data, np.array([self.Vx]) )
        np.savetxt(vy_data, np.array([self.Vy]) )
        np.savetxt(vz_data, np.array([self.Vz]) )
        
        M_data.close()
        Q_data.close()
        x_data.close()
        y_data.close()
        z_data.close()
        vx_data.close()
        vy_data.close()
        vz_data.close()
        

#%%

if __name__ == '__main__':
    
    DoMyWork = MakeDataFiles()
    DoMyWork.WriteDataFiles()
