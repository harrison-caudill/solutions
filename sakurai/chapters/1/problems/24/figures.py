#!/usr/bin/env python

#!/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt
import os
import scipy
import sys

class ItFigures(object):

    def go(self, outpath):
        pass

def classical_fall_time(d, m, L):
    g = 9.81 # m/s^2
    k = -0.144304
    c1 = d/L
    c2 = (scipy.constants.hbar/d*m*L) * (L/g)**0.5
    gamma = (g/L)**.5
    c = (c1**2 + c2**2)**.5
    return ((1/gamma)
            * (0
               + math.log(2*math.pi)
               - 2*k
               - math.log(c)))

if __name__ == '__main__':
    print(classical_fall_time(d=10.0**-25,
                              m=0.1,
                              L=0.1))
