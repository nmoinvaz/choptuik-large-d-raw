#!/usr/bin/env python3
"""xcheck_job6.py [--mutate]: job 6's consistency checks, bound fixed before the run: two converged solves of the same equations at the same D must agree in Delta to 1e-30
(their states solve to max|F| 1e-72 or below, and the weakest direction's pivot is 4e-25, so the expected gap is below 1e-47). From xc_<kind>_<D>.json, written by exact_recip_check.py delta:
  off  job 4's flag-off state (cont241_r0/) against job 6's flag-off state (job6_r0/): must agree to 1e-30;
  on   job 5's flag-on polish (resolve<D>_r1/) against job 6's flag-on state (job6_r1/): must agree to 1e-30;
  ctl  job 6's flag-off state against job 5's flag-on polish: the flag's change, about 3e-13, so it must exceed 1e-30 (the control: the check can fail).
Exit 1 when an expectation is violated; --mutate reverses every expectation and must exit 1."""
import glob
import json
import os
import re
import sys

H = os.path.dirname(os.path.abspath(__file__)) + "/"
BOUND = 1e-30
mut = "--mutate" in sys.argv
ok, n = True, 0
for p in sorted(glob.glob(H + "xc_*_*.json")):
    m = re.match(r"xc_(off|on|ctl)_(\S+)\.json", os.path.basename(p))
    if not m:
        continue
    kind, D = m.groups()
    ch = abs(json.load(open(p))["change"])
    want_small = kind != "ctl"
    good = (ch <= BOUND) == want_small
    if mut:
        good = not good
    ok &= good
    n += 1
    print(f"  {kind} D {D}: |change| {ch:.3e}, must be {'at or below' if want_small else 'above'} {BOUND:.0e}{' (--mutate: reversed)' if mut else ''}: {'ok' if good else 'FAIL'}")
if n == 0:
    print("no xc_*.json files")
    sys.exit(2)
print("xcheck", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
