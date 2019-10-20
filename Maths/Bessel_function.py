#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy.special as spl

x = np.linspace(-10, 10, 500)
y = []
v = [0, 1, 2, 3]
for i in range(0, len(v)):
    y.append( spl.jv(v[i], x))
    plt.plot(x, y[i], linewidth = 2.0,  label='v = %s' % i)
 
plt.legend()
plt.grid(True)
plt.show()
