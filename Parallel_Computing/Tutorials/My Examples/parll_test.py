#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import linspace

def wave(loop):
    
    sq = []
    for n in loop:
        sq.append(n**2)
        
    return sq
    
if __name__ == '__main__':
    
    from multiprocessing import Pool, cpu_count
    import time
    
    t = time.time()
    
    y = linspace(0, 10, 1000000)

    p = Pool( processes = cpu_count() )
    result = p.map(wave, [y])
    
    p.close()
    p.join()
    
    print('Process completed in ' + str(time.time() - t))
