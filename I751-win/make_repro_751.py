#!/usr/bin/env python3
"""#751 (b): the repeat of one shifted node from a different start state, as #741's R1.
usage: python make_repro_751.py X            (X in A..F; venv-t151 python, from this folder; writes states/R_X.npz)
       python make_repro_751.py --selftest
R_X: the arrays zh, zl, z2, z3 of #710's A1 state (I710-win/A1, D 99.875, converged on its own plan, differing from cont3's by up to 1e-17 per entry) with the meta of the state N<X> (cont3's meta, node X shifted by +1e-3).
The check after the write: the arrays equal A1's bit for bit, the meta equals N<X>'s exactly, and the arrays DIFFER from cont3's.
--selftest: planted copies with an array entry changed, a changed meta key, cont3's own arrays must each be flagged, and the right copy must pass."""
import glob
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
KEYS = ("zh", "zl", "z2", "z3")
CONT3 = "I682-win/cont3/anm_pin13_D99.8750.npz"
A1 = "I710-win/A1/anm_pin13_D99.8750.npz"


def load(path):
    d = np.load(path, allow_pickle=False)
    return {k: np.array(d[k]) for k in KEYS}, json.loads(str(d["meta"]))


def check(src, shifted, cont3, new):
    bad = []
    for k in KEYS:
        if new[0][k].tobytes() != src[0][k].tobytes():
            bad.append(f"array {k} is not A1's")
    if new[1] != shifted[1]:
        bad.append("meta differs from the shifted state's")
    if all(new[0][k].tobytes() == cont3[0][k].tobytes() for k in KEYS):
        bad.append("the arrays are cont3's, not a different start")
    return bad


def selftest():
    src = load(os.path.join(RAW, A1))
    sh = load(sorted(glob.glob(os.path.join(HERE, "states", "NA_seg*_shift1e-3.npz")))[0])
    c3 = load(os.path.join(RAW, CONT3))
    ok0 = not check(src, sh, c3, (dict(src[0]), dict(sh[1])))
    a2 = dict(src[0])
    a2["zh"] = src[0]["zh"].copy()
    a2["zh"][3] = np.nextafter(a2["zh"][3], np.inf)
    b1 = check(src, sh, c3, (a2, dict(sh[1])))
    b2 = check(src, sh, c3, (dict(src[0]), dict(sh[1], a=0.5)))
    b3 = check(src, sh, c3, (dict(c3[0]), dict(sh[1])))
    for label, good in (("the right copy passes", ok0), ("one array entry changed is flagged", bool(b1)), ("a changed meta key is flagged", bool(b2)), ("cont3's own arrays are flagged", bool(b3))):
        print(f"  {label}: {'ok' if good else 'WRONG'}")
    n = ok0 + bool(b1) + bool(b2) + bool(b3)
    print("selftest", "passed" if n == 4 else "FAILED")
    return 0 if n == 4 else 1


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    x = sys.argv[1]
    found = glob.glob(os.path.join(HERE, "states", f"N{x}_seg*_shift1e-3.npz"))
    if x not in "ABCDEF" or len(found) != 1:
        raise SystemExit(f"node {x}: expected one state N{x}_seg*_shift1e-3.npz, found {found}")
    src = load(os.path.join(RAW, A1))
    sh = load(found[0])
    c3 = load(os.path.join(RAW, CONT3))
    path = os.path.join(HERE, "states", f"R_{x}.npz")
    np.savez(path, zh=src[0]["zh"], zl=src[0]["zl"], z2=src[0]["z2"], z3=src[0]["z3"], meta=json.dumps(sh[1]))
    bad = check(src, sh, c3, load(path))
    print(f"R_{x}: arrays of {A1} with the meta of {os.path.basename(found[0])} -> states/R_{x}.npz; problems {bad}")
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
