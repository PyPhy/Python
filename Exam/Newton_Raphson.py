#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sympy import Symbol, lambdify
x  = Symbol('x')

#%% Function

f  = 2* x**3 - 2.5* x - 5
df = f.diff(x)

f  = lambdify(x, f,  'numpy')
df = lambdify(x, df, 'numpy')

#%% Constant

n = 9      # iterations
x = 2      # initial guess

#%% Newton Raphson loop

i = 1
while (i <= n):
    
    x = x - f(x)/ df(x)
    
    i = i + 1
