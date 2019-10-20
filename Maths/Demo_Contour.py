#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

x = np.arange(0, 10 + 0.2, 0.2)
y = np.arange(0, 10 + 0.2, 0.2)

X, Y = np.meshgrid(x, y)
z = np.sin(X) * np.cos(Y)

plt.figure(1)
cs = plt.contour(X, Y, z, cmap=cm.jet)
plt.clabel(cs, inline=1, fontsize=10)
plt.xlabel('x', fontsize = 20, fontweight = 'bold')
plt.ylabel('y', fontsize = 20,fontweight = 'bold')

fig = plt.figure(2)
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, z, cmap=cm.jet, linewidth=0.5, edgecolors='k')
ax.set_xlabel('X', fontsize = 12, fontweight = 'bold')
ax.set_ylabel('Y', fontsize = 12, fontweight = 'bold')
ax.set_zlabel('Z', fontsize = 12, fontweight = 'bold')
