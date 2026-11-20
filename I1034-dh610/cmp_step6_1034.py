#!/usr/bin/env python3
"""cmp_step6_1034.py [--mutate]: the three chain steps' (series_split 0, 1, 2, from run1034_step6c.sh) saved arrays compared byte by byte, step 0 against steps 1 and 2: the accepted base
`anm_pin3_D238.0270.npz`, the series `jet_pin3_D237.5270.npz` and the prediction `pred_pin3_D238.0270.npz` (npz arrays; object arrays skipped). --mutate flips one byte of the step 1 array z3 in
memory first (the comparison of step 0 with step 1 must then report a difference), the check's control. Exit 0 when the comparison ran; prints per file the number of differing bytes per array."""
import glob
import os
import sys

import numpy as np

O = os.path.dirname(os.path.abspath(__file__))
mut = "--mutate" in sys.argv


def load(p):
    z = np.load(p, allow_pickle=True)
    return {k: z[k] for k in z.files}


def ndiff(a, b):
    if a.dtype == object or b.dtype == object or a.shape != b.shape:
        return None
    if a.ndim == 0:
        return int(a.tobytes() != b.tobytes())
    return int(np.sum(a.view(np.uint8).reshape(a.shape + (-1,)) != b.view(np.uint8).reshape(b.shape + (-1,))))


for pat in ("anm_pin3_D238.0270.npz", "jet_pin3_D237.5270.npz", "pred_pin3_D238.0270.npz"):
    fs = {s: f"{O}/step_s{s}_dmax300/{pat}" for s in (0, 1, 2)}
    if not all(os.path.exists(f) for f in fs.values()):
        print(pat, "missing")
        continue
    b = load(fs[0])
    for s in (1, 2):
        o = load(fs[s])
        if mut and s == 1 and "z3" in o:
            o["z3"] = o["z3"].copy()
            o["z3"].view(np.uint8).reshape(-1)[0] ^= 1
        res = {k: ndiff(b[k], o[k]) for k in b if k in o}
        nz = {k: v for k, v in res.items() if v}
        print(f"{pat}: step 0 vs step {s}{' (--mutate)' if mut and s == 1 else ''}: {len(res)} arrays, {len(nz)} differ (differing bytes): {nz}")
