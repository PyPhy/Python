#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% Legendre Polynomials

def Legendre_Poly(n, x):

    if n == 0:
        P = 1
        
    elif n == 1:
        P = x
        
    else:
        P = (1/n)* ((2*n - 1)* x* Legendre_Poly(n-1, x) - (n - 1)* Legendre_Poly(n-2, x))

    return P

#%% Example
    
P = Legendre_Poly(5, 0)
