#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def gamit_number(N):
    
    if (len( list( str(N) ) ) == 4):
    
        square = N**2
        
        square = list( str(square) )
        
        New_N = int(square[0] + square[1]) + int(square[2] + square[3])
        
        test = True if (New_N == N) else False
        
    else:
        
        test = 'This is beyond the scope of this code'
    
    return test
        
#%%

import numpy as np

List = np.linspace(32, 99, 99 - 32 + 1)

Gamit_Numbers = []

for i in List:
    
    Test = gamit_number(i)
    
    if (Test == True):
        Gamit_Numbers.append(i)
