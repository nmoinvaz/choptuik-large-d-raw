"""Domb-Sykes on the median Taylor coefficients a_k of a taylor log: r_k = a_k / a_(k-1), fitted as r_k = A + B/k over
the last pairs of k; the singularity is at e0 = 1/A with exponent alpha = -B/A - 1 for (1 - e/e0)^alpha."""
import re, sys
import mpmath as mp
mp.mp.dps = 40
for f in sys.argv[1:]:
    a = {}
    for line in open(f):
        m = re.match(r"  a_(\d+): median (\S+),", line)
        if m:
            a[int(m.group(1))] = mp.mpf(m.group(2))
    r = {k: a[k] / a[k - 1] for k in range(2, max(a) + 1)}
    out = []
    for k1, k2 in ((3, 4), (4, 5), (5, 6)):
        if k2 not in r:
            continue
        B = (r[k2] - r[k1]) / (mp.mpf(1) / k2 - mp.mpf(1) / k1)
        A = r[k2] - B / k2
        out.append(f"k {k1},{k2}: e0 {mp.nstr(1 / A, 4)}, alpha {mp.nstr(-B / A - 1, 3)}")
    print(f, "| ratios", ", ".join(f"{k}: {mp.nstr(v, 5)}" for k, v in r.items()), "|", "; ".join(out))
