import pandas as pd
import numpy as np

Input = pd.read_csv("input.txt", sep = "=", header = None)
Input.drop( Input.columns[0], axis = 1, inplace = True)
Input = np.array(Input)

Lx = Input[0][0]
Ly = Input[1][0]
Nx = Input[2][0]
Ny = Input[3][0]

x = np.linspace(-Lx/2, Lx/2, Nx)
y = np.linspace(-Ly/2, Ly/2, Ny)
x, y = np.meshgrid(x, y)

import matplotlib.pyplot as plt

Data = pd.read_csv("DataZ.csv", header = None)
Data.drop( Data.columns[len(Data.columns)-1], axis=1, inplace=True)
Data = np.array(Data)

plt.contourf(x, y, Data, 100, cmap = 'jet')
plt.axis('square')
plt.colorbar()
plt.show()

