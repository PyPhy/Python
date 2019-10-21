#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import sqrt, arange, pi, exp, zeros
from math import factorial
from functools import lru_cache

#%% Hermite polynomials

@lru_cache(maxsize = 1000)
def Hermite( H_x, H_n):
    
    # input must be an integer
    if type(H_n) != int:
        raise TypeError('n must be positive integer')
    if H_n < 0:
        raise ValueError('n must be positive integer')
    
    # compute the the Hermite polynomial
    if H_n == 0:
        return 1
    elif H_n == 1:
        return (2* H_x)
    else:
        return (2* H_x* Hermite( H_x, H_n-1) - 2* (H_n-1)* Hermite( H_x, H_n-2) )


#%% Contants

# energy level
n = 11
# width
a = 2e-9

h = 6.62606896e-34
m = 9.10938215e-31

omg = (2*h/ (m* 2* pi* a**2))*(n + 0.5)
Nn  = sqrt( sqrt( (2* m* omg)/h ) * (1/ ( (2**n) * factorial(n)) ) )

#%% Main code

x = arange(-1.7*a, 1.7*a, a/100)
y = sqrt(2* pi* m* omg/ h)* x

phy  = zeros(len(x))
prob = zeros(len(x))

for i in range(0, len(x)):
    phy[i]  = Nn* exp(-(y[i]**2)/ 2)* Hermite(y[i], n)
    prob[i] = phy[i]**2

#%% Plotting

import matplotlib.pyplot as plt
    
plt.figure(1)
plt.plot(x, phy, color = "#ff7f0e", linewidth = 2.0)
plt.xlabel('$x$', fontsize = 20, fontweight = 'bold')
plt.ylabel('$\psi_n(x)$', fontsize = 20,fontweight = 'bold')
plt.title('Linear Harmonic Oscillator',fontsize = 20,fontweight = 'bold')
plt.grid(True)
plt.show()

plt.figure(2)
plt.plot(x, prob, color = "#ff7f0e", linewidth = 2.0)
plt.xlabel('$x$', fontsize = 20, fontweight = 'bold')
plt.ylabel('$|\psi_n(x)|^2$', fontsize = 20,fontweight = 'bold')
plt.title('Linear Harmonic Oscillator',fontsize = 20,fontweight = 'bold')
plt.grid(True)
plt.show()

plt.figure(3)
plt.scatter(x, [0]*len(x), c=prob, s = 50, cmap='jet')
plt.xlabel('spectrum', fontsize = 20,fontweight = 'bold')
plt.title('Linear Harmonic Oscillator',fontsize = 20,fontweight = 'bold')
plt.xlim(x[0], x[-1])
plt.colorbar()
plt.show()

