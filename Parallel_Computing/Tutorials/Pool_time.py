#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

def f(n):
    sum1 = 0
    sum2 = 0
    for x in range(1000):
        sum1 += x**2
        sum2 += x
    
    return [sum1, sum2]

if __name__ == '__main__':
    
    from multiprocessing import Pool
    t1 = time.time()
    
    if 2 > 1:
        Junk = 1 + 4
        Junk = [1,3,4]
        print('   Successfully received filament data from Input.py')
        
        print('   Calculating filaments...')
        
        p = Pool()
        
        result1 = p.map(f, range(100000))
        
        p.close()
        p.join()
        
        Junk = [1,3,4]
    
    print('Pool took:', time.time() - t1)
    
#    t2 = time.time()
#    result2 = []
#    for x in range(100000):
#        result2.append(f(x))
#        
#    print('Serial took:', time.time() - t2)
