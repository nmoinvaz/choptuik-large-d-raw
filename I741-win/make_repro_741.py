#!/usr/bin/env python3
"""#741 control: the shifted plans of S1 and S3 on a DIFFERENT start state, to see whether the polished Delta of a plan reproduces.
usage: python make_repro_741.py [--selftest]       (venv-t151 python, from this folder; writes states/R1_A1arrays_S1plan.npz and states/R3_X2arrays_S3plan.npz)
R1: the arrays zh, zl, z2, z3 of #710's A1 state (I710-win/A1, D 99.875, converged on its own plan, differing from cont3's by up to 1e-17 per entry) with the meta of states/S1_shift1e-4.npz (cont3's meta, the node segs[3][1] shifted by 1e-4).
R3: the arrays of #725's X2 state with the meta of states/S3_shift1e-3.npz (shift 1e-3). Nothing else is edited.
The check after each write: the arrays equal the source state's bit for bit, the meta equals the shifted state's meta exactly, and the arrays DIFFER from cont3's (so the start is a different one).
--selftest: planted copies with one array entry changed, a changed meta key, cont3's own arrays instead of the other state's must each be flagged, and the right copy must pass."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
KEYS = ("zh", "zl", "z2", "z3")
CONT3 = "I682-win/cont3/anm_pin13_D99.8750.npz"
JOBS = {"R1": ("I710-win/A1/anm_pin13_D99.8750.npz", "S1_shift1e-4", "R1_A1arrays_S1plan"),
        "R3": ("I725-win/X2/anm_pin13_D99.8750.npz", "S3_shift1e-3", "R3_X2arrays_S3plan")}


def load(path):
    d = np.load(path, allow_pickle=False)
    return {k: np.array(d[k]) for k in KEYS}, json.loads(str(d["meta"]))


def check(src, shifted, cont3, new):
    """problems: arrays equal the source's, meta equals the shifted state's, and the arrays differ from cont3's"""
    bad = []
    for k in KEYS:
        if new[0][k].tobytes() != src[0][k].tobytes():
            bad.append(f"array {k} is not the source state's")
    if new[1] != shifted[1]:
        bad.append("meta differs from the shifted state's")
    if all(new[0][k].tobytes() == cont3[0][k].tobytes() for k in KEYS):
        bad.append("the arrays are cont3's, not a different start")
    return bad


def selftest():
    src = load(os.path.join(RAW, JOBS["R1"][0]))
    sh = load(os.path.join(HERE, "states", "S1_shift1e-4.npz"))
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
    c3 = load(os.path.join(RAW, CONT3))
    log = []
    for name, (srcp, shp, out) in JOBS.items():
        src = load(os.path.join(RAW, srcp))
        sh = load(os.path.join(HERE, "states", shp + ".npz"))
        path = os.path.join(HERE, "states", out + ".npz")
        np.savez(path, zh=src[0]["zh"], zl=src[0]["zl"], z2=src[0]["z2"], z3=src[0]["z3"], meta=json.dumps(sh[1]))
        bad = check(src, sh, c3, load(path))
        mx = max(float(np.max(np.abs(src[0][k] - c3[0][k]))) for k in KEYS[:1])
        line = f"{name}: arrays of {srcp} (max |zh difference| from cont3's {mx:.3e}) with the meta of states/{shp}.npz -> states/{out}.npz; problems {bad}"
        print(line)
        log.append(line)
        if bad:
            sys.exit(1)
    open(os.path.join(HERE, "states", "repro_log.txt"), "w").write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
