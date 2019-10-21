#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import numpy library
import numpy as np

# Parametres
r   = 1
tht = np.linspace(0, 10* np.pi, 1000)

# Parametric equations in cartesian co-ordinates
x = r* np.cos(tht)
y = r* np.sin(tht)
z = np.exp(-tht)

# Import plotting libraries
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as Axes3D

# Adjustment for figure
fig = plt.figure('Parametric curves')
ax  = fig.add_subplot(111, projection='3d')

# Plot the data
ax.plot(x, y, z, '-r', linewidth = 3)

# Add labels
ax.set_xlabel('X', fontweight = 'bold', fontsize = 14)
ax.set_ylabel('Y', fontweight = 'bold', fontsize = 14)
ax.set_zlabel('Z', fontweight = 'bold', fontsize = 14)

# Add title
plt.title('Parametric Curve', fontweight = 'bold', fontsize = 16)

# Finally show the figure
plt.show()
