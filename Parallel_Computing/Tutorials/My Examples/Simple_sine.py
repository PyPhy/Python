#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import sin, linspace


if __name__ == '__main__':
    
    from multiprocessing import Pool, cpu_count
    import time
    
    t = time.time()
    
    y = linspace(0, 2* 3.14159265358979, 10000)
    
    p = Pool( processes = cpu_count() )
    result = p.map(sin, y)
    
    p.close()
    p.join()
    
    print('Process completed in ' + str(time.time() - t))
