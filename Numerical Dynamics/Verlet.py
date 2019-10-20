#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import cos, array

#%% Constants

k  = 1     # Spring constant
m  = 1     # Mass
dt = 0.2   # Accuracy
tm = 10    # Simulation time

#%% Initial conditions

x = [1]    # initial position
v = [0]    # initial velocity

# Time
t = [0]

#%% Verlet algorithm

i = 0

while t[-1] <= tm:
    
    # Acceleration
    a = -(k/m)* x[i]
    
    if i == 0:
        
        # Euler Cromer method
        
        # Velocity
        v_next = v[i] + a* dt
        
        # Position
        x_next = x[i] + v_next* dt
        
    else:
        
        # Position
        x_next = 2* x[i] - x[i-1] + a* dt**2
        
    # Position update
    x.append(x_next)
    
    # Time update
    t.append(t[i] + dt)
        
    # Loop update
    i = i + 1
    
#%% Analytical solution
    
omg = (k/ m)**0.5
xa  = x[0]* cos(omg* array(t))

#%% Plot
import matplotlib.pyplot as plt

plt.plot(t, xa, label = 'Analytical')
plt.plot(t, x, 'ro', label = 'Verlet')
plt.title('Verlet', fontweight = 'bold', fontsize = 16)
plt.xlabel('t', fontweight = 'bold', fontsize = 14)
plt.ylabel('X', fontweight = 'bold', fontsize = 14)
plt.grid(True)
plt.legend()
plt.show()
