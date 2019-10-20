#!/usr/bin/env python3

''' The main aim of writting this fibonacci code is to show that how to 
    write the recursive funtions very fast and effective '''

from functools import lru_cache

@lru_cache(maxsize = 5000)
def fibonacci(n):
    # check that input is integer
    if type(n) != int:
        raise TypeError('n must be positive int')
    if n < 1:
        raise ValueError('n must be positive int')
    
    # compute the nth term
    if n == 1:
        return 1
    elif n == 2:
        return 1
    elif n > 2:
        return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(15))

