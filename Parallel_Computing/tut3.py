#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 11:37:10 2019

@author: divyang
"""

from multiprocessing import Process
 
 
def greeting():
    print('hello world')
 
if __name__ == '__main__':
    p = Process(target=greeting)
    p.start()
    p.join()