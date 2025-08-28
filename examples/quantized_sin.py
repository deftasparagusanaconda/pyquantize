from pyquantize import quantize
from math import sin, pi, radians

import matplotlib.pyplot as plt

qpoints = [quantize(sin(radians(deg)), 0.1) for deg in range(360)]

plt.plot(qpoints)
plt.show()
