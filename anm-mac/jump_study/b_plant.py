"""Task 5: planted check of the split extrapolation, on the training D grid (137 states, D 36.07-61.03).
Plant: S(D) = a polynomial in 1/n fitted to the real states (degree 14, clean part) + B/(n - 20) (a pole at n = 20,
which gives Chebyshev coefficients decaying about as fast as the real data's k = 1 components). Noise: 1e-7 and
1e-8 (x3) in four fixed directions (the real data's residual directions), each a smooth bias sin(D/L + phi) plus
white 1e-9, plus 1e-14 white in every component. Truth: S(D). Pass criteria, written before the run:
  (a) the method finds the planted directions: principal angles with the planted V below 1e-3;
  (b) the clean part (P S) at 67.74 recovered to within 3x the error the same settings give on the real data's
      clean part at 68.5 (the level claimed), and below 1e-9;
  (c) control: the same fit without the split (r = 0) has its error dominated by the noise (> 1e-8).
Usage: b_plant.py r Ks Kc [mutate]   mutate=1 plants the noise in 6 directions while the method uses r (control)."""
import sys, numpy as np
from b_lib import *
from b_split import Split, unit_weights, noise_dirs
r, Ks, Kc = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); mut = int(sys.argv[4]) if len(sys.argv) > 4 else 0
d = np.load('train36.npz'); Ds, Hc = d['Ds'], d['Hc']
Z = Hc @ Tinv.T; w = unit_weights(Ds)
rng = np.random.default_rng(7)
Vreal = noise_dirs(Ds, Z, 6, 12, w)[0]
Vp = Vreal[:, :6 if mut else 4]
base = Split(Ds, Z, 4, 14, 0, w=w, V=Vreal[:, :4]).fw          # clean polynomial part of the real data
B = rng.standard_normal(769) * np.maximum(np.abs(Z[-1]), 1e-6) * 3e-3
B[-1] = 3e-3 * Z[-1, -1]
S = lambda D: base(D)[0] + B / (np.asarray(D) - 2 - 20.0)
amps = [1e-7, 1e-8, 1e-8, 1e-8, 1e-8, 1e-8][:Vp.shape[1]]
Ls = rng.uniform(2, 8, len(amps)); ph = rng.uniform(0, 2 * np.pi, len(amps))
noise = np.array([[a * np.sin(D / L + p) + 1e-9 * rng.standard_normal() for a, L, p in zip(amps, Ls, ph)] for D in Ds])
Zp = np.array([S(D) for D in Ds]) + noise @ Vp.T + 1e-14 * rng.standard_normal((len(Ds), 769))
sp = Split(Ds, Zp, r, Ks, Kc, w=w)
V = sp.V
if r:
    sv = np.linalg.svd(V.T @ Vp[:, :4], compute_uv=False)
    print(f'(a) principal angles between found and planted directions: max {np.arccos(np.clip(sv.min(), -1, 1)):.1e} rad')
for Dt in (67.742203, 68.5, 69.5):
    g, wc, c = sp(Dt); zt = S(Dt)
    e = g - zt; Pe = e - V @ (V.T @ e)
    print(f'D {Dt}: total {np.abs(e[:-1]).max():.2e}, clean part {np.abs(Pe[:-1]).max():.2e}, junk coords {np.abs(V.T @ e).max() if r else 0:.2e}, |dDelta| {abs(e[-1]):.1e}')
sp0 = Split(Ds, Zp, 0, Ks, -1, w=w, V=np.zeros((769, 0)))
e0 = sp0(67.742203)[0] - S(67.742203)
print(f'(c) control without the split (r = 0, degree {Ks}): total error at 67.74 {np.abs(e0[:-1]).max():.2e}')
