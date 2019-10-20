#!/usr/bin/env python3

import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot( 111 , projection='3d')

x = np.linspace(0, np.pi, 20)
y = np.linspace(0, np.pi, 20)

X, Y = np.meshgrid(x, y)
Z = np.sin(X * Y)

ax.plot_surface(X, Y, Z, color = (0.1, 0.5, 1), edgecolors='k' )
