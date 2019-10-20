from vpython import *
import numpy as np
sin = np.sin
cos = np.cos
pi = np.pi

def pol2cart(r, th, z):
    x = r* cos(pi/2 - th)
    y = r* sin(pi/2 - th)
    return x, y, z

def cart2pol( x, y, z):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2( x, y)
    return( rho, phi, z)

# Canvas settings
scene = canvas(title = 'Pendulum',
               width = 1100, height = 600,
               center= vector(0,0,0), background = color.black)

t  = 0           # Initial time
dt = 0.01        # small steps
g  = 9.8         # gravitational accelaration

l0 = 3.8
l1 = 3.7
l2 = 3.6
l3 = 3.5
l4 = 3.4
l5 = 3.3
l6 = 3.2
l7 = 3.1
l8 = 3.0

tta0 = 50* (pi/180)
tta1 = 50* (pi/180)
tta2 = 50* (pi/180)
tta3 = 50* (pi/180)
tta4 = 50* (pi/180)
tta5 = 50* (pi/180)
tta6 = 50* (pi/180)
tta7 = 50* (pi/180)
tta8 = 50* (pi/180)

x0, y0, z0 = pol2cart(l0, tta0, -2)
x1, y1, z1 = pol2cart(l1, tta1, -1.5)
x2, y2, z2 = pol2cart(l2, tta2, -1)
x3, y3, z3 = pol2cart(l3, tta3, -0.5)
x4, y4, z4 = pol2cart(l4, tta4, 0)
x5, y5, z5 = pol2cart(l5, tta5, 0.5)
x6, y6, z6 = pol2cart(l6, tta6, 1)
x7, y7, z7 = pol2cart(l7, tta7, 1.5)
x8, y8, z8 = pol2cart(l8, tta8, 2)

m0 = 1
m1 = 1
m2 = 1
m3 = 1
m4 = 1
m5 = 1
m6 = 1
m7 = 1
m8 = 1

L0 = 0
L1 = 0
L2 = 0
L3 = 0
L4 = 0
L5 = 0
L6 = 0
L7 = 0
L8 = 0

I0 = m0* l0**2
I1 = m1* l1**2
I2 = m2* l2**2
I3 = m3* l3**2
I4 = m4* l4**2
I5 = m5* l5**2
I6 = m6* l6**2
I7 = m7* l7**2
I8 = m8* l8**2

Hook = box( pos = vector(0, 2, 0), size = vector(0.5, 0.1, 5),
            color = color.yellow)

ball0 = sphere( pos = vector(x0, y0, z0), radius = 0.2, color = color.magenta)
ball1 = sphere( pos = vector(x1, y1, z1), radius = 0.2, color = color.red)
ball2 = sphere( pos = vector(x2, y2, z2), radius = 0.2, color = color.blue)
ball3 = sphere( pos = vector(x3, y3, z3), radius = 0.2, color = color.green)
ball4 = sphere( pos = vector(x4, y4, z4), radius = 0.2, color = color.cyan)
ball5 = sphere( pos = vector(x5, y5, z5), radius = 0.2, color = color.orange)
ball6 = sphere( pos = vector(x6, y6, z6), radius = 0.2, color = color.magenta)
ball7 = sphere( pos = vector(x7, y7, z7), radius = 0.2, color = color.red)
ball8 = sphere( pos = vector(x8, y8, z8), radius = 0.2, color = color.blue)

rod0 = cylinder(pos = vector(0, 0, z0), axis = vector(0, l0, 0), radius = 0.05)
rod1 = cylinder(pos = vector(0, 0, z1), axis = vector(0, l1, 0), radius = 0.05)
rod2 = cylinder(pos = vector(0, 0, z2), axis = vector(0, l2, 0), radius = 0.05)
rod3 = cylinder(pos = vector(0, 0, z3), axis = vector(0, l3, 0), radius = 0.05)
rod4 = cylinder(pos = vector(0, 0, z4), axis = vector(0, l4, 0), radius = 0.05)
rod5 = cylinder(pos = vector(0, 0, z5), axis = vector(0, l5, 0), radius = 0.05)
rod6 = cylinder(pos = vector(0, 0, z6), axis = vector(0, l6, 0), radius = 0.05)
rod7 = cylinder(pos = vector(0, 0, z7), axis = vector(0, l7, 0), radius = 0.05)
rod8 = cylinder(pos = vector(0, 0, z8), axis = vector(0, l8, 0), radius = 0.05)

