#!/usr/bin/env python3
"""#506: run hp/modecount_circle.py unchanged, with the double-double differentiation matrix handed to
modecount_cx.CSolver changed by one ulp in one entry (the high part dh; the low part is left as it is).

    python3 ulp_circle.py I J SHIFT -- <the arguments of hp/modecount_circle.py>

SHIFT is +1 or -1 (one ulp up or down with np.nextafter) or 0 (the matrix is passed as it is, which must reproduce
the plain run bit for bit). Prints the entry, its old and new value. Changes no repository file; the hook is the
module attribute modecount_cx.CSolver, which hp/modecount_common.py looks up when it builds the solver."""
import os
import runpy
import sys

import numpy as np

HP = os.environ.get("HP_DIR", os.path.expanduser("~/Source/choptuik-large-d/hp"))
sys.path.insert(0, HP)
sys.path.insert(0, os.path.join(HP, "modecount_cx", "build"))
import modecount_cx  # noqa: E402

i, j, shift = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
assert sys.argv[4] == "--" and shift in (-1, 0, 1)
rest = sys.argv[5:]
orig = modecount_cx.CSolver


def patched(M, nh, nl, dh, dl, ph, pl, *args, **kw):
    dh2 = np.array(dh, dtype=float, copy=True)
    old = dh2[i, j]
    if shift:
        dh2[i, j] = np.nextafter(old, np.inf if shift > 0 else -np.inf)
    changed = int(np.count_nonzero(dh2 != np.asarray(dh)))
    print(f"ulp_circle: dh[{i},{j}] {old!r} -> {dh2[i, j]!r} (shift {shift:+d}), entries changed {changed}", flush=True)
    return orig(M, nh, nl, dh2, dl, ph, pl, *args, **kw)


modecount_cx.CSolver = patched
script = os.path.join(HP, "modecount_circle.py")
sys.argv = [script] + rest
runpy.run_path(script, run_name="__main__")
