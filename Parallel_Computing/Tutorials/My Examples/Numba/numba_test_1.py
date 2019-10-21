#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Numba_test_2 import monte_carlo_pi
import time

if __name__ == '__main__':
    
    t = time.time()
    
    print(monte_carlo_pi(100000000))
    
    print('Numba took ' + str(time.time() - t))
