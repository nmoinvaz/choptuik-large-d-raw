#!/usr/bin/env python3
"""#526: run hp/modecount_circle.py unchanged, with one input of modecount_cx.CSolver changed by SHIFT ulps.

    python3 ulp_circle.py dh I J SHIFT -- <the arguments of hp/modecount_circle.py>     entry [I, J] of the high part dh
    python3 ulp_circle.py ph I SHIFT -- ...                                              entry I of the phase weights ph
    python3 ulp_circle.py seg S K SHIFT -- ...                                           boundary K (interior) of segment S of the plan
    python3 ulp_circle.py show -- ...                                                    print the shapes and values and stop

SHIFT is an integer from -4 to 4 (that many ulps up or down, by repeated np.nextafter) or 0 (the input is passed as it
is, which must reproduce the plain run bit for bit). The dh branch is #520's. Changes no repository file; the hook is the
module attribute modecount_cx.CSolver, which hp/modecount_common.py looks up when it builds the solver."""
import os
import runpy
import sys

import numpy as np

HP = os.environ.get("HP_DIR", os.path.expanduser("~/Source/choptuik-large-d/hp"))
sys.path.insert(0, HP)
sys.path.insert(0, os.path.join(HP, "modecount_cx", "build"))
import modecount_cx  # noqa: E402

kind = sys.argv[1]
k = sys.argv.index("--")
spec, rest = [int(x) for x in sys.argv[2:k]], sys.argv[k + 1:]
shift = spec[-1] if spec else 0
assert kind in ("dh", "ph", "seg", "show") and abs(shift) <= 4
orig = modecount_cx.CSolver


def bump(a, shift):
    for _ in range(abs(shift)):
        a = np.nextafter(a, np.inf if shift > 0 else -np.inf)
    return a


def patched(M, nh, nl, dh, dl, ph, pl, nodes, segs, *args, **kw):
    if kind == "show":
        print(f"ulp_circle show: dh {np.shape(dh)}, ph {np.shape(ph)} {np.asarray(ph).dtype}, segments {len(segs)}", flush=True)
        print("  ph[:6]", np.asarray(ph).ravel()[:6], flush=True)
        for s, g in enumerate(segs):
            print(f"  seg {s}: {len(g)} boundaries, first {g[:4]}, last {g[-2:]}", flush=True)
        sys.exit(0)
    dh2, ph2, segs2 = dh, ph, segs
    if kind == "dh":
        i, j = spec[0], spec[1]
        dh2 = np.array(dh, dtype=float, copy=True)
        old, dh2[i, j] = dh2[i, j], bump(dh2[i, j], shift)
        new = dh2[i, j]
        what = f"dh[{i},{j}]"
    elif kind == "ph":
        i = spec[0]
        ph2 = np.array(ph, dtype=float, copy=True)
        old, ph2[i] = ph2[i], bump(ph2[i], shift)
        new = ph2[i]
        what = f"ph[{i}]"
    else:
        s, kk = spec[0], spec[1]
        segs2 = [[float(x) for x in g] for g in segs]
        assert 0 < kk < len(segs2[s]) - 1, "interior boundaries only"
        old = segs2[s][kk]
        segs2[s][kk] = float(bump(np.float64(old), shift))
        new = segs2[s][kk]
        what = f"seg[{s}][{kk}]"
    print(f"ulp_circle: {what} {old!r} -> {new!r} (shift {shift:+d}), ulps {(new - old) / np.spacing(abs(old)):+.0f}", flush=True)
    return orig(M, nh, nl, dh2, dl, ph2, pl, nodes, segs2, *args, **kw)


modecount_cx.CSolver = patched
script = os.path.join(HP, "modecount_circle.py")
sys.argv = [script] + rest
runpy.run_path(script, run_name="__main__")
