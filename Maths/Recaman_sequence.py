#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def recaman(n):
    
    seq = [0]
    for i in range(1, n):
        
        x = seq[i-1] - i
        
        if (x >= 0 and x not in seq): 
            seq += [x]
        else: 
            seq += [seq[i-1] + i]

    return seq

print(recaman(20))

