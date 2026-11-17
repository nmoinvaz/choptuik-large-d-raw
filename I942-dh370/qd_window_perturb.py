"""#942 control: hp/qd_window.py (unchanged) with one random entry of the start raised by 1e-60 of itself.

    python qd_window_perturb.py SEED INFO.json QD_WINDOW_ARGS...

load_q is wrapped before qd_window imports it. The entry is drawn from the nonzero ones of the leading part and the
1e-60 relative step goes into the last part (a double cannot hold it in the leading one). INFO.json records it."""
import json
import os
import sys

import numpy as np

HP = "/home/nathan/Source/choptuik-large-d-935/hp"
sys.path.insert(0, HP)
import hpkernel.driver as drv  # noqa: E402

seed, info, rest = int(sys.argv[1]), sys.argv[2], sys.argv[3:]
_load = drv.load_q


def load_q(path):
    z, m = _load(path)
    z = [np.array(p) for p in z]
    i = int(np.random.default_rng(seed).choice(np.flatnonzero(z[0])))
    d = 1e-60 * z[0][i]
    with open(info, "w") as f:
        json.dump(dict(seed=seed, index=i, z0=float(z[0][i]), z3_before=float(z[3][i]), rel=1e-60, added=float(d)), f)
    z[3][i] += d
    return tuple(z), m


drv.load_q = load_q
sys.argv = [os.path.join(HP, "qd_window.py")] + rest
import qd_window  # noqa: E402

sys.exit(qd_window.main())
