#!/usr/bin/env python3
"""#611: a start state at D 54.996085 by linear interpolation in D of hp's two up10 states (D 54.041398 and 55.035148).
usage: python make_interp.py [D]    (from this folder; writes interp_D<D>.npz, in the format of the up10 states; D defaults to 54.996085;
D = 54.041398 is the control, w = 0, which must reproduce the state of the lower end up to the dd rounding of zh + zl)
Interpolated in double precision on zh (zl = 0); scan_qd.py then polishes it in quad-double at its own D (no step in D)."""
import json
import os
import sys

import numpy as np

HP = r"C:\Users\nathan\Source\choptuik-i611\hp\data\states"
b = np.load(os.path.join(HP, "up10_D54.0414.npz"), allow_pickle=True)
a = np.load(os.path.join(HP, "up10_D55.0351.npz"), allow_pickle=True)
mb, ma = json.loads(str(b["meta"])), json.loads(str(a["meta"]))
assert {k: v for k, v in mb.items() if k != "D"} == {k: v for k, v in ma.items() if k != "D"}
Db, Da = mb["D"], ma["D"]
Dt = float(sys.argv[1]) if len(sys.argv) > 1 else 54.996085
w = (Dt - Db) / (Da - Db)
zh = (1 - w) * (b["zh"] + b["zl"]) + w * (a["zh"] + a["zl"])
meta = dict(mb, D=Dt)
np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"interp_D{Dt:.6f}.npz"), zh=zh, zl=np.zeros_like(zh), meta=json.dumps(meta))
print(f"w = {w:.9f}, |zb - za|_max = {np.max(np.abs(b['zh'] - a['zh'])):.3e}, meta {meta}")
