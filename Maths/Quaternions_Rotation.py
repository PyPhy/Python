#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import sin, cos, pi

def Rotation(r, ω, θ):
    '''
    "r" is the target point which we want to rotate about the "ω" axis with an angle "θ".
    1. Rotation is defined by right hand screw rule.
    2. "ω" is the unit vector i.e. a^2 + b^2 + c^2 = 1.
    3. Quaternions solves the "gimbal lock" problem which is the disadvantage of Euler rotation matrix.
    '''
    
    x, y, z = r[0], r[1], r[2]
    a, b, c = ω[0], ω[1], ω[2]
    
    A = 0
    B = (1 + cos(θ))* x + (1 - cos(θ))* ( ( a**2 - b**2 - c**2)*x + 2*a*(b*y + c*z) ) + 2* sin(θ)* (b*z - c*y)
    C = (1 + cos(θ))* y + (1 - cos(θ))* ( (-a**2 + b**2 - c**2)*y + 2*b*(c*z + a*x) ) + 2* sin(θ)* (c*x - a*z)
    D = (1 + cos(θ))* z + (1 - cos(θ))* ( (-a**2 - b**2 + c**2)*z + 2*c*(a*x + b*y) ) + 2* sin(θ)* (a*y - b*x)
    
    return [A, 0.5* B, 0.5* C, 0.5* D]

print( Rotation([1,0,0], [0,1,0], pi) )
