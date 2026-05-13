#!/usr/bin/env python

#!/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt
import os
import pprint
import scipy
import sympy
import sys

class ItFigures(object):

    def go(self, outpath):
        # Universal mathematical constants
        self.k = -float(sympy.EulerGamma/4)
        self.C = float(sympy.EulerGamma)
        self.g = scipy.constants.g
        self.h = scipy.constants.hbar

        # Chosen Constants
        self.m = 0.1 # kg
        self.L = 0.1 # m

        # Computed constants
        self.gamma = (self.g/self.L)**.5

        # Compute the max number of necessary points
        self.dpi = 300
        width_in = 8.5
        self.max_n_pts = int(self.dpi * width_in)

        # Generate a plot based upon the ratio
        self.by_log_ratio(outpath)
        self.by_linear_ratio(outpath)
        self.by_log_value(outpath)
        self.printables()

    def c1(self, d):
        return d/self.L

    def c2(self, d):
        return self.h/(d*self.m*self.L*self.gamma)

    def c(self, d):
        return (self.c1(d)**2 + self.c2(d)**2)**.5

    def d(self, R=None):
        if R:
            # returns d for the given ratio of C1/C2
            d = ((self.h * R) / (self.m * self.gamma))**0.5
        else:
            # maximizes fall time
            d = (self.h / (self.m * self.gamma))**0.5
        assert(d > 0)
        return d

    def tfc(self, d):
        return ((1/self.gamma)
                * (0
                   + math.log(2*math.pi)
                   - 2*self.k
                   - math.log(self.c(d))))

    def by_log_ratio(self, outpath):
        x = []
        y = []
        R0 = 10**-20
        R1 = 100.0
        N = self.max_n_pts
        s = math.e**((1/N)*math.log(R1/R0))
        R = R0
        for i in range(N):
            d = self.d(R=R)
            x.append(R)
            y.append(self.tfc(d))
            R *= s

        fig, ax = plt.subplots()
        ax.semilogx(x, y, label='<Fall Time> (s)')
        ax.axvline(x=1,
                   color='red',
                   linestyle='--',
                   label='Balanced Uncertainty')
        cur = list(ax.get_xticks())
        cur.append(1)
        ax.set_xticks(cur)
        ax.set_title('Fall-Time vs C1/C2 Ratio', fontsize=14)
        ax.set_xlabel('Ratio (C1/C2)', fontsize=12)
        ax.set_ylabel('<Fall Time> (s)', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        fig.savefig(os.path.join(outpath, 'by_log_ratio.pdf'),
                    format='pdf',
                    dpi=self.dpi)

    def by_linear_ratio(self, outpath):
        N = self.max_n_pts
        x = []
        y = []
        R0 = 10**-2
        R1 = 10.0
        s = (R1-R0)/N
        for i in range(N):
            R = R0 + i*s
            d = self.d(R=R)
            x.append(R)
            y.append(self.tfc(d))

        fig, ax = plt.subplots()
        ax.plot(x, y, label='<Fall Time> (s)')
        ax.axvline(x=1,
                   color='red',
                   linestyle='--',
                   label='Balanced Uncertainty')
        cur = list(ax.get_xticks())
        cur.append(1)
        ax.set_xticks(cur)
        ax.set_title('Fall-Time vs C1/C2 Ratio', fontsize=14)
        ax.set_xlabel('Ratio (C1/C2)', fontsize=12)
        ax.set_ylabel('<Fall Time> (s)', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(outpath, 'by_linear_ratio.pdf'),
                    format='pdf', dpi=self.dpi)

    def by_log_value(self, outpath):
        N = self.max_n_pts
        d0 = 10**-33
        d1 = 10**-2
        x = []
        y = []
        s = math.e**((1/N)*math.log(d1/d0))
        d = d0
        for i in range(N):
            x.append(d)
            y.append(self.tfc(d))
            d *= s

        fig, ax = plt.subplots()
        ax.semilogx(x, y, label='<Fall Time> (s)')
        ax.axvline(x=self.d(),
                   color='red',
                   linestyle='--',
                   label='Balanced Uncertainty')
        ax.set_title('Fall-Time vs d', fontsize=14)
        ax.set_xlabel('d (m)', fontsize=12)
        ax.set_ylabel('<Fall Time> (s)', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(outpath, 'by_log_value.pdf'),
                    format='pdf', dpi=self.dpi)

    def tfe(self, s):
        return (1/self.gamma) * (
            math.log(self.gamma * math.pi * self.L * (self.m/2)**.5)
            + self.C/4
            + math.log(2)/4
            - math.log(s)/2)

    def printables(self):

        print("="*80)
        print("X/P Method")
        print("="*80)
        print("")

        # appropriate value of sigma_e
        d = self.d()
        print(f"d:       {d}")

        # expectation value for the fall-time
        ft = self.tfc(d)
        print(f"<tf>:    {ft}")
        print("")
        ft_xp = ft

        print("="*80)
        print("E = N(0, sigma)")
        print("="*80)
        print("")
        # appropriate value of sigma_t
        st = math.pi / (4*2**.5*self.gamma)
        print(f"sigma-t: {st}")

        # appropriate value of sigma_e
        se = self.h/(2*st)
        print(f"sigma-e: {se}")

        # expectation value for the fall-time given that energy uncertainty
        ft = self.tfe(se)
        print(f"<tf>:    {ft}")
        print("")
        ft_en = ft
        
        print("="*80)
        print("P = N(0, sigma)")
        print("="*80)
        # appropriate value of sigma_t
        st = math.pi / (2**.5*self.gamma)
        print(f"sigma-t: {st}")

        # appropriate value of sigma_e
        se = self.h/(2*st)
        print(f"sigma-e: {se}")

        # expectation value for the fall-time given that energy uncertainty
        ft = self.tfe(se)
        print(f"<tf>:    {ft}")
        ft_pn = ft

        print("="*80)
        print("Differences")
        print("="*80)
        print("")
        print(f"X/P vs E=N: {abs(ft_xp - ft_en)}")
        print(f"X/P vs P=N: {abs(ft_xp - ft_pn)}")
