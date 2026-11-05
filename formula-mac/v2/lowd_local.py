# Local structure of Delta near D = 3 from the converged points 3.04375-4 (no fit beyond local differences):
# x = D - 3; alpha_eff = d ln Delta / d ln x (a power law A x^alpha keeps it constant; a finite intercept sends it to 0
# like s); and the derivative dDelta/ds, s = sqrt(x) (finite at s = 0 if Delta is analytic in s).
import numpy as np
from scipy.interpolate import CubicSpline
import common as C
D, H, L, s, run = C.data(); m = D <= 4.0 + 1e-9; D, y = D[m], (H + L)[m]
x = D - 3; lx = np.log(x); ly = np.log(y); sq = np.sqrt(x)
cs = CubicSpline(lx, ly); cs2 = CubicSpline(sq, y)
print(f'{len(D)} points 3.04375-4')
print(f"{'D':>9s} {'Delta':>12s} {'alpha_eff':>10s} {'dDelta/ds':>10s} {'d2Delta/ds2':>12s}")
for d in [3.04375, 3.05, 3.0625, 3.075, 3.1, 3.125, 3.15, 3.2, 3.25, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 4.0]:
    i = np.argmin(abs(D - d))
    print(f'{D[i]:9.5f} {y[i]:12.8f} {cs(lx[i], 1):10.5f} {cs2(sq[i], 1):10.4f} {cs2(sq[i], 2):12.3f}')
