#!/usr/bin/env python3
"""make_branches.py: the two-branch picture of the roots near D 22.1 to 22.25 (flat F and steep S), from the reading files only (det-linear positions of the robust changes: crude at a 0.02 spacing, not enclosures).
F: the roots 0.545 (D 22.0), 0.4908 (22.125, the rescan), 0.4727 (22.15625), the upper root at D 22.1875, 22.21875, 22.25; S: the upper root of D 22.125 (high scan) and D 22.15625 (high scan), the lower root of D 22.1875 (mid scan), 22.21875 and 22.25 (low scan).
usage: make_branches.py | make_branches.py --selftest [--mutate=cross]  (planted two linear branches with a known crossing; the mutation puts a sign error in the offset and must fail)"""
import math, re, sys
L = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda"
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)

def det(folder):
    t = open("%s/%s/read_lower.txt" % (L, folder)).read()
    return [(float(m[0]), float(m[1]), m[2], float(m[3])) for m in re.findall(r"robust change \((-?[\d.]+), (-?[\d.]+)\), (.+?), det-linear (-?[\d.]+)", t)]

def slopes(T):
    ds = sorted(T); return [(a, b, (T[b] - T[a]) / (b - a)) for a, b in zip(ds, ds[1:])]

def crossing(F, S, a, b):
    """both branches linear between D a and D b: where they meet"""
    x = (F[a] - S[a]) / ((S[b] - S[a]) - (F[b] - F[a])) * (b - a)
    if MUT == "cross": x = (S[a] - F[a]) / ((S[b] - S[a]) - (F[b] - F[a])) * (b - a)      # a sign error in the offset: the planted crossing must then be missed
    return a + x, F[a] + (F[b] - F[a]) * x / (b - a)

def selftest():
    F = {0.0: 0.50, 1.0: 0.40}; S = {0.0: 0.80, 1.0: 0.20}
    d, l = crossing(F, S, 0.0, 1.0)         # F = 0.50 - 0.1 d, S = 0.80 - 0.6 d: meet at d = 0.6, lambda 0.44
    ok = abs(d - 0.6) < 1e-12 and abs(l - 0.44) < 1e-12
    print("planted: F 0.50 to 0.40, S 0.80 to 0.20 over D 0 to 1 meet at D %.4f, lambda %.4f (0.6, 0.44 wanted): %s" % (d, l, "PASS" if ok else "FAIL"))
    print("selftest:", "PASS" if ok else "FAIL"); return 0 if ok else 1

if __name__ == "__main__":
    if "--selftest" in sys.argv: sys.exit(selftest())
    F = {22.0: det("22.0")[0][3], 22.125: 0.490845, 22.15625: det("22.15625")[0][3], 22.1875: det("22.1875")[0][3], 22.21875: det("22.21875_full")[1][3], 22.25: det("22.25")[0][3]}
    S = {22.125: det("22.125_high")[0][3], 22.15625: det("22.15625_high")[0][3], 22.1875: det("22.1875_mid")[0][3], 22.21875: det("22.21875_full")[0][3], 22.25: det("22.25_low")[0][3]}
    for n, T in (("F (flat)", F), ("S (steep)", S)):
        print("**%s:** %s; slopes per unit D: %s" % (n, ", ".join("D %r %.4f" % (d, T[d]) for d in sorted(T)), ", ".join("%.2f" % s for _, _, s in slopes(T))))
    d, l = crossing(F, S, 22.15625, 22.1875)
    print("**Crossing** (both branches taken linear between D 22.15625 and D 22.1875): D %.4f, lambda %.4f; gap S minus F at the scanned D: %s" % (d, l, ", ".join("%r %+.4f" % (x, S[x] - F[x]) for x in sorted(S))))
    ds = [22.1875, 22.21875, 22.25]; v = [S[x] for x in ds]
    lag = lambda t: sum(v[i] * math.prod((t - ds[j]) / (ds[i] - ds[j]) for j in range(3) if j != i) for i in range(3))
    lo, hi = 22.25, 22.4
    for _ in range(60):
        m = (lo + hi) / 2
        if lag(m) > 0: lo = m
        else: hi = m
    print("**Zero of S by arithmetic on those positions (an extrapolation, not a result):** quadratic through the last three: D %.3f; linear from the last slope: D %.3f; F extrapolated linearly from its last slope (%.2f): D %.2f" % (
        lo, 22.25 + S[22.25] / (-(S[22.25] - S[22.21875]) / 0.03125), slopes(F)[-1][2], 22.25 + F[22.25] / -slopes(F)[-1][2]))
