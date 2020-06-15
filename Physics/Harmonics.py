#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import sin, cos, pi, sqrt, shape, linspace, meshgrid, zeros
from math import factorial

def Shperical2Cartesian(r, theta, phi):

    x = r* sin(theta)* cos(phi)
    y = r* sin(theta)* sin(phi)
    z = r* cos(theta)
    
    return x, y, z

#%% Legendre Polynomials

def legendre_polynomial(l, m, x):
    pmm = 1.0
    if m > 0:
        sign = 1.0 if m % 2 == 0 else -1.0
        pmm = sign * pow( factorial(2 * m - 1) * (1.0 - x * x), ((m / 2)) )

    if l == m:
        return pmm

    pmm1 = x * (2 * m + 1) * pmm
    if l == m + 1:
        return pmm1

    for n in range(m + 2, l + 1):
        pmn = (x * (2 * n - 1) * pmm1 - (n + m - 1) * pmm) / (n - m)
        pmm = pmm1
        pmm1 = pmn

    return pmm1

#%% Main code
    
''' Now all functions are defined
    So we are ready to use it '''
    
#%% Azimuthal and Magnetic quantum nubers

l = int(input('Azimuthal quantum number "l": '))

if l < 0:
    print('"l" can not be a negative number')

m = int(input('Magnetic quantum number "m": '))

if m > l or m < (-l):
    print('quntum number "m" belong to "[-l,l]"')

#%%  Normalization constant

K = sqrt( ((2*l + 1)* factorial(l - abs(m)))/ (4* pi* factorial(l + abs(m))) )

#%% Value of Phi and Theta

phi = linspace(0, 2* pi, 181)
tht = linspace(0, pi, 91)

Phi, Tht = meshgrid(phi, tht)

#%% Value of Y

p, q = shape(Phi)
Y    = zeros([p, q])

for i in range(0, p):
    for j in range(0, q):

        if m > 0:
        
            Y[i, j] = sqrt(2) * K * cos(m * Phi[i, j]) * legendre_polynomial(l, m, cos(Tht[i, j]))
        
        elif m < 0:
        
            Y[i, j] = sqrt(2) * K * sin(abs(m) * Phi[i, j]) * legendre_polynomial(l, abs(m), cos(Tht[i, j]))
        
        else:
        
            Y[i, j] = K * legendre_polynomial(l, 0, cos(Tht[i, j]))


#%% Take care about negative Y
p, q = shape(Y)

#%% Finally convert data to cartesian form

x, y, z = Shperical2Cartesian(abs(Y), Tht, Phi)

#%% plotting

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as mp3d

fig = plt.figure('Harmonics')
ax = fig.add_subplot( 111 , projection='3d')

ax.plot_surface(x, y, z, cmap = 'jet', edgecolor = 'k')

plt.axis('square')
plt.title('Spherical Harmonics', fontsize = 14, fontweight = 'bold')
ax.set_xlabel('X', fontsize = 12, fontweight = 'bold')
ax.set_ylabel('Y', fontsize = 12, fontweight = 'bold')
ax.set_zlabel('Z', fontsize = 12, fontweight = 'bold')
plt.show()
