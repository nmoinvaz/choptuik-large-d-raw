#!/usr/bin/env python3
"""#640 step 1, the planted control on T81's full-system state at D 73.0 (kfreeze 13): the release from the perturbed start must equal the unperturbed
release (Delta within 1e-25, p1's harmonics 5-13 coefficients within 1e-20); with --it_max=0 (no release) the same comparison must fail.
Usage: python3 compare640.py   (reads control_unperturbed/, control_perturbed/, control_noreleas/ jsonl records). Exit 0 when the control passes and
its counter-control fails as it must."""
import json, os, sys
import mpmath as mp
mp.mp.dps = 60
here = os.path.dirname(os.path.abspath(__file__))
def rec(d):
    f = os.path.join(here, d, "release.jsonl")
    return json.loads(open(f).readlines()[-1])
a, b, c = rec("control_unperturbed"), rec("control_perturbed"), rec("control_noreleas")
def cmp(x, y):
    dd = abs(mp.mpf(x["Delta_full"]) - mp.mpf(y["Delta_full"]))
    cc = max(abs(p - q) for u, v in zip(x["coeffs_end"], y["coeffs_end"]) for p, q in zip(u, v))
    return dd, cc
for lab, r in (("unperturbed", a), ("perturbed 1e-10", b), ("perturbed, --it_max=0", c)):
    print(f"{lab}: converged {r['converged']} ok {r['ok']} steps {r['steps']} |F| start {r['F_start']:.2e} end {r['F']:.2e}; Delta_full - Delta_start = {r['diff']:+.3e}")
d1, c1 = cmp(a, b)
d2, c2 = cmp(a, c)
p1 = d1 <= mp.mpf("1e-25") and c1 <= 1e-20
p2 = d2 <= mp.mpf("1e-25") and c2 <= 1e-20
print(f"perturbed release against unperturbed: |dDelta| {mp.nstr(d1, 3)}, max |dcoeff| {c1:.2e}: {'pass' if p1 else 'FAIL'} (needs 1e-25, 1e-20)")
print(f"no-release run against unperturbed: |dDelta| {mp.nstr(d2, 3)}, max |dcoeff| {c2:.2e}: {'fails as it must' if not p2 else 'DOES NOT FAIL (the control is blind)'}")
sys.exit(0 if (p1 and not p2) else 1)
