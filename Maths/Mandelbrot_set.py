#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

#%% Mandelbrot function

def mandelbrot(a):
    
	z = 0
	for n in range(1, 100):
        
		z = z**2 + a
        
		if abs(z) > 2:
			return n
    
	return np.NaN

#%%
X = np.arange(-2, 0.5, 0.002)
Y = np.arange(-1.2,  1.2, 0.002)
Z = np.zeros( [len(X), len(Y)] )
 
for i in tqdm(range(0, len(X))):
    
    #print(str(i) + ' of ' + str(len(X)))
    
    for j in range(0, len(Y)): 
	    Z[i,j] = mandelbrot(X[i] + 1j * Y[j])
 
#%% Plot

plt.imshow(Z, cmap = plt.cm.prism, interpolation = 'none')#, extent = (Y.min(), Y.max(), X.min(), X.max()))

plt.title('Mandelbrot Set', fontweight='bold', fontsize=14)
plt.axis('off')
plt.savefig('Mandelbrot Set', dpi=500)
plt.show()
