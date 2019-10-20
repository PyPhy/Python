#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import sin, cos, linspace

#%% constants

dt = 0.5    # Accuracy
tm = 10     # Simulation time

#%% Initial condition

x = [1]     # initial position
v = [0]     # initial velocity

t = [0]     # initial time

#%% Acceleration

def a(x):
    
    k = 1   # Spring constant
    m = 1   # mass
    
    A = -(k/m) * x
    
    return A

#%% Velocity Verlet
i = 0

while (t[-1] < tm):
    
    if (i == 0):
        
        v_half = v[i] + (1/2)* a(x[i]) * dt 
        
        x.append( x[i] + v_half* dt )
        
        v.append( v_half + (1/2)* a(x[i+1]) * dt )
        
    else:
        
        x.append( x[i] + v[i] * dt + (1/2)* a(x[i]) * dt**2 )
        
        v.append( v[i] + (1/2) * ( a(x[i]) + a(x[i+1]) )* dt )
    
    
    t.append(t[i] + dt)
    i = i + 1


x_verlet = x
v_verlet = v
t_verlet = t

#%%
import matplotlib.pyplot as plt

t = linspace(0, tm,1000)
x = cos(t)
v =-sin(t)

plt.figure('Position (verlet)')
ax = plt.gca()

plt.plot(t_verlet, x_verlet, 'ro', label='Verlet')
plt.plot(t, x, label='Real')
plt.legend()
plt.xlabel('t', fontweight='bold')
plt.ylabel('x', fontweight='bold')
plt.grid(True)
plt.show()


plt.figure('velocity')
ax = plt.gca()

plt.plot(t_verlet, v_verlet, 'ro', label='Verlet')
plt.plot(t, v, label='Real')
plt.legend()
plt.xlabel('t', fontweight='bold')
plt.ylabel('v', fontweight='bold')
plt.grid(True)
plt.show()
