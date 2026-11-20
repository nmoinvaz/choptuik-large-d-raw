"""#1021: how far one representable step of the harmonics moves each residual, from a hier_nb.py --verbose=2 log.
Reads the start x (A, w, B3, C3, B5, C5) and the first "K by level" table (max |d r_l / d x_nu|), and prints
K[l][nu] x spacing(max(|B_nu|, |C_nu|)), the residual change per double step of the larger harmonic of x_nu, beside
the level's first noise-floor stop |g| (if any). The step is that of the harmonic with the larger spacing, so the
product is the change per step only when K's largest entry is with respect to it; it is an order of magnitude.
    python k_ulp.py LOG [LOG ...]"""
import re, sys
import numpy as np

for f in sys.argv[1:]:
    t = open(f).read()
    x = [float(v) for v in re.search(r"start x \[([^\]]+)\]", t).group(1).split(",")]
    xi = re.search(r"M 5, xi1 ([0-9.]+)", t).group(1)
    rows = re.findall(r"^\s+l (\d): ([0-9.e+-]+)\s+([0-9.e+-]+)\s+([0-9.e+-]+)$", t[t.index("K by level"):], re.M)[:3]
    sp = {3: np.spacing(max(abs(x[2]), abs(x[3]))), 5: np.spacing(max(abs(x[4]), abs(x[5])))}
    stops = {int(l): float(g) for l, g in re.findall(r"level (\d) \([a-z]+\): stop at \|g\| ([0-9.e+-]+) \(noise floor\)", t)[::-1]}
    print(f"{'/'.join(f.split('/')[-3:])} (xi1 {xi}): spacing of x_3 {sp[3]:.2g}, of x_5 {sp[5]:.2g}")
    for l, k1, k3, k5 in rows:
        l = int(l)
        print(f"  r_{l}: per step of x_3 {float(k3) * sp[3]:.2g}, of x_5 {float(k5) * sp[5]:.2g}"
              + (f"; first noise-floor stop of level {l} at |g| {stops[l]:.3g}" if l in stops else ""))
