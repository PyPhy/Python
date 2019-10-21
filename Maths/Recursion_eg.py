#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import math
from functools import lru_cache

#%% Numerical differentiation
# To get the accurate answer dicrease the value of h ( h tends to 0)
#x = 1
#h = 1E-7
#F = lambda X: X**2
#d_F = (F(x+h) - F(x))/h

#%% Legendre polynomials
@lru_cache(maxsize = 500)
def legendre(x, l):
    # check that input is integer
    if type(l) != int:
        raise TypeError('l must be int')
    
    # compute the legendre polynomial
    if l == 0:
        return 1
    elif l == 1:
        return x
    elif l > 0:
        return ( (1/l)* ( (2*l-1)* x* legendre(x, l-1) - (l-1)* legendre(x, l-2) ) )
    
#%% Associated Legendre polynomials
@lru_cache(maxsize = 500)   
def asso_legendre(x, l, m):
    # check that input is integer
    if type(l) != int:
        raise TypeError('l must be int')
    if type(m) != int:
        raise TypeError('m must be int')
    
    # compute the Associated legendre polynomial
    if m == 0:
        return legendre(x, l)
    elif m > 0:
        return ( (1/np.sqrt(1-x**2))* ( (l-m+2)* asso_legendre(x, l+1, m-1) - (l+m)* x* asso_legendre(x, l, m-1) ) )
    elif m < 0:
        return ( ((-1)**(abs(m)))* ( math.factorial(l - abs(m))/ math.factorial(l + abs(m)))* asso_legendre(x, l, abs(m)) )

#%% Hermite polynomials

@lru_cache(maxsize = 500)
def Hermite(x, n):
    # check that input is integer
    if type(n) != int:
        raise TypeError('n must be positive int')
    if n < 0:
        raise ValueError('n must be positive int')
    
    # compute the Hermite polynomial
    if n == 0:
        return 1
    elif n == 1:
        return ( 2* x)
    else:
        return ( 2* x* Hermite(x, n-1) - 2* (n-1)* Hermite(x, n-2) )
    
#%% fibonacci numbers
        
fibonacci_cache = {}

def fibonacci(n):
    # If we have the value, the return it
    if n in fibonacci_cache:
        return fibonacci_cache[n]
    
    # Compute the Nth term
    if n == 1:
        value = 1
    elif n == 2:
        value = 1
    elif n > 2:
        value = fibonacci(n-1) + fibonacci(n-2)
        
    # Cache ththe value and return it
    fibonacci_cache[n] = value
    return value

print(fibonacci(10))

