#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% Hermite Polynomial

def Hermite(n, x):
    ''' n is the order
        x is the point interest'''
    
    if n == 0:
        H = 1
    
    elif n == 1:
        H = 2* x
    
    else:
        H = 2* x* Hermite(n-1, x) - 2* (n-1)* Hermite(n-2, x)
    
    return H

#%% Example
    
H = Hermite(2, 0.5)
