from vpython import *
import numpy as np

#%% constants

# spring constant
k1 = 1
k2 = 1

# mass of the balls
m1 = 1
m2 = 1

# Coordinates of ball 1 and 2
x1 = 0.5
x2 = 2.5

# velocity
v1 = 0
v2 = 0

#%% Canvas settings
scene = canvas(title = 'Springs',
               width = 600, height = 200,
               center= vector(0, 0, 0), background = color.white)

Hook = box( pos = vector(0, 0, 0), size = vector(0.1, 0.1, 0.1),
            color = color.yellow)

ball1 = sphere( pos = vector(x1, 0, 0), radius = 0.2, color = color.red)
ball2 = sphere( pos = vector(x2, 0, 0), radius = 0.2, color = color.blue)

Spring1 = cylinder(pos  = vector(0, 0, 0),
                   axis = vector(x1, 0, 0),
                   radius = 0.05,
                   color  = color.orange)

Spring2 = cylinder(pos  = vector(x1, 0, 0),
                   axis = vector(x2 - x1, 0, 0),
                   radius = 0.05,
                   color  = color.cyan)

#%% Graph
gd = graph( width = 600, height = 300,
            title = '<b>Phase Space</b>',
            xtitle = '<i>x1</i>', ytitle = '<i>x2</i>',
            foreground = color.black, background = color.white)

phase = gcurve( color = color.blue )

#%% Solver
T  = 200     # simulation time
dt = 0.001   # accuracy

t = 0
while (t < T):

    rate(3000)

    # angular velocity update
    v1 = v1 + ( -(k1 + k2)* x1 + k2* x2 )* dt
    v2 = v2 + ( k2* x1 - k2* x2 )* dt

    # angle update
    x1 = x1 + v1* dt
    x2 = x2 + v2* dt

    # time update
    t = t + dt

    # Red ball
    ball1.pos.x = x1

    # Blue ball
    ball2.pos.x = x2

    # Spring
    Spring1.axis.x = x1

    Spring2.pos.x = x1
    Spring2.axis.x = x2 - x1

    # Phase space plot
    phase.plot( pos=(x1, x2) )
