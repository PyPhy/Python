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
    
    try:
        if m == 0:
            P = Legendre_Poly(l, x)
            
        elif m > 0:
            P = (1/ sqrt(1 - x**2))* ((l-m+1)* x* Asso_Leg(l, m-1, x) \
                                    - (l+m-1)* Asso_Leg(l-1, m-1, x) )
                                
        elif m < 0:
            m = abs(m)
            P = ((-1)**m) * (factorial(l - m)/ factorial(l + m))* Asso_Leg(l, m, x)
            
    except ZeroDivisionError:
        P = 0
    
    return P

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

phi = linspace(0, 2* pi, 100)
tht = linspace(0, pi, 100)

Phi, Tht = meshgrid(phi, tht)

#%% Value of Y

p, q = shape(Phi)
Y    = zeros([p, q])

for i in range(0 + 1, p - 1):
    for j in range(0 + 1, q - 1):

        if m > 0:
        
            Y[i, j] = sqrt(2)* K* cos(m* Phi[i, j])* Asso_Leg(l, m, cos(Tht[i, j]))
        
        elif m < 0:
        
            Y[i, j] = sqrt(2)* K* sin(abs(m)* Phi[i, j])* Asso_Leg(l, abs(m), cos(Tht[i, j]))
        
        elif m == 0:
        
            Y[i, j] = K* Legendre_Poly(l, cos(Tht[i, j]))


#%% Take care about negative Y
p, q = shape(Y)

for i in range(0, p):
    for j in range(0, q):

        if Y[i, j] < 0:
            Tht[i, j] = Tht[i, j] + pi

#%% Finally convert data to cartesian form

x, y, z = Shperical2Cartesian(Y, Tht, Phi)

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
