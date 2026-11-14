#!/usr/bin/env python3
"""#760 (#712's check, the folder changed): each saved 24-order series (I760-dh370/repro/jet_pin3_D<D>.npz, meta norms and pivots) against #603's record of the step from that base
(I603-win2/chain_nsr/anm_run.jsonl, the record with D0 nearest): equal norms (of 25) and equal pivots, bit for bit. The control
(--control) compares each series with the record of the next base (the previous one for the last) instead, which must differ.
    python3 repro_check760.py RAW [--control]"""
import glob
import json
import os
import sys

import numpy as np

raw = sys.argv[1]
control = "--control" in sys.argv
recs = [json.loads(x) for x in open(os.path.join(raw, "I603-win2", "chain_nsr", "anm_run.jsonl"))]
recs.sort(key=lambda r: r["D0"])
ok = True
for jp in sorted(glob.glob(os.path.join(raw, "I760-dh370", "repro", "jet_pin3_D*.npz"))):
    m = json.loads(str(np.load(jp, allow_pickle=True)["meta"]))
    i = min(range(len(recs)), key=lambda j: abs(recs[j]["D0"] - m["D"]))
    if control:
        i = i + 1 if i + 1 < len(recs) else i - 1
    r = recs[i]
    eq = sum(a == b for a, b in zip(m["norms"], r["norms"]))
    pv = list(m["pivots"]) == list(r["pivots"])
    good = eq == len(r["norms"]) == len(m["norms"]) and pv
    print(f"D {m['D']:.4f} (record D0 {r['D0']:.4f}): norms equal {eq} of {len(r['norms'])}, pivots equal {pv}, N {m['N']} -> {'identical' if good else 'DIFFERS'}")
    ok = ok and good
if control:
    sys.exit(0 if not ok else 1)  # the control passes only if the comparison fails
sys.exit(0 if ok else 1)