while (t < 25):
    rate(100)
    # Torque
    tau0 = -m0* g* l0* sin(tta0)
    L0   = L0 + tau0* dt
    tta0 = tta0 + (L0/I0)* dt

    tau1 = -m1* g* l1* sin(tta1)
    L1   = L1 + tau1* dt
    tta1 = tta1 + (L1/I1)* dt

    tau2 = -m2* g* l2* sin(tta2)
    L2   = L2 + tau2* dt
    tta2 = tta2 + (L2/I2)* dt

    tau3 = -m3* g* l3* sin(tta3)
    L3   = L3 + tau3* dt
    tta3 = tta3 + (L3/I3)* dt

    tau4 = -m4* g* l4* sin(tta4)
    L4   = L4 + tau4* dt
    tta4 = tta4 + (L4/I4)* dt

    tau5 = -m5* g* l5* sin(tta5)
    L5   = L5 + tau5* dt
    tta5 = tta5 + (L5/I5)* dt

    tau6 = -m6* g* l6* sin(tta6)
    L6   = L6 + tau6* dt
    tta6 = tta6 + (L6/I6)* dt

    tau7 = -m7* g* l7* sin(tta7)
    L7   = L7 + tau7* dt
    tta7 = tta7 + (L7/I7)* dt

    tau8 = -m8* g* l8* sin(tta8)
    L8   = L8 + tau8* dt
    tta8 = tta8 + (L8/I8)* dt

    # Ball's Position
    x0, y0, z0 = pol2cart(l0, tta0, 0)
    ball0.pos.x = x0
    ball0.pos.y = -y0 + 2

    x1, y1, z1 = pol2cart(l1, tta1, 0)
    ball1.pos.x = x1
    ball1.pos.y = -y1 + 2

    x2, y2, z2 = pol2cart(l2, tta2, 0)
    ball2.pos.x = x2
    ball2.pos.y = -y2 + 2

    x3, y3, z3 = pol2cart(l3, tta3, 0)
    ball3.pos.x = x3
    ball3.pos.y = -y3 + 2

    x4, y4, z4 = pol2cart(l4, tta4, 0)
    ball4.pos.x = x4
    ball4.pos.y = -y4 + 2

    x5, y5, z5 = pol2cart(l5, tta5, 0)
    ball5.pos.x = x5
    ball5.pos.y = -y5 + 2

    x6, y6, z6 = pol2cart(l6, tta6, 0)
    ball6.pos.x = x6
    ball6.pos.y = -y6 + 2

    x7, y7, z7 = pol2cart(l7, tta7, 0)
    ball7.pos.x = x7
    ball7.pos.y = -y7 + 2

    x8, y8, z8 = pol2cart(l8, tta8, 0)
    ball8.pos.x = x8
    ball8.pos.y = -y8 + 2

    # Update
    rod0.pos.x = x0
    rod0.pos.y = -y0 + 2
    rod0.axis.x =-l0* sin(tta0)
    rod0.axis.y = l0* cos(tta0)

    rod1.pos.x = x1
    rod1.pos.y = -y1 + 2
    rod1.axis.x =-l1* sin(tta1)
    rod1.axis.y = l1* cos(tta1)

    rod2.pos.x = x2
    rod2.pos.y = -y2 + 2
    rod2.axis.x =-l2* sin(tta2)
    rod2.axis.y = l2* cos(tta2)

    rod3.pos.x = x3
    rod3.pos.y = -y3 + 2
    rod3.axis.x =-l3* sin(tta3)
    rod3.axis.y = l3* cos(tta3)

    rod4.pos.x = x4
    rod4.pos.y = -y4 + 2
    rod4.axis.x =-l4* sin(tta4)
    rod4.axis.y = l4* cos(tta4)

    rod5.pos.x = x5
    rod5.pos.y = -y5 + 2
    rod5.axis.x =-l5* sin(tta5)
    rod5.axis.y = l5* cos(tta5)

    rod6.pos.x = x6
    rod6.pos.y = -y6 + 2
    rod6.axis.x =-l6* sin(tta6)
    rod6.axis.y = l6* cos(tta6)

    rod7.pos.x = x7
    rod7.pos.y = -y7 + 2
    rod7.axis.x =-l7* sin(tta7)
    rod7.axis.y = l7* cos(tta7)

    rod8.pos.x = x8
    rod8.pos.y = -y8 + 2
    rod8.axis.x =-l8* sin(tta8)
    rod8.axis.y = l8* cos(tta8)

    t = t + dt
