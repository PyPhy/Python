from vpython import *
import numpy as np
np.sin = sin; np.cos = cos; np.pi = pi

gd = graph( width = 600, height = 300,
            title = '<b>Graph</b>',
            xtitle = '<i>t</i>', ytitle = '<i>x(t), y(t)</i>',
            foreground = color.black, background = color.white)

x_graph = gcurve( color = color.green, label = 'x' )
y_graph = gcurve( color = color.red,   label = 'y' )

def pol2cart(r, th, z):
    x = r* cos(pi/2 - th)
    y = r* sin(pi/2 - th)
    return x, y, z

def cart2pol( x, y, z):
    rho = sqrt(x**2 + y**2)
    phi = np.arctan2( x, y)
    return( rho, phi, z)

# Canvas settings
scene = canvas(title = 'Pendulum',
               width = 600, height = 300,
               center= vector(0,0,0), background = color.black)

l = 2                               # lenght of pendulum
tta = (90+45)* (pi/180)                  # Initial angle
x, y, z = pol2cart(l, tta, 0)

t = 0           # Initial time
dt = 0.01       # small steps
g = 9.8         # gravitational accelaration
m = 1           # mass of ball
L = 0           # Initial angular momentum
I = m* l**2     # moment of inertia

Hook = box( pos = vector(0, 2, 0), size = vector(0.5, 0.1, 1.5),
            color = color.yellow)

ball = sphere( pos = vector(x, y, 0), radius = 0.2, color = color.red)

rod = cylinder(pos = vector(0, 0, 0), axis = vector(0, l, 0), radius = 0.05)

while (t < 15):
    rate(100)
    _, tta, _ = cart2pol(x, y, 0)

    tau = -m* g* l* sin(tta)
    L = L + tau* dt
    tta = tta + (L/I)* dt
    t = t + dt

    x, y, z = pol2cart(l, tta, 0)
    ball.pos.x = x
    ball.pos.y = -y + 2

    rod.pos.x = x
    rod.pos.y = -y + 2
    rod.axis.x =-l* sin(tta)
    rod.axis.y = l* cos(tta)

    x_graph.plot(pos=(t, x) )
    y_graph.plot(pos=(t,-y + 2) )
