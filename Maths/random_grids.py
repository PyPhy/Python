#!/usr/bin/env python3

import matplotlib.pyplot as plt
import random
import numpy as np

x1 = np.array([0, 1])
y1 = np.array([0, 1])

x2 = np.array([1, 0])
y2 = np.array([0, 1])

#%%
f = plt.gca()

for i in range(10):
    for j in range(10):

        rand = 100*random.random() 
        if (rand > 50.0):
            x1_1 = x1 + i
            y1_1 = y1 + j
            plt.plot(x1_1, y1_1, color = 'm')
        elif (rand <= 50.0):
            x2_1 = x2 + i
            y2_1 = y2 + j
            plt.plot(x2_1, y2_1, color = 'c')


f.set_xlim([0, 10])
f.set_ylim([0, 10])
plt.axis('equal')
plt.axis('off')
plt.show()

