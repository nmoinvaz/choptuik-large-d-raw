#!/usr/bin/env python3
"""#727: Delta of the three D 99.875 full-system states and their pairwise differences.
usage: python cmp_727.py [--selftest]        (venv-t151 python, from this folder; reads the three STATES and prints Delta in arb at 600 bits)
       python cmp_727.py --od                (the polished bases pilot2/, A1c/, X2c/ base_pin13_D99.8750.npz, eight parts, Delta to 40 digits, against cont3's stored quad-double Delta)
Delta of a state = the exact sum of the last entry of every part present (zh, zl, z2, z3 and z4 to z7 of an octo-double state). Pass NAME=path to compare other states.
--selftest: a planted equal pair must read 0, a planted pair displaced by 2e-25 must show 2e-25, and a planted eight-part value must come back to 40 digits (the two-part sum must differ)."""
import itertools
import os
import sys

import flint
import numpy as np

flint.ctx.prec = 600
arb = flint.arb
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
STATES = {"cont3": "I682-win/cont3/anm_pin13_D99.8750.npz", "A1": "I710-win/A1/anm_pin13_D99.8750.npz", "X2": "I725-win/X2/anm_pin13_D99.8750.npz"}


def delta(path):
    d = np.load(path, allow_pickle=True)
    s = arb(0)
    for k in ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7"):
        if k in d.files:
            s += arb(float(d[k][-1]))
    return s


def parts_sum(path, n):
    """the sum of the first n parts only (the control: two parts must differ from eight)"""
    d = np.load(path, allow_pickle=True)
    s = arb(0)
    for k in ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")[:n]:
        if k in d.files:
            s += arb(float(d[k][-1]))
    return s


def selftest():
    a = arb("1.74515002816449925294435272784")
    bad = 0
    same = float((a - a).mid())
    print(f"  planted equal pair: difference {same:.3e} {'ok' if same == 0 else 'WRONG'}")
    bad += same != 0
    shown = float(((a + arb("2e-25")) - a).mid())
    ok = abs(shown - 2e-25) < 1e-33
    print(f"  planted pair displaced by 2e-25: difference {shown:.4e} {'ok' if ok else 'WRONG'}")
    bad += not ok
    # a planted eight-part value: 150 digits split greedily into doubles, written as an octo-double state file
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
        np.savez(pth, **{k: np.array([0.0, v]) for k, v in zip(("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7"), parts)})
        got = delta(pth).str(40, radius=False)
        two = parts_sum(pth, 2).str(40, radius=False)
    want = mp.nstr(x, 40, strip_zeros=False)
    ok = got.replace(".", "").lstrip("0")[:38] == want.replace(".", "").lstrip("0")[:38] and two.replace(".", "")[:38] != want.replace(".", "")[:38]
    print(f"  planted eight-part value {want}: read {got}, two parts {two} {'ok' if ok else 'WRONG'}")
    bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--od" in sys.argv:
        od = {k: os.path.join(HERE, k, "base_pin13_D99.8750.npz") for k in ("pilot2", "A1c", "X2c") if os.path.exists(os.path.join(HERE, k, "base_pin13_D99.8750.npz"))}
        q = delta(os.path.join(RAW, STATES["cont3"]))
        vals = {k: delta(p) for k, p in od.items()}
        print(f"Delta cont3 stored (quad-double): {q.str(40, radius=False)}")
        for k, v in vals.items():
            print(f"Delta {k} (octo-double, eight parts): {v.str(40, radius=False)}")
        if "pilot2" in vals:
            print(f"pilot2 - cont3 stored: {float((vals['pilot2'] - q).mid()):+.4e}")
        names = list(vals)
        diffs = []
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                d = float((vals[a] - vals[b]).mid())
                diffs.append(abs(d))
                print(f"  {a} - {b}: {d:+.4e}")
        if diffs:
            print(f"largest |difference|: {max(diffs):.4e}")
        return
    paths = {k: os.path.join(RAW, v) for k, v in STATES.items()}
    for arg in sys.argv[1:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            paths[k] = v
    vals = {k: delta(p) for k, p in paths.items()}
    for k, v in vals.items():
        print(f"Delta {k}: {v.str(30, radius=False)}   ({paths[k]})")
    print("pairwise differences:")
    diffs = []
    for a, b in itertools.combinations(vals, 2):
        d = float((vals[a] - vals[b]).mid())
        diffs.append(abs(d))
        print(f"  {a} - {b}: {d:+.4e}")
    print(f"largest |difference|: {max(diffs):.4e}")


if __name__ == "__main__":
    main()
