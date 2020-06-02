#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#%%

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
    
    x_Frame.append(frame)
    y_Frame.append(np.sin(frame))
    
    ln.set_data(x_Frame, y_Frame)
    
    return ln,

ani = FuncAnimation(fig, NewFrame, frames=np.linspace(0, 2*np.pi, 140),
                    init_func = PlotSettings, blit=True)

ani.save('SineWave.mp4', writer = 'ffmpeg', fps = 20)
plt.show()
