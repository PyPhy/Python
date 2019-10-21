#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import arange
import time
from numba import jit

start_time = time.time()

@jit
def sum2d(arr):
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]
    return result

a = arange(5000* 5000).reshape(5000, 5000)
print(sum2d(a))

elapsed_time = time.time() - start_time
print('elapsed time is: ' + str(elapsed_time))
