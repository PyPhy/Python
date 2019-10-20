#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-2, 2, 99)
y1 = np.sqrt(1 - (np.abs(x) - 1)**2)
y2 = (-3) * np.sqrt(1 - np.sqrt(np.abs(x) / 2))

plt.figure()
ax = plt.gca()

plt.plot(x, y1, x, y2, color='r')
plt.xlabel('X', fontweight='bold')
plt.ylabel('Y', fontweight='bold')
plt.title('Heart curve', fontsize=18, fontweight='bold')
ax.set_xlim([-3, 3])
plt.grid(True)
plt.show()

