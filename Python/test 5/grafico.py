import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))

x1 = np.linspace(0, 3, 10)
y1 = -1*(-10 -24.9*x1 - 0.13*(x1**2)/2)
plt.plot(x1, y1)

x2 = np.linspace(3, 6, 10)
y2 = -1*(-10 -24.9*x2 -0.13*(x2**2)/2 -20*(x2-3))
plt.plot(x2, y2)

x3 = np.linspace(6, 8, 10)
y3 = -1*(-10 -24.9*x3 -0.13*(x3**2)/2 -20*(x3-3) +106.3*(x3-6) -10*((x3-6)**2)/2)
plt.plot(x3, y3)

x4 = np.linspace(8, 11, 10)
y4 = -1*(-10 -24.9*x4 -0.13*(x4**2)/2 -20*(x4-3) +106.3*(x4-6) -10*((x4-6)**2)/2)
plt.plot(x4, y4)

plt.show()