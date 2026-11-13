#!/usr/bin/env python3
"""#727: Delta of the three D 99.875 full-system states and their pairwise differences.
usage: python cmp_727.py [--selftest]        (venv-t151 python, from this folder; reads the three STATES and prints Delta in arb at 400 bits)
Delta of a state = the sum of the last entry of each of the four parts zh, zl, z2, z3. Pass a polished state per name as NAME=path to compare those instead of the starts.
--selftest: a planted equal pair must read 0 and a planted pair displaced by 2e-25 must show 2e-25."""
import itertools
import os
import sys

import flint
import numpy as np

flint.ctx.prec = 400
arb = flint.arb
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
STATES = {"cont3": "I682-win/cont3/anm_pin13_D99.8750.npz", "A1": "I710-win/A1/anm_pin13_D99.8750.npz", "X2": "I725-win/X2/anm_pin13_D99.8750.npz"}


def delta(path):
    d = np.load(path, allow_pickle=True)
    s = arb(0)
    for k in ("zh", "zl", "z2", "z3"):
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
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
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
