#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import pi, sin, append, linspace, array, arange
from numpy.random import rand, seed
from scipy.fftpack import fft
import matplotlib.pyplot as plt
from mpldatacursor import datacursor

#%% FFT

class FFT():
    
    def __init__(self, t, Signal):
        
        self.t = t
        self.f = Signal
        self.N = len(t)
        
    def Freq(self):
        
        freqs = arange(1, self.N, 1)[:int(self.N/2) - 1]
        Ampts = (2/self.N)* abs( fft(self.f)[:int(self.N/2)] )[1:]
        
        return freqs, Ampts

    def PlotFFT(self):
        
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(80, 60))
        
        # signal plot
        axs[0].plot(self.t, self.f)
        axs[0].grid()
        axs[0].set_xlabel('time (s)', fontsize = 16)
        axs[0].set_ylabel('Voltage', fontsize = 16)
        axs[0].set_title('Signal', fontweight = 'bold', fontsize = 20)
        
        # frequency
        freqs, Ampts = self.Freq()
        
        h = axs[1].plot(freqs, Ampts, 'r')
        datacursor(h)
        axs[1].grid()
        axs[1].set_xlabel('frequency (Hz)', fontsize = 16)
        axs[1].set_ylabel('Voltage', fontsize = 16)
        axs[1].set_title('FFT', fontweight = 'bold', fontsize = 20)
        
        plt.show()

#%%

if __name__ == '__main__':
    
    # time
    t = linspace(0, 1, 400)
    
    # Example - 1: Signal
    # f = sin(2* pi* 5* t) + 0.5* sin(2* pi* 10* t)
    
    # Example - 2: Square wave
    # f = array([])
    # for i in t:
    #     if i <= 0.5:
    #         f = append(f, 1)
    #     else:
    #         f = append(f, -1)
    
    # Example - 3: Signal with noise
    seed(1)
    f = sin(2* pi* 5* t) + 0.5* sin(2* pi* 10* t) + rand( len(t) )
    
    SignalFFT = FFT(t, f)
    SignalFFT.PlotFFT()
