#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numba import jit
import random
import time

@jit(nopython=True)
def monte_carlo_pi(nsamples):
    
    acc = 0
    
    for i in range(nsamples):
        
        x = random.random()
        y = random.random()
        
        if (x ** 2 + y ** 2) < 1.0:
            acc += 1
    
    return 4.0 * acc / nsamples

if __name__ == '__main__':
    
    t = time.time()
    
    print(monte_carlo_pi(100000000))
    
    print('Numba took ' + str(time.time() - t))