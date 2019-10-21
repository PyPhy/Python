#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import numpy library
import numpy as np

# Parametres
Ro  = 2
r   = 1
tht = np.linspace(0, 2* np.pi, 50)
phi = np.linspace(0, 2* np.pi, 50)

# Meshgrid to create mesh
tht, phi = np.meshgrid(tht, phi)

# Parametric equations in cartesian co-ordinates
x = (Ro + r* np.cos(tht))* np.cos(phi)
y = (Ro + r* np.cos(tht))* np.sin(phi)
z = r* np.exp(-tht)

# Import plotting libraries
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as Axes3D

# Adjustment for figure
fig = plt.figure('Parametric Surfaces')
ax  = fig.add_subplot(111, projection='3d')

# Plot the data
h = ax.plot_surface(x, y, z, cmap = 'jet', edgecolor = 'k')

# Colorbar for easy visualization
fig.colorbar(h)

# Add labels
ax.set_xlabel('X', fontweight = 'bold', fontsize = 14)
ax.set_ylabel('Y', fontweight = 'bold', fontsize = 14)
ax.set_zlabel('Z', fontweight = 'bold', fontsize = 14)

# Add title
ax.set_title('Parametric Surface', fontweight = 'bold', fontsize = 16)

# Adjust figure axes
ax.axis('square')

# Finally show the figure
plt.show()
