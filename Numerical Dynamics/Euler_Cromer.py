#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% constants

k = 1       # Spring constant
m = 1       # mass
dt = 0.5    # accuracy
t_max = 10   # simulation time

#%% Initial condition
x = [1]     # initial position
t = [0]     # initial time
v = [0]     # initial velocity

# intial conditions for euler cromer methond
x_euler = x[0]
t_euler = t[0]
v_euler = v[0]
dt_euler = dt/1000

i = 0

while t[-1] <= t_max:
    
    # acceleration
    a = -(k/m)* x[i]
    
    v_next = v[i] + a* dt
    x_next = x[i] + v_next* dt

    # Position update
    x.append(x_next)
    
    # Velocity update
    v.append(v_next)
    
    # Time update
    t.append(t[i] + dt)
        
    # Loop update
    i = i + 1
    
    
x_euler = x
v_euler = v
t_euler = t    
    
#%%
import numpy as np
t = np.linspace(0,t_max,1000)
x = np.cos(t)
v = - np.sin(t)

import matplotlib.pyplot as plt

plt.figure('Position (Euler)')
ax = plt.gca()

plt.plot(t_euler, x_euler, 'ro', label='Euler')
plt.plot(t, x, label='Real')
plt.legend()
plt.xlabel('t', fontweight='bold')
plt.ylabel('x', fontweight='bold')
plt.grid(True)
plt.show()
