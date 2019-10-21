#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import multiprocessing

def deposit(balance, lock):
    for i in range(100):
        time.sleep(0.01)
        
        lock.acquire()
        balance.value = balance.value + 1   # Lock this critical variable 
        lock.release()

def withdraw(balance, lock):
    for i in range(100):
        time.sleep(0.01)
        
        lock.acquire()
        balance.value = balance.value - 1   # Lock this critical variable
        lock.release()

if __name__ == '__main__':
    
    balance = multiprocessing.Value('i', 200)
    
    # Lock variable to avoide excess of "balance" at the same time
    lock = multiprocessing.Lock()
    
    d = multiprocessing.Process(target=deposit, args=(balance,lock))
    w = multiprocessing.Process(target=withdraw, args=(balance,lock))
    
    d.start()
    w.start()
    
    d.join()
    w.join()
    print(balance.value)