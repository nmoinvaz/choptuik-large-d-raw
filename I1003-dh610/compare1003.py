#!/usr/bin/env python3
"""compare1003.py PILOT.json REF.json [--n 13] [--tol 1e-19] [--mutate sigma7|omega]: sigma_0..sigma_{n-1} of the pilot against the reference's, relative, from
the files' 'sigma_str' (20 significant digits each, amp_flint_par.py line 688: the 1e-30 of the issue is not reachable from these files) and 'sigma' (doubles).
Pass, fixed before the run: every real and imaginary part's relative difference |a - b| / |b| <= tol over the larger of the pair's moduli, and the doubles equal.
Controls (the run must fail): --mutate sigma7 scales the reference's sigma_7 by 1 + 1e-15, --mutate omega reads the omega 0.99 file instead of the reference.
Exit 1 on failure."""
import json
import sys
import mpmath as mp

mp.mp.dps = 40
a = sys.argv[1:]
pil, ref = json.load(open(a[0])), json.load(open(a[1]))
n = int(a[a.index("--n") + 1]) if "--n" in a else 13
tol = mp.mpf(a[a.index("--tol") + 1]) if "--tol" in a else mp.mpf("1e-19")
mut = a[a.index("--mutate") + 1] if "--mutate" in a else ""
if mut == "omega":
    ref = json.load(open(a[1].replace("w1.0000", "w0.9900")))
rs = [[mp.mpf(x) for x in p] for p in ref["sigma_str"]]
if mut == "sigma7":
    rs[7] = [x * (1 + mp.mpf("1e-15")) for x in rs[7]]
worst, bad = mp.mpf(0), []
for k in range(n):
    ps = [mp.mpf(x) for x in pil["sigma_str"][k]]
    mod = max(mp.sqrt(rs[k][0] ** 2 + rs[k][1] ** 2), mp.sqrt(ps[0] ** 2 + ps[1] ** 2))
    d = max(abs(ps[0] - rs[k][0]), abs(ps[1] - rs[k][1])) / mod if mod else mp.mpf(0)
    eq = pil["sigma"][k] == ref["sigma"][k]
    worst = max(worst, d)
    if d > tol or (not eq and not mut):
        bad.append((k, mp.nstr(d, 3), eq))
    print(f"sigma_{k}: max relative difference of re, im over the larger modulus {mp.nstr(d, 3)}, doubles equal {eq}")
ok = not bad
print(f"{'PASS' if ok else 'FAIL'}: sigma_0..sigma_{n - 1} against the reference, worst {mp.nstr(worst, 3)}, tol {mp.nstr(tol, 3)}, bad {bad}" + (f" (control {mut})" if mut else ""))
sys.exit(0 if ok else 1)
