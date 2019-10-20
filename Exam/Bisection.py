#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% Bisection
    
def Bisection(a, b, n, f):
    
    ''' a = start point
        b = end point
        n = number of iteration'''
    
    if ( f(a) == f(b) ) or ( (f(a) < 0) and (f(b) < 0) ) or ( (f(a) > 0) and (f(b) > 0) ):
        
        return 'Method failed', 'Method failed'
        
    else:
        i = 1
        while (i <= n):
            
            c = (a + b)/2
            B = f(c)
            
            if ( (f(c) < 0) and (f(b) < 0) ) or ( (f(c) > 0) and (f(b) > 0) ):
                
                b = c
                
            elif ( (f(a) < 0) and (f(c) < 0) ) or ( (f(a) > 0) and (f(c) > 0) ):
                
                a = c                
            
            i = i + 1
        
    return c, B


#%% Example

# starting and ending points
a = 1
b = 2

# iteration
n = 8

# function
f = lambda x: x**3 + 3*x - 5

c, B = Bisection(a, b, n, f)

