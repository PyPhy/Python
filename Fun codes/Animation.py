#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#%% Data

x = np.linspace(0, 2*np.pi, 200)
y = np.sin(x)

#%% Animate

x_Frame, y_Frame = [], []

fig, ax = plt.subplots()
ln, = plt.plot([], [], linewidth = 2)

def PlotSettings():
    
    ax.set_title('Sine wave', fontsize = 20, fontweight = 'bold')
    
    ax.set_xlabel('x', fontsize = 16, fontweight = 'bold')
    ax.set_ylabel('y', fontsize = 16, fontweight = 'bold')
    
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    
    return ln,

def NewFrame(frame):
    
    x_Frame.append(x[frame])
    y_Frame.append(y[frame])
    
    ln.set_data(x_Frame, y_Frame)
    
    return ln,

ani = FuncAnimation(fig, NewFrame, frames = range(0, len(x)),
                    init_func = PlotSettings, blit=True)

ani.save('SineWave.mp4', writer = 'ffmpeg', fps = 20)
plt.show()
