#!/usr/bin/env python3
"""#1057: out-of-sample prediction of the two-mode fit (twomode949.py's own `real`, `fit`, `pair`, `share`, unchanged) at a D not yet read, from the last five states.

    predict1057.py D_NEXT [N]     prints the fit's sigma_Delta, sigma_2, their ratio and the lowest vector's Delta share at D_NEXT (written before the read, to be compared with it)"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import twomode949 as tm  # noqa: E402

dn = float(sys.argv[1])
n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
D, sd, s2, sh = tm.real(n)
th, rms = tm.fit(D, sd, s2)
x = np.array([dn - D[-1]])
a, b = tm.pair(th, x)
print(f"fit on the last {n} states D {D[0]:.4f} to {D[-1]:.4f}: gamma {th[4]:.4f}, D_c {tm.crossing(th, D[-1]):.3f}, rms {rms:.2e}")
print(f"prediction at D {dn}: sigma_Delta {float(a[0]):.4e}, sigma_2 {float(b[0]):.4e}, sigma_2/sigma_Delta {float(b[0] / a[0]):.3f}, Delta share of the lowest vector {float(tm.share(th, x)[0]):.3f}")
