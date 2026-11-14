#!/usr/bin/env python3
"""#754: copies of cont3's D 99.875 state whose plan takes A1's or X2's interior nodes in one part of the plan only.
    python make_754.py [RAW]              (venv-t151 python, from this folder; writes states/<name>.npz and states/edit_log.txt)
    python make_754.py --selftest [RAW]
RAW is the raw clone (default: this folder's parent). The plans (meta["segs"]) of cont3 (I682-win/cont3), A1 (I710-win/A1)
and X2 (I725-win/X2) share their structure and their segment ends, and differ in the interior nodes (#727, #751).
  LA, LX   cont3's arrays and plan, with segment 3's interior nodes (segs[3][1], segs[3][2]) set to A1's (X2's)
  CA, CX   cont3's arrays and plan, with every other interior node (segments 0 to 2) set to A1's (X2's): the complement
  R_LX     A1's arrays (a different start, as #751's repeat) with LX's plan
Only meta["segs"] changes. The check after each write: the arrays are bit for bit those of the stated source, the changed
meta keys are exactly {segs}, each interior node equals the target plan's in the parts taken from it and cont3's elsewhere,
the segment ends are cont3's, and the plan increases inside each segment.
--selftest: planted copies (an array entry changed, a second meta key changed, one node taken from the wrong plan, a
node in the wrong part, a segment end moved, cont3's arrays under R_LX) must each be flagged, and the right copies pass.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = ("zh", "zl", "z2", "z3")
SRC = {"cont3": "I682-win/cont3/anm_pin13_D99.8750.npz", "A1": "I710-win/A1/anm_pin13_D99.8750.npz",
       "X2": "I725-win/X2/anm_pin13_D99.8750.npz"}
# name: (the arrays' source, the plan the nodes come from, the segments whose interior nodes come from it)
CASES = {"LA": ("cont3", "A1", (3,)), "CA": ("cont3", "A1", (0, 1, 2)), "LX": ("cont3", "X2", (3,)),
         "CX": ("cont3", "X2", (0, 1, 2)), "R_LX": ("A1", "X2", (3,))}


def load(path):
    d = np.load(path, allow_pickle=False)
    return {k: np.array(d[k]) for k in KEYS}, json.loads(str(d["meta"]))


def mixed(base, other, parts):
    """cont3's plan with the interior nodes of the segments in parts taken from other"""
    segs = [list(sg) for sg in base]
    for i in parts:
        segs[i] = [base[i][0]] + list(other[i][1:-1]) + [base[i][-1]]
    return segs


def check(arr_src, cont3, other, parts, new):
    """problems of the written copy new = (arrays, meta) against its intended sources"""
    bad = []
    for k in KEYS:
        if new[0][k].tobytes() != arr_src[0][k].tobytes():
            bad.append(f"array {k} is not its source's")
    changed = {k for k in set(new[1]) | set(cont3[1]) if new[1].get(k) != cont3[1].get(k)}
    if changed - {"segs"}:
        bad.append(f"meta keys other than segs changed: {sorted(changed - {'segs'})}")
    base, segs = cont3[1]["segs"], new[1]["segs"]
    if [len(s) for s in segs] != [len(s) for s in base]:
        return bad + ["the plan's structure differs from cont3's"]
    for i, sg in enumerate(segs):
        if sg[0] != base[i][0] or sg[-1] != base[i][-1]:
            bad.append(f"segment {i}'s ends moved")
        want = other[1]["segs"][i] if i in parts else base[i]
        for j in range(1, len(sg) - 1):
            if sg[j] != want[j]:
                bad.append(f"node segs[{i}][{j}] is {sg[j]!r}, wanted {want[j]!r}")
        if any(b <= a for a, b in zip(sg[:-1], sg[1:])):
            bad.append(f"segment {i} does not increase")
    return bad


