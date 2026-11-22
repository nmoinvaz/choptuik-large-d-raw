#!/usr/bin/env python3
"""read997c.py plants [--mutate] | read SERIES.npz LOG: #997's readings at D0 3.04315 with hp/series_singularity.py's ratio fit (ratios r_k = Delta_k / Delta_{k-1} over the window k = 2..K, r_k = a + b/k, h* = 1/a, radius |h*|),
K being the last order of the converged run (orders 1..K all converged in the anm_lowd.py log). The coordinator's readings: a radius of 0.03 or more: the closing is NOT a singularity of Delta; 0.001 or less: it IS; between: no reading.
plants (run before the data, criteria fixed here): planted series (series_singularity.planted_series, mu 0.7, the regular part and the confluent term of its P1 to P3) at D0 3.04315 with D* = 3.000 (true radius 0.04315) and D* = 3.04312 (true radius 3e-5), N 8,
for every K from 4 to 8: the 3.000 plant must read 'not a singularity' and the 3.04312 plant 'a singularity', each for every K (three ratios or more); --mutate raises the not-a-singularity bar to 0.5, which the 3.000 plant must then fail (exit 1).
read: prints the fit for the window 2..K and 3..K (K at least 4: three ratios; fewer: no reading), with the radius, D*, mu, the fit's rms residual and the reading. Exit 0 when the plants pass (read: always 0)."""
import re
import sys

import numpy as np

sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-997c/hp")
import series_singularity as ss  # noqa: E402

D0 = 3.04315


def classify(radius, bar=0.03):
    return "NOT a singularity (radius >= 0.03)" if radius >= bar else ("a SINGULARITY (radius <= 0.001)" if radius <= 0.001 else "no reading (between 0.001 and 0.03)")


def window_fit(dk, k1, K):
    h, mu, res = ss.fit(dk, k1, K)
    return abs(h), h, mu, res


def plants(mutate):
    bar = 0.5 if mutate else 0.03
    ok = True
    for Dstar, want in ((3.000, "NOT"), (3.04312, "SINGULARITY")):
        dk = ss.planted_series(Dstar, 0.7, D0, N=8)
        for K in range(4, 9):
            r, h, mu, res = window_fit(dk, 2, K)
            c = classify(r, bar)
            good = want in c
            ok &= good
            print(f"  plant D* {Dstar}, orders 2..{K}: radius {r:.3e} (true {abs(D0 - Dstar):.3e}), D* read {D0 + h:.6f}, mu {mu:.2f}, residual {res:.1e}: {c}: {'ok' if good else 'FAIL'}")
    print("plants", "PASS" if ok else "FAIL")
    return ok


def converged_K(log):
    o = {int(m.group(1)): m.group(5) == "True" for m in re.finditer(r"^  z_(\d+): \|z\| (\S+), \|rhs\| (\S+), (\d+) products, converged (True|False)", open(log).read(), re.M)}
    K = 0
    while o.get(K + 1):
        K += 1
    return K, o


def read(series, log):
    d0, dk = ss.coeffs(series)
    K, o = converged_K(log)
    print(f"series {series.split('/')[-1]}: D0 {d0}, {len(dk) - 1} orders in the file, converged orders 1..{K} (log), Delta_k: " + ", ".join(f"{x:.6e}" for x in dk[:K + 1]))
    if K < 4:
        print(f"no reading: {K} converged orders, three ratios need K >= 4")
        return
    for k1 in (2, 3):
        if K - k1 + 1 < 3:
            continue
        r, h, mu, res = window_fit(dk, k1, K)
        print(f"  window {k1}..{K}: radius {r:.4e}, h* {h:+.4e}, D* {d0 + h:.6f}, mu {mu:.2f}, residual {res:.1e}: {classify(r)}")
    print("ratios r_k:", ", ".join(f"{dk[k] / dk[k - 1]:+.4e}" for k in range(2, K + 1)))


if __name__ == "__main__":
    if sys.argv[1] == "plants":
        sys.exit(0 if plants("--mutate" in sys.argv) else 1)
    read(sys.argv[2], sys.argv[3])
