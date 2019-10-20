#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import factorial

#%% Associated Laguerre Polynomial
    
def Asso_Laguerre(n, k, x):
    
    L = 0
    for m in range(0, n):
        L = L + (-1)**m * (factorial(n+k)/( factorial(n-m)* factorial(k+m)* factorial(m)) )* x**m

    return L

#%% Example
    
L = Asso_Laguerre(3, 0, 0.5)
