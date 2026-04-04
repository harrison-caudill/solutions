#!/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt
import sys

data = []
bins = list(range(1, 6, 1))
for n in bins:
    datum = n**2 * math.pi**2 / 12 - .5
    data.append(datum)

fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(bins, data,
       color='steelblue',
       edgecolor='black',
       label='Particle in a Box')
 
ax.axhline(y=.25, color='red', linestyle='--', linewidth=2, 
           zorder=4, label='Heisenberg Limit ($1/4$)')

ax.set_title('Particle Position Distribution', fontsize=14)
ax.set_xlabel('Energy Level ($n$)', fontsize=12)
ax.set_ylabel('Variance Product / $\hbar^2$', fontsize=12)
ax.set_xlim(1, bins[-1])
ax.set_ylim(0, data[-2]*1.05)
ax.legend(loc='upper left', fontsize=11)
ax.grid(axis='y', alpha=0.3)

fig.tight_layout()

fig.savefig('energy_levels.pdf', format='pdf', dpi=300)
