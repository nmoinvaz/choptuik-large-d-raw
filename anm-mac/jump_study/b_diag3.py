"""Which stored M=32 states have p1 harmonics above 13 at zero (the kfreeze 13 system)?"""
import numpy as np
from b_lib import *
tr = train_files(dmin=0, dmax=200)
for D, p in tr:
    h = T @ zf(load(p)[1])
    hn = max(abs(h[i]) for i, l in enumerate(LABELS) if l[1] == 'p1' and l[3] >= 15)
    if D < 37 or hn > 1e-15: print(f'{p.split("/")[-1]:24s} {hn:.2e}')
