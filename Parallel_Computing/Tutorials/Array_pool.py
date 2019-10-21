#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import time

def lazy_func(A):
    
    for i in range(0, len(A)):
        time.sleep(1)
        print(A)
    

if __name__ == '__main__':
    
    import multiprocessing as mp
    
    A = np.array([ np.linspace(0, 1, 6),
                   10* np.linspace(0, 1, 6),
                   100* np.linspace(0, 1, 6) ])
    
    t = time.time()
    
    pool = mp.Pool( processes = mp.cpu_count() )
    
    pool.map(lazy_func, [A[0]] )
    
    pool.close()
    pool.join()
    
    print(time.time() - t)
    
