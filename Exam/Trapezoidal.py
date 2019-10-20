#!/usr/bin/env python3

import numpy as np

# Function
def y(x):
    ''' Change the expression 
        eg. np.sin(x), x**3, x '''
    return x**2

# Trapezoidal Integrator
def Trapezoidal(xi, xf, h):
    
    ''' xi is the lower limit of intigration
        xf is the upper limit of intigration
        h is small step size '''
    
    n = int( (xf - xi)/ h )
    
    X = np.linspace(xi, xf, n+1)
    Y = y(X)
    
    T = h* ( np.sum(Y) - (Y[0] + Y[-1])/2)
    
    return T

# Example
print( Trapezoidal(0, 1, 0.001) )
