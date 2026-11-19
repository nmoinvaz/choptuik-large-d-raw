#!/usr/bin/env python3
"""compare997.py M256.npz M160.npz [M128.npz]: Delta_k of the saved series (anm_lowd.py --save_series: delta_hi + delta_lo, double-double parts of z_k's last
unknown) at each M, per order, with the relative difference of M 256 against M 160 and of M 160 against M 128; then, per M, the partial sums of Delta_k h^k at
h = -0.01 and the size of each term and of |z_k| h^k (max norm of z_k's double-double sum over all unknowns), the series' own check at D 3.14 without Newton.
Reference at D 3.14: Newton's Delta at M 160 and M 128 from win2b's runs (series/anm_lowd_D3.140000_M160.npz, series_M128/anm_lowd_D3.140000_M128.npz) is given by --ref.
Exit 1 if the files disagree on D0 or N."""
import sys
import numpy as np
import mpmath as mp

mp.mp.dps = 40
paths = [a for a in sys.argv[1:] if not a.startswith("--")]
ref = None
for a in sys.argv[1:]:
    if a.startswith("--ref="):
        ref = mp.mpf(a[6:])
S = []
for p in paths:
    f = np.load(p, allow_pickle=False)
    dk = [mp.mpf(float(h)) + mp.mpf(float(l)) for h, l in zip(f["delta_hi"], f["delta_lo"])]
    zn = [float(np.abs(np.asarray(f["zh"][k]) + np.asarray(f["zl"][k])).max()) for k in range(len(f["zh"]))]
    S.append(dict(path=p, M=int(f["M"]), D0=float(f["D0"]), dk=dk, zn=zn))
if len({s["D0"] for s in S}) != 1 or len({len(s["dk"]) for s in S}) != 1:
    print("the files differ in D0 or in N"); sys.exit(1)
N = len(S[0]["dk"]) - 1
print(f"D0 {S[0]['D0']}, N {N}, M " + ", ".join(str(s['M']) for s in S))
print("k | " + " | ".join(f"Delta_k(M {s['M']})" for s in S) + " | " + " | ".join(f"rel diff M {S[i]['M']} vs {S[i+1]['M']}" for i in range(len(S) - 1)))
for k in range(N + 1):
    row = [mp.nstr(s["dk"][k], 12) for s in S]
    rel = [mp.nstr(abs(S[i]["dk"][k] - S[i + 1]["dk"][k]) / abs(S[i + 1]["dk"][k]), 3) for i in range(len(S) - 1)]
    print(f"{k} | " + " | ".join(row) + " | " + " | ".join(rel))
h = mp.mpf("-0.01")
print("\npartial sums at h = -0.01: k | per M: term Delta_k h^k, partial sum minus the reference | |z_k| h^k (max norm)")
for s in S:
    ps = mp.mpf(0)
    print(f"M {s['M']}:")
    for k in range(N + 1):
        t = s["dk"][k] * h ** k
        ps += t
        print(f"  {k:2d}  term {mp.nstr(t, 4):>11}  partial sum {mp.nstr(ps, 18)}" + (f"  minus ref {mp.nstr(ps - ref, 4)}" if ref is not None else "") + f"   |z_k| h^k {s['zn'][k] * 1e-2 ** k:.3e}")
