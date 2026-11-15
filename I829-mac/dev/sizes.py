# plant sizes only: a least-squares fit of the measured Delta at the states in [259.3, 259.84] to the Puiseux form
import sys, glob
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-xf-829/hp")
import mpmath as mp, numpy as np
import lam_gauge as LG
mp.mp.dps = 50
RAW = "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad/raw-wt/I603-win2/chain_nsr"
pts = []
for p in sorted(glob.glob(RAW + "/anm_pin3_D*.npz")):
    parts, meta = LG.load(p)
    D = float(meta["D_str"])
    if D >= 259.3:
        pts.append((D, float(mp.fsum(mp.mpf(float(q[-1])) for q in parts))))
Ds = 259.9033
s = np.array([np.sqrt(Ds - D) for D, _ in pts]); y = np.array([v for _, v in pts])
for K in (5, 6, 7):
    A = np.vstack([s ** k for k in range(K + 1)]).T
    c = np.linalg.lstsq(A, y, rcond=None)[0]
    print(K, len(pts), " ".join("%+.4e" % x for x in c), "rms %.1e" % np.sqrt(np.mean((A @ c - y) ** 2)))
