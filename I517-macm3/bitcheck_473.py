#!/usr/bin/env python3
"""Bit check of a rebuilt modecount_cx against #473's cached determinants (the coordinator's check before #517 at M 80).

    cd <checkout>/hp && python3 <raw>/I517-macm3/bitcheck_473.py <raw>/I473-macm3/data/modecount_D30.0688_M64_evals.jsonl

Sets up the D 30.0688 M 64 state as #473 did (hp/data/states/up6_D30.0688.npz, --M=64 --kf=none --fmax=1e-15, one thread;
the saved re-converged state hp/data/modecount_state_D30.0688_M64.npz is loaded, sha256 92f49438...), evaluates det M at four
points of #473's cache with st.det and compares all four numbers (ln|det|, arg, pmin, pmax) with the cached ones for equality.
Control: det at the first point moved by one ulp of lambda must differ from the cached value, else the comparison cannot
fail. Exit 1 on any mismatch or if the control does not differ.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.getcwd())
from modecount_common import setup  # noqa: E402

cache = {}
for line in open(sys.argv[1]):
    r = json.loads(line)
    cache[(r["re"], r["im"])] = r
points = [(0.124, 0.0), (1.0, 0.0), (6.182, 0.533123594726121), (6.182, 1.5993707841783633)]
for p in points:
    assert p in cache, p
st = setup("data/states/up6_D30.0688.npz", M=64, threads=1, kf=None, fmax=1e-15)
ok = True
for p in points:
    got = tuple(st.det(p[0], p[1]))
    ref = cache[p]
    want = (ref["lnabs"], ref["arg"], ref["pmin"], ref["pmax"])
    same = got == want
    ok &= same
    print(f"lambda {p[0]!r} {p[1]!r}: {'identical' if same else 'DIFFERENT'}  got {got}  cached {want}", flush=True)
p = points[0]
alt = tuple(st.det(float(np.nextafter(p[0], np.inf)), p[1]))
ref = cache[p]
differs = alt != (ref["lnabs"], ref["arg"], ref["pmin"], ref["pmax"])
print(f"control, lambda one ulp up from {p[0]!r}: {'differs from the cached value, as it must' if differs else 'EQUAL to the cached value, the check cannot fail'}  {alt}", flush=True)
ok &= differs
print("bitcheck", "pass" if ok else "FAIL", flush=True)
sys.exit(0 if ok else 1)
