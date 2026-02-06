import pyquantize as pq
from math import sin, pi, radians

import matplotlib.pyplot as plt

lattice = pq.Lattice(0.1)

quantized_points = [lattice.project(sin(radians(deg))) for deg in range(360)]

plt.plot(quantized_points)
plt.show()
