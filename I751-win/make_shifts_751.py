#!/usr/bin/env python3
"""#751: copies of cont3's D 99.875 state (I682-win/cont3/anm_pin13_D99.8750.npz) whose plan has ONE interior node shifted by +1e-3, for each of the six interior nodes #741 did not shift, beside the original, which is not touched.
usage: python make_shifts_751.py [--selftest]       (venv-t151 python, from this folder; writes states/<name>.npz and states/edit_log.txt)
Nodes (segs[i][j] of cont3's plan): A [0][1], B [0][2], C [1][1], D [1][2], E [2][1], F [3][2]. (#741 shifted [3][1], its S3 at 1e-3 is the seventh node of the comparison.)
Only meta["segs"] changes, by exactly that node plus 1e-3; zh, zl, z2, z3 are copied bit for bit.
The check after each write: arrays bit-identical, changed meta keys exactly {segs}, exactly one node differs from cont3's plan, it is the named node, and it moved by 1e-3 to within 1e-15, and the plan is still increasing inside its segment.
--selftest: planted copies with one array entry changed, a second meta key changed, two nodes shifted, the wrong node shifted, the wrong shift size, no shift, and a node moved past its neighbour must each be flagged, and the right copy must pass."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
CONT3 = "I682-win/cont3/anm_pin13_D99.8750.npz"
KEYS = ("zh", "zl", "z2", "z3")
SHIFT = 1e-3
NODES = {"A": (0, 1), "B": (0, 2), "C": (1, 1), "D": (1, 2), "E": (2, 1), "F": (3, 2)}


def load(path):
    d = np.load(path, allow_pickle=False)
    return {k: np.array(d[k]) for k in KEYS}, json.loads(str(d["meta"]))


def check(orig, new, node, shift=SHIFT):
    (oa, om), (na, nm) = orig, new
    bad = []
    for k in KEYS:
        if oa[k].dtype != na[k].dtype or oa[k].shape != na[k].shape or oa[k].tobytes() != na[k].tobytes():
            bad.append(f"array {k} differs")
    changed = sorted(k for k in set(om) | set(nm) if om.get(k) != nm.get(k))
    if changed != ["segs"]:
        bad.append(f"changed meta keys {changed}, expected ['segs']")
    a, b = om["segs"], nm["segs"]
    diff = []
    if len(a) != len(b) or any(len(x) != len(y) for x, y in zip(a, b)):
        bad.append("the plan's shape changed")
    else:
        diff = [(i, j, y - x) for i, (sa, sb) in enumerate(zip(a, b)) for j, (x, y) in enumerate(zip(sa, sb)) if x != y]
        if [(i, j) for i, j, _ in diff] != [node]:
            bad.append(f"differing nodes {[(i, j) for i, j, _ in diff]}, expected only {node}")
        elif abs(diff[0][2] - shift) > 1e-15:
            bad.append(f"the node moved by {diff[0][2]:.6e}, expected {shift:.6e}")
        if any(any(s[k + 1] <= s[k] for k in range(len(s) - 1)) for s in b):
            bad.append("a segment's nodes are no longer increasing")
    return bad, diff


def shifted(meta, node, shift=SHIFT):
    segs = [list(s) for s in meta["segs"]]
    segs[node[0]][node[1]] = segs[node[0]][node[1]] + shift
    return dict(meta, segs=segs)


def selftest():
    arrs, meta = load(os.path.join(RAW, CONT3))
    node = NODES["A"]
    cases = [("the right copy (node A, +1e-3)", (dict(arrs), shifted(meta, node)), node, True)]
    a2 = dict(arrs)
    a2["zh"] = arrs["zh"].copy()
    a2["zh"][5] = np.nextafter(a2["zh"][5], np.inf)
    cases += [("one array entry changed", (a2, shifted(meta, node)), node, False),
              ("a second meta key changed", (dict(arrs), dict(shifted(meta, node), a=0.5)), node, False),
              ("two nodes shifted", (dict(arrs), shifted(shifted(meta, node), NODES["F"])), node, False),
              ("the wrong node shifted", (dict(arrs), shifted(meta, NODES["B"])), node, False),
              ("the wrong shift size (2e-3)", (dict(arrs), shifted(meta, node, 2e-3)), node, False),
              ("no shift", (dict(arrs), dict(meta)), node, False),
              ("a node moved past its neighbour (+0.05)", (dict(arrs), shifted(meta, node, 0.05)), node, False)]
    n = 0
    for label, new, nd, want_ok in cases:
        bad, _ = check((arrs, meta), new, nd, SHIFT if label != "a node moved past its neighbour (+0.05)" else 0.05)
        good = (not bad) == want_ok
        print(f"  {label}: problems {bad} {'ok' if good else 'WRONG'}")
        n += good
    ok = n == len(cases)
    print("selftest", "passed" if ok else "FAILED")
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    os.makedirs(os.path.join(HERE, "states"), exist_ok=True)
    orig = load(os.path.join(RAW, CONT3))
    log = []
    for name, node in NODES.items():
        out = os.path.join(HERE, "states", f"N{name}_seg{node[0]}_{node[1]}_shift1e-3.npz")
        np.savez(out, zh=orig[0]["zh"], zl=orig[0]["zl"], z2=orig[0]["z2"], z3=orig[0]["z3"], meta=json.dumps(shifted(orig[1], node)))
        new = load(out)
        bad, diff = check(orig, new, node)
        line = (f"N{name}: segs{list(node)} ({orig[1]['segs'][node[0]][node[1]]!r} -> {new[1]['segs'][node[0]][node[1]]!r}) -> {os.path.basename(out)}; "
                f"differing nodes {[(i, j) for i, j, _ in diff]}; arrays bit-identical: {not any('array' in b for b in bad)}; problems {bad}")
        print(line)
        log.append(line)
        if bad:
            sys.exit(1)
    open(os.path.join(HERE, "states", "edit_log.txt"), "w").write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
