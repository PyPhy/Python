#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import tan

#%% Function

def f(t, y):
    
    return tan(y) + 1

#%% Runge-Kutta method

def RK(h, to, yo):
    
    K1 = h* f(to, yo)
    K2 = h* f(to + h/2, yo + K1/2)
    K3 = h* f(to + h/2, yo + K2/2)
    K4 = h* f(to + h, yo + K3)
    
    t1 = to + h
    y1 = yo + (K1 + 2*K2 + 2*K3 + K4)/ 6
    
    return t1, y1

#%% Initialization
    
t = [1]     # intial value of t
y = [1]     # intial value of y
h = 0.025   # accuracy

# Maximum value of t
t_max = 1.1

#%% Loop in action

while (t[-1] < t_max):
    
    t_next, y_next = RK(h, t[-1], y[-1])
    
    t.append(t_next)
    y.append(y_next)
