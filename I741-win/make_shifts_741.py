#!/usr/bin/env python3
"""#741: copies of cont3's D 99.875 state (I682-win/cont3/anm_pin13_D99.8750.npz) whose plan has ONE interior node shifted, beside the original, which is not touched.
usage: python make_shifts_741.py [--selftest]       (venv-t151 python, from this folder; writes states/S<k>_shift<tag>.npz and states/edit_log.txt)
The node is segs[3][1] (0.6485815917, the first free interior node of the last segment; X2's plan differs from cont3's most there, by 9.489e-4). Only meta["segs"] changes, by exactly that node plus the shift; zh, zl, z2, z3 are copied bit for bit.
Shifts: S0 0 (the control), S1 1e-4, S2 3e-4, S3 1e-3, S4 3e-3, S5 1e-2 (made now, run only after the fit is written down).
The check after each write: arrays bit-identical, changed meta keys exactly {segs}, exactly one node differs from cont3's plan, it is segs[3][1], and it moved by the shift to within 1e-15 (S0: nothing differs).
--selftest: planted copies with one array entry changed, a second meta key changed, two nodes shifted, the wrong node shifted, the wrong shift size, and an unshifted copy for a nonzero shift must each be flagged, and the right copy must pass."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
CONT3 = "I682-win/cont3/anm_pin13_D99.8750.npz"
KEYS = ("zh", "zl", "z2", "z3")
NODE = (3, 1)
SHIFTS = {"S0": ("0", 0.0), "S1": ("1e-4", 1e-4), "S2": ("3e-4", 3e-4), "S3": ("1e-3", 1e-3), "S4": ("3e-3", 3e-3), "S5": ("1e-2", 1e-2)}


def load(path):
    d = np.load(path, allow_pickle=False)
    return {k: np.array(d[k]) for k in KEYS}, json.loads(str(d["meta"]))


def check(orig, new, shift, node=NODE):
    """(problems, differing nodes): empty problems when the arrays are bit-identical, only segs changed, and exactly the node `node` moved by `shift`"""
    (oa, om), (na, nm) = orig, new
    bad = []
    for k in KEYS:
        if oa[k].dtype != na[k].dtype or oa[k].shape != na[k].shape or oa[k].tobytes() != na[k].tobytes():
            bad.append(f"array {k} differs")
    changed = sorted(k for k in set(om) | set(nm) if om.get(k) != nm.get(k))
    want_keys = ["segs"] if shift != 0 else []
    if changed != want_keys:
        bad.append(f"changed meta keys {changed}, expected {want_keys}")
    a, b = om["segs"], nm["segs"]
    diff = []
    if len(a) != len(b) or any(len(x) != len(y) for x, y in zip(a, b)):
        bad.append("the plan's shape changed")
    else:
        diff = [(i, j, y - x) for i, (sa, sb) in enumerate(zip(a, b)) for j, (x, y) in enumerate(zip(sa, sb)) if x != y]
        if shift == 0 and diff:
            bad.append(f"nodes differ for the zero shift: {diff}")
        if shift != 0:
            if [(i, j) for i, j, _ in diff] != [node]:
                bad.append(f"differing nodes {[(i, j) for i, j, _ in diff]}, expected only {node}")
            elif abs(diff[0][2] - shift) > 1e-15:
                bad.append(f"the node moved by {diff[0][2]:.6e}, expected {shift:.6e}")
    return bad, diff


def shifted(meta, shift, node=NODE):
    segs = [list(s) for s in meta["segs"]]
    segs[node[0]][node[1]] = segs[node[0]][node[1]] + shift
    return dict(meta, segs=segs)


def selftest():
    arrs, meta = load(os.path.join(RAW, CONT3))
    s = 1e-3
    cases = []
    cases.append(("the right copy (shift 1e-3, node [3][1])", (dict(arrs), shifted(meta, s)), s, True))
    a2 = dict(arrs)
    a2["zh"] = arrs["zh"].copy()
    a2["zh"][5] = np.nextafter(a2["zh"][5], np.inf)
    cases.append(("one array entry changed", (a2, shifted(meta, s)), s, False))
    cases.append(("a second meta key changed", (dict(arrs), dict(shifted(meta, s), a=0.5)), s, False))
    two = shifted(shifted(meta, s), 1e-4, node=(0, 1))
    cases.append(("two nodes shifted", (dict(arrs), two), s, False))
    cases.append(("the wrong node shifted", (dict(arrs), shifted(meta, s, node=(1, 1))), s, False))
    cases.append(("the wrong shift size (2e-3)", (dict(arrs), shifted(meta, 2e-3)), s, False))
    cases.append(("no shift for a nonzero shift", (dict(arrs), dict(meta)), s, False))
    n = 0
    for label, new, sh, want_ok in cases:
        bad, _ = check((arrs, meta), new, sh)
        good = (not bad) == want_ok
        print(f"  {label}: problems {bad} {'ok' if good else 'WRONG'}")
        n += good
    bad0, _ = check((arrs, meta), (dict(arrs), dict(meta)), 0.0)
    g0 = not bad0
    print(f"  the zero shift, untouched: problems {bad0} {'ok' if g0 else 'WRONG'}")
    n += g0
    bad0b, _ = check((arrs, meta), (dict(arrs), shifted(meta, 1e-4)), 0.0)
    g0b = bool(bad0b)
    print(f"  the zero shift with a node moved: problems {bad0b} {'ok' if g0b else 'WRONG'}")
    n += g0b
    ok = n == len(cases) + 2
    print("selftest", "passed" if ok else "FAILED")
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    os.makedirs(os.path.join(HERE, "states"), exist_ok=True)
    orig = load(os.path.join(RAW, CONT3))
    log = []
    for name, (tag, sh) in SHIFTS.items():
        meta = shifted(orig[1], sh) if sh else dict(orig[1])
        out = os.path.join(HERE, "states", f"{name}_shift{tag}.npz")
        np.savez(out, zh=orig[0]["zh"], zl=orig[0]["zl"], z2=orig[0]["z2"], z3=orig[0]["z3"], meta=json.dumps(meta))
        new = load(out)
        bad, diff = check(orig, new, sh)
        line = (f"{name}: shift {tag} of segs{list(NODE)} ({orig[1]['segs'][NODE[0]][NODE[1]]!r} -> {new[1]['segs'][NODE[0]][NODE[1]]!r}) -> states/{name}_shift{tag}.npz; "
                f"differing nodes {[(i, j) for i, j, _ in diff]}; arrays bit-identical: {not any('array' in b for b in bad)}; problems {bad}")
        print(line)
        log.append(line)
        if bad:
            sys.exit(1)
    open(os.path.join(HERE, "states", "edit_log.txt"), "w").write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
