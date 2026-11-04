"""Task 1b: high p1 harmonics per training state; guess error per component at the truth states; truth uniqueness."""
import numpy as np
from b_lib import *
d = np.load('diag1.npz'); Ds, Hc = d['Ds'], d['Hc']
tr = train_files()
idx = {lab: i for i, lab in enumerate(LABELS)}
def hi_norm(h, kmin):
    return max(abs(h[i]) for i, l in enumerate(LABELS) if l[1] == 'p1' and l[3] >= kmin)
print('state, max|p1 harmonics k>=15|, p1 s13, p1 c13, p1 c11')
for (D, p), h in zip(tr, Hc):
    print(f'  {p.split("/")[-1]:24s} {hi_norm(h,15):.2e} {h[idx[("ctr","p1","s",13)]]:+.4e} {h[idx[("ctr","p1","c",13)]]:+.4e} {h[idx[("ctr","p1","c",11)]]:+.6e}')
print('\ntruth states:')
TH = {}
for D, p in TRUTH.items():
    h = T @ zf(load(p)[1]); TH[D] = h
    print(f'  {D} {p.split("/")[-1]:30s} {hi_norm(h,15):.2e} {h[idx[("ctr","p1","s",13)]]:+.4e} {h[idx[("ctr","p1","c",13)]]:+.4e} {h[idx[("ctr","p1","c",11)]]:+.6e}')
print('\nuniqueness of the full-system qd solution: pin5 vs pin7 _full')
for Dt in ('68.5000', '69.5000', '70.5000'):
    a = zf(load(R + f'T84-mac/pin5_D{Dt}_full.npz')[1]); b = zf(load(R + f'T84-mac/pin7_D{Dt}_full.npz')[1])
    da = np.abs(T @ (a - b)); i = da.argmax()
    print(f'  D {Dt}: max |dz| {np.abs(a-b).max():.2e}, worst harmonic {LABELS[i]} {da[i]:.2e}')