def write(raw, name, srcs):
    a, o, parts = CASES[name]
    arrs, meta = srcs[a][0], dict(srcs["cont3"][1])
    meta["segs"] = mixed(srcs["cont3"][1]["segs"], srcs[o][1]["segs"], parts)
    out = os.path.join(HERE, "states", f"{name}.npz")
    np.savez(out, meta=json.dumps(meta), **arrs)
    new = load(out)
    bad = check(srcs[a], srcs["cont3"], srcs[o], parts, new)
    moved = [(i, j, srcs["cont3"][1]["segs"][i][j], new[1]["segs"][i][j]) for i, sg in enumerate(new[1]["segs"])
             for j in range(1, len(sg) - 1) if sg[j] != srcs["cont3"][1]["segs"][i][j]]
    line = (f"{name}: arrays of {a}, segments {list(parts)} from {o}; nodes moved from cont3's "
            + ", ".join(f"[{i}][{j}] {x!r} -> {y!r} ({y - x:+.3e})" for i, j, x, y in moved) + f"; problems {bad}")
    return line, bad


def selftest(srcs):
    n = bad_n = 0
    c3, a1, x2 = srcs["cont3"], srcs["A1"], srcs["X2"]

    def case(label, arr_src, other, parts, arrs, segs, want_ok, meta_extra=None):
        nonlocal n, bad_n
        meta = dict(c3[1], segs=segs, **(meta_extra or {}))
        bad = check(arr_src, c3, other, parts, (arrs, meta))
        good = (not bad) == want_ok
        print(f"  {label}: problems {bad} {'ok' if good else 'WRONG'}")
        n += 1
        bad_n += not good

    la = mixed(c3[1]["segs"], a1[1]["segs"], (3,))
    case("LA, the right copy", c3, a1, (3,), dict(c3[0]), la, True)
    case("CX, the right copy", c3, x2, (0, 1, 2), dict(c3[0]), mixed(c3[1]["segs"], x2[1]["segs"], (0, 1, 2)), True)
    case("R_LX, the right copy", a1, x2, (3,), dict(a1[0]), mixed(c3[1]["segs"], x2[1]["segs"], (3,)), True)
    a2 = dict(c3[0])
    a2["zh"] = c3[0]["zh"].copy()
    a2["zh"][4] = np.nextafter(a2["zh"][4], np.inf)
    case("one array entry changed", c3, a1, (3,), a2, la, False)
    case("a second meta key changed", c3, a1, (3,), dict(c3[0]), la, False, dict(a=0.5))
    wrong = [list(s) for s in la]
    wrong[3][1] = x2[1]["segs"][3][1]
    case("one node from the wrong plan", c3, a1, (3,), dict(c3[0]), wrong, False)
    case("a node in the wrong part (segment 0 from A1 too)", c3, a1, (3,), dict(c3[0]),
         mixed(la, a1[1]["segs"], (0,)), False)
    endm = [list(s) for s in la]
    endm[3][0] = endm[3][0] + 1e-3
    case("a segment end moved", c3, a1, (3,), dict(c3[0]), endm, False)
    case("cont3's arrays under R_LX", a1, x2, (3,), dict(c3[0]), mixed(c3[1]["segs"], x2[1]["segs"], (3,)), False)
    print("selftest", "passed" if bad_n == 0 else "FAILED", f"({n - bad_n} of {n})")
    return 0 if bad_n == 0 else 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    raw = args[0] if args else os.path.dirname(HERE)
    srcs = {k: load(os.path.join(raw, p)) for k, p in SRC.items()}
    if "--selftest" in sys.argv:
        sys.exit(selftest(srcs))
    os.makedirs(os.path.join(HERE, "states"), exist_ok=True)
    log = []
    for name in CASES:
        line, bad = write(raw, name, srcs)
        print(line)
        log.append(line)
        if bad:
            sys.exit(1)
    open(os.path.join(HERE, "states", "edit_log.txt"), "w").write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
