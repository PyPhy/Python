#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

# Function
def y(x):
    
    ''' Change the expression 
        eg. np.sin(x), x**3, x '''
    
    return (x + 1/x)

# Simpson's 1/3 rule
def Simpson_1_3(xi, xf, h):
    
    ''' xi is the lower limit of intigration
        xf is the upper limit of intigration
        h is small step size '''
    
    n = int( (xf - xi)/ h )
    
    X = np.linspace(xi, xf, n+1)
    Y = y(X)
    
    # Exclude 1st and last element, jump to 2nd data
    Y1 = np.sum( Y[1: len(Y) - 1 :2] )
    
    # Exclude 2nd and last element, jump to 2nd data
    Y2 = np.sum( Y[2: len(Y) - 1 :2] )
    
    S = (h/3)* ( Y[0] + Y[-1] + 4*Y1 + 2*Y2 )
    
    return S

# Example
print( Simpson_1_3(1.2,1.6,0.1) )
