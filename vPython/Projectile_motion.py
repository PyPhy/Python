from __future__ import print_function, division
from vpython import *
import numpy as np

# Canvas settings
scene = canvas(title = 'Projectile Motion',
               width = 1000, height = 600,
               center= vector(0,0,0), background = color.white)
AnimationSpeed = 100

Angle = 45                            # Initial Angle in degrees
v0    = 15                            # Initial velocity
x0    = -11                           # Initial position
y0    = 2
g     = 9.8                           # earth's accelaration
T     = 10                            # simulation time in second

t   = np.linspace(0, T, int( AnimationSpeed* T) )
tta = Angle* np.pi/ 180               # Angle in radians

# Wood
wood = box( pos = vector(x0, y0, 0), size = vector(2, 0.5, 2),
            color = color.yellow )

# Base
Base = box( pos = vector(0, 0, 0), size = vector(30, 0.5, 30),
            color = color.green )

# ball as sphere
ball = sphere( pos = vector(x0, y0, 0), radius = 0.5,
               color = color.red, make_trail = True)

# animation
for i in range(0, len(t)):
    rate(AnimationSpeed)
    ball.pos.x = x0 + v0* np.cos(tta)* t[i]
    ball.pos.y = y0 + v0* np.sin(tta)* t[i] - 0.5* g* t[i]**2

    # if ball is going below the ground then break
    if (ball.pos.y - 0.5) < 0:
        print('Time of flight is ' + str(t[i]) + ' s')
        print('Range is ' + str(ball.pos.x) + ' m' )
        break
