#!/usr/bin/env python3

import time
import multiprocessing

def calc_square(numbers, result):
    v.value = 3.14
    for idx, n in enumerate(numbers):
        result[idx] = n**2

if __name__=='__main__':
    arr = [2, 3, 5]

    # Shared memory variable
    # 'd' means double
    # 'i' means integer
    # here size of an array is 3 and data type is integer
    result = multiprocessing.Array('i', 3)
    
    v = multiprocessing.Value('d', 0.0)	
    
    p = multiprocessing.Process(target=calc_square, args=(arr, result))
    
    p.start()
    p.join()
    
    print(result[:])
    print(v.value)
