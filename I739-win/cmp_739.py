#!/usr/bin/env python3
"""#739: Delta of the octo-double states against the quad-double ones, from the saved states.
usage: python cmp_739.py [--selftest]       (venv-t151 python, from this folder)
Delta of a state = the exact sum of the last entry of every part present (zh, zl, z2, z3 and z4 to z7), arb at 600 bits, printed to 40 digits.
Reads: the stored quad-double D 112.75 state (I726-win/L), ctl/base_pin13_D112.7500.npz (the control (a)), A/anm_pin13_D112.8750.npz and B/anm_pin13_D113.0000.npz when they exist.
--selftest: a planted eight-part value must come back to 40 digits and its two-part sum must differ."""
import os
import sys

import flint
import numpy as np

flint.ctx.prec = 600
arb = flint.arb
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
KEYS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
STATES = {"qd D 112.75 (I726-win/L)": os.path.join(RAW, "I726-win", "L", "anm_pin13_D112.7500.npz"),
          "ctl (octo-double polish of it)": os.path.join(HERE, "ctl", "base_pin13_D112.7500.npz"),
          "A (octo-double, D 112.875)": os.path.join(HERE, "A", "anm_pin13_D112.8750.npz"),
          "B (octo-double, D 113)": os.path.join(HERE, "B", "anm_pin13_D113.0000.npz")}


def delta(path, n=8):
    d = np.load(path, allow_pickle=True)
    s = arb(0)
    for k in KEYS[:n]:
        if k in d.files:
            s += arb(float(d[k][-1]))
    return s


def selftest():
    import tempfile
    import mpmath as mp
    mp.mp.dps = 160
    x = mp.pi / 2 + mp.e * mp.mpf(10) ** -37
    r, parts = x, []
    for _ in range(8):
        h = float(r)
        parts.append(h)
        r -= mp.mpf(h)
    with tempfile.TemporaryDirectory() as t:
        pth = os.path.join(t, "planted.npz")
        np.savez(pth, **{k: np.array([0.0, v]) for k, v in zip(KEYS, parts)})
        got, two = delta(pth).str(40, radius=False), delta(pth, 2).str(40, radius=False)
    want = mp.nstr(x, 40, strip_zeros=False)
    norm = lambda s: s.replace(".", "").lstrip("0")[:38]
    ok = norm(got) == norm(want) and norm(two) != norm(want)
    print(f"  planted eight-part value {want}: read {got}, two parts {two} {'ok' if ok else 'WRONG'}")
    print("selftest", "passed" if ok else "FAILED")
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    vals = {k: delta(p) for k, p in STATES.items() if os.path.exists(p)}
    for k, v in vals.items():
        print(f"Delta {k}: {v.str(40, radius=False)}")
    ref = vals["qd D 112.75 (I726-win/L)"]
    if "ctl (octo-double polish of it)" in vals:
        c = vals["ctl (octo-double polish of it)"]
        d = float((c - ref).mid())
        print(f"control (a): ctl - qd = {d:+.4e}   {'within' if abs(d) <= 1e-30 else 'OUTSIDE'} the 1e-30 bar")
    for k in ("A (octo-double, D 112.875)", "B (octo-double, D 113)"):
        if k in vals:
            print(f"{k}: Delta - qd D 112.75 = {float((vals[k] - ref).mid()):+.6e}")


if __name__ == "__main__":
    main()
