#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 11:40:02 2019

@author: divyang
"""

from multiprocessing import Process
 
 
def square():
 
    for x in numbers:
        Squares.append(x**2)

    return Squares
 
def cube():
 
    for x in numbers:
        Cubes.append(x**3)

    return Cubes
 
if __name__ == '__main__':
    
    numbers = [1, 2, 3, 4, 5]
    Squares = []
    Cubes = []
 
    p1 = Process(target = square)
    p2 = Process(target = cube)
 
    p1.start()
    p2.start()
 
    p1.join()
    p2.join()
