#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% Lagrange Polynomial

def Lrng_ply(x, xD, yD):
    
    
    # Summation loop
    L = 0
    for i in range(0, len(xD)):
        
        # Multiplication loop
        l = 1
        for j in range(0, len(xD)):
            
            # Take care about '1/0'
            if (xD[i] != xD[j]):
                l = l* (x - xD[j])/ (xD[i] - xD[j])
        
        L = L + l* yD[i]
        
    return L

#%% Example
    
# data set
x_Data = [1, 2, 4]
y_Data = [1, 4, 16]

# Point of interest
x = 3

L = Lrng_ply(x, x_Data, y_Data)
