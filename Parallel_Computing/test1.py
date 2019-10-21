#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 12:53:30 2019

@author: divyang
"""

from multiprocessing import Process
 
 
def sqr():
 
    for x in numbers:
        Squares.append(x**2)

    return Squares

 
if __name__ == '__main__':
    
    numbers = [1, 2, 3, 4, 5]
    Squares = []
 
    p1 = Process(target = sqr)
 
    p1.start()
 
    p1.join()
