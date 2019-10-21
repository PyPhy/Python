#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import multiprocessing as mp

x = np.array([[1, 2], [3, 4]])

def f(x):
    return x**2

def pool_handler():
    pool = mp.Pool(mp.cpu_count())
    Sq = pool.map(f, x)
    pool.close()
    return Sq

if __name__ == '__main__':
    Sq = pool_handler()
    