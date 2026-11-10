#!/usr/bin/env python3
"""The planted state of #267: D 30's saved state (hp/data/states/up6_D30.0688.npz, M 32, kc 414) with its centre series
order lowered to kc 100. Its M 32 layout still passes the gate (centre 2.7e-18), and resampled to M 48 its centre
series is truncated at 2.6e-13, above SERIES_TAIL (1e-15).

    python3 plant.py WORKTREE OUT.npz
"""
import json
import sys

import numpy as np

src = sys.argv[1] + "/hp/data/states/up6_D30.0688.npz"
d = np.load(src)
meta = json.loads(str(d["meta"]))
assert meta["kc"] == 414 and meta["M"] == 32
meta = dict(meta, kc=100, planted="I267: up6_D30.0688.npz with kc 414 -> 100 (centre series truncated above 1e-15 at "
                                  "M 48)")
np.savez(sys.argv[2], zh=d["zh"], zl=d["zl"], meta=json.dumps(meta))
print(f"{sys.argv[2]}: {meta}")
