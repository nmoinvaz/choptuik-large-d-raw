"""The contraction factor of --fix1's passes through the stored double-double LU, c = |r_after| / |r_before| per pass
(records' fix1 = [before, after pass 1, after pass 2]), against D: the double-double Jacobian's error measured against
the quad-double model in its weakest directions. A pass stops reducing once c reaches 1. Also the pivots' growth.
    python contraction_fit.py RAWDIR"""
import glob, json, os, sys
import numpy as np
raw = sys.argv[1]
pts, piv = [], []
for f in sorted(glob.glob(os.path.join(raw, "anm-mac", "run_trend_pin3_qd*", "anm_run.jsonl"))):
    for l in open(f):
        r = json.loads(l)
        piv.append((r["D0"], r["pivots"][0], r["pivots"][1]))
        if r.get("fix1"):
            h = r["fix1"]
            pts.append((r["D0"], h[1] / h[0], h[2] / h[1]))
x = np.array([p[0] for p in pts])
for j, name in ((1, "pass 1"), (2, "pass 2")):
    y = np.log10([p[j] for p in pts]); b = np.polyfit(x, y, 1)
    print(f"contraction {name}: {len(x)} bases, D {x.min():.2f}-{x.max():.2f}: {10 ** np.polyval(b, x.min()):.1e} at the first, growth "
          f"{10 ** b[0]:.2f}x per unit D, rms {np.sqrt(np.mean((y - np.polyval(b, x)) ** 2)):.2f} decades; reaches 1 at D {-b[1] / b[0]:.1f} (extrapolated)")
xp = np.array([p[0] for p in piv]); lo = np.log10([p[1] for p in piv]); hi = np.log10([p[2] for p in piv])
for name, y in (("smallest pivot", lo), ("largest pivot", hi)):
    b = np.polyfit(xp, y, 1)
    print(f"{name}: D {xp.min():.2f}-{xp.max():.2f}, {10 ** np.polyval(b, xp.min()):.1e} -> {10 ** np.polyval(b, xp.max()):.1e}, growth {10 ** b[0]:.3f}x per unit D")
