from vpython import *
import numpy as np

#%% constants
g = 9.8                 # Gravitational constant
k = 10                  # spring constant
m = 0.1                 # mass of the balls

tht1 = 35* np.pi/180    # angle of first mass
tht2 = 30* np.pi/180    # angle of second mass

l = 2                   # lenght of both pendulums
d = 2                   # separation between mass

T  = 20                 # simulation time
dt = 0.001              # accuracy

#%% Coordinates of ball 1 and 2
x1, y1 =     l* np.sin(tht1), -l* np.cos(tht1)
x2, y2 = d + l* np.sin(tht2), -l* np.cos(tht2)

#%% Canvas settings
scene = canvas(title = 'Coupled Oscillator',
               width = 600, height = 300,
               center= vector(0.5,-1,0), background = color.white)

Hook = box( pos = vector(d/2, 0, 0), size = vector(d + 0.5, 0.5, 0.5),
            color = color.yellow)

ball1 = sphere( pos = vector(x1, y1, 0), radius = 0.2, color = color.red)
ball2 = sphere( pos = vector(x2, y2, 0), radius = 0.2, color = color.blue)

rod1 = cylinder(pos = vector(0, 0, 0), axis = vector(l* np.sin(tht1), -l* np.cos(tht1), 0), radius = 0.05)
rod2 = cylinder(pos = vector(d, 0, 0), axis = vector(l* np.sin(tht2), -l* np.cos(tht2), 0), radius = 0.05)

Spring = cylinder(pos  = vector(l* np.sin(tht1)/2,-l* np.cos(tht1)/2, 0),
                  axis = vector(d + l* np.sin(tht2)/2 - l* np.sin(tht1)/2,-l* np.cos(tht2)/2 + l* np.cos(tht1)/2, 0),
                  radius = 0.05,
                  color  = color.orange)

#%% Graph
gd = graph( width = 600, height = 300,
            title = '<b>Phase Space</b>',
            xtitle = '<i>Theta</i>', ytitle = '<i>Omega</i>',
            foreground = color.black, background = color.white)

phase_1 = gcurve( color = color.red,  label = 'b1' )
phase_2 = gcurve( color = color.blue, label = 'b2' )

#%% Solver
omega_1 = 0
omega_2 = 0

t = 0

while (t < T):

    rate(500)

    # angular velocity update
    omega_1 = omega_1 + ( -g* np.sin(tht1)/l + k* np.sin(2*(tht2-tht1))/ (8* m) )* dt
    omega_2 = omega_2 + ( -g* np.sin(tht2)/l - k* np.sin(2*(tht2-tht1))/ (8* m) )* dt

    # angle update
    tht1 = tht1 + omega_1* dt
    tht2 = tht2 + omega_2* dt

    # time update
    t = t + dt

    # Red ball
    ball1.pos.x =   l* np.sin(tht1)
    ball1.pos.y = - l* np.cos(tht1)

    rod1.axis.x =   l* np.sin(tht1)
    rod1.axis.y = - l* np.cos(tht1)

    # Blue ball
    ball2.pos.x =  l* np.sin(tht2) + d
    ball2.pos.y =- l* np.cos(tht2)

    rod2.axis.x =   l* np.sin(tht2)
    rod2.axis.y = - l* np.cos(tht2)

    # Spring
    Spring.pos.x  =   l* np.sin(tht1)/2
    Spring.pos.y  = - l* np.cos(tht1)/2
    Spring.axis.x = d + l* np.sin(tht2)/2 - l* np.sin(tht1)/2
    Spring.axis.y =   - l* np.cos(tht2)/2 + l* np.cos(tht1)/2

    # Phase space plot
    phase_1.plot( pos=(tht1, omega_1) )
    phase_2.plot( pos=(tht2, omega_2) )
