#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

r = np.arange(0.05E-9, 0.35E-9 + 0.005E-9, 0.005E-9)
re = 0.1274E-9
x = r - re

# Harmonic potential
k = 516
V = 0.5* k* x**2

# Morese Potential
De = 7.09764E-19
beta = np.sqrt(k/(2* De))

Vm = De* ( 1 - np.exp(-beta* x) )**2

#%% Plotting
plt.figure(1)
plt.plot(r, V, linewidth = 3.0, color = 'g', label='Harmonic potential') 
plt.plot(r, Vm,linewidth = 3.0, color = 'r', label='Morse potential' )
plt.xlabel('Internuclear distance', fontsize = 10)
plt.ylabel('$V(r)$ in $(J)$', fontsize = 10)
plt.legend()
plt.grid(True)
plt.show()

#%%

output_data = pd.DataFrame({"x" : ( x  ),
                            "V" : ( V  ),
                            "Vm": ( Vm )}, columns=['x','V','Vm'] )

output_data.to_excel('Potential.xlsx',index= False)

