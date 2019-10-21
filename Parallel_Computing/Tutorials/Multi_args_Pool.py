#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def multi_run_wrapper(args):
    
    return add(*args)

def add(x,y):

    return x+y

if __name__ == '__main__':
    
    from multiprocessing import Pool, cpu_count
    
    pool = Pool( processes = cpu_count() )
    
    results = pool.map(multi_run_wrapper,[(1,2),(2,3),(3,4)])
    
    pool.close()
    pool.join()
    