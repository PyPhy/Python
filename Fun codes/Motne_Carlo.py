#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

#%% Initialization

# Maximum iteration
Max_It = 100000

# Record of points which are outside the circle
Out_x = []
Out_y = []

# Record of points which are inside the circle
In_x = []
In_y = []

#%% Monte Carlo loop

i = 0
while (i <= Max_It):
    
    # Random numbers between -0.5 and 0.5
    x = random.uniform(0, 1) - 0.5
    y = random.uniform(0, 1) - 0.5
    
    # distance from the origin
    d = (x**2 + y**2)**0.5
    
    if d > 0.5:
        Out_x.append(x)
        Out_y.append(y)
    
    elif d < 0.5:
        In_x.append(x)
        In_y.append(y)
    
    # Loop update
    i = i + 1

#%% Pi
    
Pi = 4* len(In_x)/ ( len(In_x) + len(Out_x) )

print('With ' + str(Max_It) + ' Iterations, the value of Pi is ' + str(Pi))

#%% Plot

import matplotlib.pyplot as plt
fig, ax = plt.subplots()

# Points
In     = (In_x,  In_y)
Out    = (Out_x, Out_y)
data   = (In, Out)
colors = ('r', 'b')

for data, color in zip(data, colors):
    x, y = data
    ax.scatter(x, y, c = color, edgecolors = 'none', alpha = 0.5)

# Square
plt.plot([-0.5,-0.5,0.5,0.5,-0.5], [-0.5,0.5,0.5,-0.5,-0.5], linewidth = 3)

# Circle
cir = plt.Circle((0, 0), 0.5, fill = False, linewidth = 3, edgecolor = 'b')
ax.add_artist(cir)

plt.title('Monte Carlo', fontweight = 'bold', fontsize = 16)
plt.xlabel('X', fontweight = 'bold', fontsize = 14)
plt.ylabel('Y', fontweight = 'bold', fontsize = 14)
plt.axis('square')
plt.show()
