#!/usr/bin/env python3
"""compare_x.py [--mutate=delta|root] : the k_c 143 state of kc143_d23125x (regridded from k_c 127) against the regridded-from-k_c 135 state of kc143_d23125 (t5's order, #1025 comment 7213649039):
Delta, lam_gauge, |F|, steps, psi-constraint, wall; t5's bar on the state (a Delta difference above 1e-6 is a different state, whatever the root says) and, when point_summary.txt exists, t5's bars on the root
(|root - (-0.024495)| <= 1e-3 reproduced; >= 3e-3 path-dependent; between: as measured). Every number from the files. --mutate=delta adds 2e-6 to the new Delta (the state verdict must flip), --mutate=root adds 0.004 to the root
(the root verdict must flip). Arithmetic on the files, not a result beyond what t5's bars say."""
import json, os, re, sys
R = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/"
rd = lambda p: [json.loads(l) for l in open(p) if l.strip()][-1]
new = rd(R + "kc143_d23125x/in/l1kc143macm3d23125x.jsonl"); ref = rd(R + "kc143_d23125/in/l1kc143macm3d23125.jsonl"); src = rd(R + "kc143_d23125x/in/l1kc127Lmacm3.jsonl")
if "--mutate=delta" in sys.argv: new = dict(new, Delta=new["Delta"] + 2e-6)
dD = new["Delta"] - ref["Delta"]
print("regridded from k_c 127 (kc143_d23125x) against regridded from k_c 135 (kc143_d23125), the same D 23.125, k_c 143:")
print("  Delta      %.12f  %.12f  difference %+.3e (t5's bar 1e-6: %s; R0's solve scatter 4.2e-7: %.2f times)" % (new["Delta"], ref["Delta"], dD, "a DIFFERENT STATE" if abs(dD) > 1e-6 else "the same state", abs(dD) / 4.2e-7))
print("  lam_gauge  %.12f  %.12f  difference %+.3e (k_c 135 -> 143 in kc143_d23125: %+.3e)" % (new["lam_gauge"], ref["lam_gauge"], new["lam_gauge"] - ref["lam_gauge"], ref["lam_gauge"] - rd(R + "kc143_d23125/in/l1kc135macm3d23125.jsonl")["lam_gauge"]))
print("  |F|        %.4e  %.4e  (below 5e-10: %s)" % (new["F"], ref["F"], new["F"] < 5e-10))
print("  steps      %d  %d  difference %+d" % (new["steps"], ref["steps"], new["steps"] - ref["steps"]))
print("  psi-constraint %.4e  %.4e  ratio %.4f" % (new["constraint"], ref["constraint"], new["constraint"] / ref["constraint"]))
print("  F_start %.3e  %.3e;  ell_refine seconds %s  %s;  source (k_c 127): Delta %.12f, lam_gauge %.12f, steps %d, constraint %.4e; Delta shift from the source %+.4e (by the chain %+.4e)" % (
    new["F_start"], ref["F_start"], new.get("seconds"), ref.get("seconds"), src["Delta"], src["lam_gauge"], src["steps"], src["constraint"], new["Delta"] - src["Delta"], ref["Delta"] - src["Delta"]))
ps = R + "kc143_d23125x/point_summary.txt"
if os.path.exists(ps):
    t = open(ps).read(); m = re.search(r"secant root bracket \[(\S+), (\S+)\], width (\S+), signs.*det-linear root (\S+);", t)
    lo, hi, root = float(m.group(1).rstrip(",")), float(m.group(2).rstrip(",")), float(m.group(4))
    if "--mutate=root" in sys.argv: root += 0.004; lo += 0.004; hi += 0.004
    d = root + 0.024495; rr = -0.02449537
    verdict = "REPRODUCED (within 1e-3): the state is reproduced, the doubled step is real" if abs(d) <= 1e-3 else ("PATH-DEPENDENT (3e-3 or more): two k_c 143 states, the D 23.125 point is withdrawn until understood" if abs(d) >= 3e-3 else "BETWEEN (1e-3 to 3e-3): as measured")
    print("root %+.8f, robust bracket [%.8f, %.8f]; minus t5's -0.024495: %+.3e; minus the kc143_d23125 root %+.8f: %+.3e; the bar: %s" % (root, lo, hi, d, rr, root - rr, verdict))
else:
    print("(no point_summary.txt yet: the root bars are scored when the secant has ended)")
