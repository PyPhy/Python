from vpython import *
import numpy as np

# Canvas settings
scene = canvas(title = 'Simple Harmonic Oscillator',
               width = 900, height = 600,
               center= vector(0,0,0), background = color.white)

k = 1                                # spring constant
m = 0.1                              # mass of the ball
T = 20                               # simulation time
omg = np.sqrt(k/ m)                  # angular frequancy
t = np.linspace(0, T, int(100* T) )  # time interval in which the calculations will done

# ball as sphere
ball = sphere( pos = vector(0, 0, 0), radius = 0.2,
               color = color.red)
# Wood
wood = box( pos = vector(-2, 0, 0), size = vector(1.7, 1.5, 1),
            color = color.yellow )
# rod
rod = cylinder( pos = vector(0, 0, 0), axis = vector(-2.2, 0, 0), radius = 0.05)

text( pos = vector(0, 1, 0), text = 'S.H.O.', align = 'center', depth = -0.3, color = color.green)

# animation
for i in range(0, len(t)):
    rate(100)                           # 100 calculations per second
    ball.pos.x = 0.5*np.sin(omg* t[i])  # position as the function of time
    rod.pos.x  = 0.5*np.sin(omg* t[i])
