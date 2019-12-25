from vpython import *
import numpy as np

#%% constants
g = 9.8                  # Gravitational constant

m1 = 1                   # mass of first ball
m2 = 1                   # mass of second ball

tht1 = 100* np.pi/180    # angle of first mass
tht2 = 0* np.pi/180      # angle of second mass

omg1 =-2                 # initial angular velocity of ball 1
omg2 = 0                 # initial angular velocity of ball 2

l1 = 2                   # lenght of first pendulums
l2 = 1                   # lenght of second pendulums

T  = 70                  # simulation time
dt = 0.001               # accuracy

#%% Coordinates of ball 1 and 2
x1, y1 = l1* np.sin(tht1), -l1* np.cos(tht1)
x2, y2 = l2* np.sin(tht2) + l1* np.sin(tht1), -l2* np.cos(tht2) - l1* np.cos(tht1)

#%% Canvas settings
scene = canvas(title = 'Double Pendulum',
               width = 600, height = 300,
               center= vector(0.5,-1,0), background = color.white)

Hook = box( pos = vector(0, 0, 0), size = vector(0.5, 0.5, 0.5),
            color = color.yellow)

ball1 = sphere( pos = vector(x1, y1, 0), radius = 0.2, color = color.red)
ball2 = sphere( pos = vector(x2, y2, 0), radius = 0.2, color = color.blue)

rod1 = cylinder(pos = vector(0, 0, 0), axis = vector(x1, y1, 0), radius = 0.05)
rod2 = cylinder(pos = vector(x1, y1, 0), axis = vector(x2 - x1, y2 - y1, 0), radius = 0.05)

#%% Graph
gd = graph( width = 600, height = 300,
            title = '<b>Phase Space</b>',
            xtitle = '<i>Theta</i>', ytitle = '<i>Omega</i>',
            foreground = color.black, background = color.white)

phase_1 = gcurve( color = color.red,  label = 'b1' )
phase_2 = gcurve( color = color.blue, label = 'b2' )

#%% Solver
t = 0

while (t < T):

    rate(500)

    A = (m2/(m1 + m2))* (l2/l1)* np.cos(tht2 - tht1)
    B = (g/l1)* np.sin(tht1) - (m2/(m1 + m2))* (l2/l1)* np.sin(tht2 - tht1)* omg2**2

    C = (l1/l2)* np.cos(tht2 - tht1)
    D = (l1/l2)* np.sin(tht2 - tht1)* omg1**2 + (g/l2)* np.sin(tht2)

    # angular velocity update
    omg1 = omg1 + ( (B - A* D)/ (A* C - 1) )* dt
    omg2 = omg2 + ( (D - B* C)/ (A* C - 1) )* dt

    # angle update
    tht1 = tht1 + omg1* dt
    tht2 = tht2 + omg2* dt

    # time update
    t = t + dt

    # Red ball
    ball1.pos.x =   l1* np.sin(tht1)
    ball1.pos.y = - l1* np.cos(tht1)

    rod1.axis.x =   l1* np.sin(tht1)
    rod1.axis.y = - l1* np.cos(tht1)

    # Blue ball
    ball2.pos.x =  l2* np.sin(tht2) + l1* np.sin(tht1)
    ball2.pos.y =- l2* np.cos(tht2) - l1* np.cos(tht1)

    rod2.pos.x = l1* np.sin(tht1)
    rod2.pos.y =-l1* np.cos(tht1)

    rod2.axis.x =  ( l2* np.sin(tht2) + l1* np.sin(tht1) ) - l1* np.sin(tht1)
    rod2.axis.y =  (- l2* np.cos(tht2) - l1* np.cos(tht1)) + l1* np.cos(tht1)

    # Phase space plot
    phase_1.plot( pos=(tht1, omg1) )
    phase_2.plot( pos=(tht2, omg2) )
