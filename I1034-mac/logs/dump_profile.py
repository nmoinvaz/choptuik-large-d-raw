"""exponent profiles of fastmul dumps: per file, per factor, per lane, the LS slope and the spread after the common slope"""
import sys, os, glob
import numpy as np

d = sys.argv[1]
for f in sorted(glob.glob(os.path.join(d, "*.bin")))[: int(sys.argv[2]) if len(sys.argv) > 2 else 9999]:
    v = np.fromfile(f, dtype="<f8")
    n, na, nb = int(v[0]), int(v[1]), int(v[2])
    c = v[3:].reshape(na + nb, 8, 8)  # coefficient, lane, part
    lead = c[:, :, 0]
    out = []
    for name, x in (("a", lead[:na]), ("b", lead[na:])):
        e = np.where(x != 0, np.floor(np.log2(np.abs(np.where(x != 0, x, 1.0)))) + 1, np.nan)
        slopes, spreads, zeros = [], [], int(np.sum(x == 0))
        for l in range(8):
            ok = ~np.isnan(e[:, l])
            i = np.arange(len(e))[ok]
            if len(i) < 2:
                slopes.append(0.0)
                spreads.append(0)
                continue
            p = np.polyfit(i, e[ok, l], 1)
            slopes.append(p[0])
            r = e[ok, l] - p[0] * i
            spreads.append(int(r.max() - r.min()))
        out.append(f"{name}: slope {np.min(slopes):+.2f}..{np.max(slopes):+.2f}, detrended spread {min(spreads)}..{max(spreads)} bits, zeros {zeros}")
    print(f"{os.path.basename(f):18} n {n:4}  " + " | ".join(out))
