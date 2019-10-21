#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def add(args):
    x, y = args[0], args[1]
    
    print(x)
    print(y)

    return 0

if __name__ == '__main__':
    
    from multiprocessing import Pool, cpu_count
    
    pool = Pool( processes = cpu_count() )
    
    
    results = pool.map(add, [ [1, [2, 3, 4] ] ])
    
    pool.close()
    pool.join()
