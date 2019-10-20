#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import factorial
from numpy import sqrt

#%% Legendre Polynomials

def Legendre_Poly(n, x):

    if n == 0:
        P = 1
        
    elif n == 1:
        P = x
        
    else:
        P = (1/n)* ((2*n - 1)* x* Legendre_Poly(n-1, x) - (n - 1)* Legendre_Poly(n-2, x))

    return P

#%% Associated Legendre Polynomials

def Asso_Leg(l, m, x):
    
    if m == 0:
        P = Legendre_Poly(l, x)
        
    elif m > 0:
        P = (1/ sqrt(1 - x**2))* ((l-m+1)* x* Asso_Leg(l, m-1, x) \
                                - (l+m-1)* Asso_Leg(l-1, m-1, x) )
                            
    elif m < 0:
        m = abs(m)
        P = ((-1)**m) * (factorial(l - m)/ factorial(l + m))* Asso_Leg(l, m, x)

    return P

#%% Example
    
P = Asso_Leg(3, 2, 0.5)
