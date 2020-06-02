#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#%%

class AnimateData:
    
    def __init__(self, x, y):
        
        self.x = x
        self.y = y

        self.x_Frame, self.y_Frame = [], []
        
        self.fig, self.ax = plt.subplots()
        self.ln, = plt.plot([], [], linewidth = 2)
    
    def PlotSettings(self):
        
        self.ax.set_title('Sine wave', fontsize = 20, fontweight = 'bold')
        
        self.ax.set_xlabel('x', fontsize = 16, fontweight = 'bold')
        self.ax.set_ylabel('y', fontsize = 16, fontweight = 'bold')
        
        self.ax.set_xlim(0, 2*np.pi)
        self.ax.set_ylim(-2, 2)
        
        return self.ln,
    
    def NewFrame(self, frame):
        
        self.x_Frame.append( self.x[frame] )
        self.y_Frame.append( self.y[frame] )
        
        self.ln.set_data(self.x_Frame, self.y_Frame)
        
        return self.ln,

    def RunTheCode(self):
        
        Animation = FuncAnimation(self.fig, self.NewFrame, frames = range(0, len(self.x)),
                                  init_func = self.PlotSettings, blit = True)
        
        Animation.save('SineWave.mp4', writer = 'ffmpeg', fps = 20)
        plt.show()

#%%

if __name__ == '__main__':
    
    x = np.linspace(0, 2*np.pi, 200)
    y = np.sin(x)
    
    DoMyWork = AnimateData(x, y)
    DoMyWork.RunTheCode()
