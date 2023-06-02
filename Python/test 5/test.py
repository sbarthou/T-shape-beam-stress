B = 500
H = 500
l = 32
t = 32

W = 7850*((B*l + t*(H-l))/1000**2)*0.001

Cy = (20*3 + W*11*(11/2) + 10*2*7 + 40*11 - 10)/6
Ay = abs(80 + W*11 - Cy)

# Diagrama fuerza cortante
p1 = -Ay
p2 = p1 - 20
p3 = p2 + Cy
p4 = p3 - 20

A1 = p1*3
A2 = p2*3
A3 = p4*2+20
A4 = p4*3

# Diagrama momento flector
Mz = -10 -Ay*x -W*(x**2)/2 -20*(x-3)

