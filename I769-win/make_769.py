"""#769: copies of cont3's D 99.875 state with one of the last segment's interior nodes moved by s times A1's shift,
s = 0.25, 0.75, 1.5 and 2.0 (I710-win/A1): a node c becomes c + s (a - c), with a its value in A1's plan. With #763's
s = 0.5 and 1.0 that gives each node's effect at six shifts. The control C_N2_05 is #763's N2_05 made again.
    python make_769.py [RAW]              (venv-t151 python, from this folder; writes states/<name>.npz and states/edit_log.txt)
    python make_769.py --selftest [RAW]
  N1_<s>   segs[3][1] moved, every other node cont3's
  N2_<s>   segs[3][2] moved
Only meta["segs"] changes, and the arrays are cont3's bit for bit, checked after each write as make_763.py does; its
--selftest is make_763.py's seven cases and three at this task's scales.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = ("zh", "zl", "z2", "z3")
CONT3 = "I682-win/cont3/anm_pin13_D99.8750.npz"
A1 = "I710-win/A1/anm_pin13_D99.8750.npz"
NODES = {"N1": [(3, 1)], "N2": [(3, 2)], "P": [(3, 1), (3, 2)]}
SCALES = {"025": 0.25, "075": 0.75, "15": 1.5, "20": 2.0}
# the states written: each node at each scale, and the control (name, node, scale)
MAKE = [(f"{k}_{t}", k, s) for k in ("N1", "N2") for t, s in SCALES.items()] + [("C_N2_05", "N2", 0.5)]


def load(path):
    d = np.load(path, allow_pickle=False)
    return {k: np.array(d[k]) for k in KEYS}, json.loads(str(d["meta"]))


def target(base, a1, nodes, s):
    segs = [list(sg) for sg in base]
    for i, j in nodes:
        segs[i][j] = base[i][j] + s * (a1[i][j] - base[i][j])
    return segs


def check(c3, a1, nodes, s, new):
    bad = []
    for k in KEYS:
        if new[0][k].tobytes() != c3[0][k].tobytes():
            bad.append(f"array {k} is not cont3's")
    changed = {k for k in set(new[1]) | set(c3[1]) if new[1].get(k) != c3[1].get(k)}
    if changed - {"segs"}:
        bad.append(f"meta keys other than segs changed: {sorted(changed - {'segs'})}")
    want = target(c3[1]["segs"], a1[1]["segs"], nodes, s)
    segs = new[1]["segs"]
    if [len(x) for x in segs] != [len(x) for x in want]:
        return bad + ["the plan's structure differs"]
    for i, sg in enumerate(segs):
        for j, v in enumerate(sg):
            if v != want[i][j]:
                bad.append(f"node segs[{i}][{j}] is {v!r}, wanted {want[i][j]!r}")
        if any(b <= a for a, b in zip(sg[:-1], sg[1:])):
            bad.append(f"segment {i} does not increase")
    return bad


def selftest(c3, a1):
    n = bad_n = 0

    def case(label, arrs, segs, nodes, s, want_ok, extra=None):
        nonlocal n, bad_n
        bad = check(c3, a1, nodes, s, (arrs, dict(c3[1], segs=segs, **(extra or {}))))
        good = (not bad) == want_ok
        print(f"  {label}: problems {bad} {'ok' if good else 'WRONG'}")
        n += 1
        bad_n += not good

    base, other = c3[1]["segs"], a1[1]["segs"]
    case("P_10, the right copy", dict(c3[0]), target(base, other, NODES["P"], 1.0), NODES["P"], 1.0, True)
    case("N1_05, the right copy", dict(c3[0]), target(base, other, NODES["N1"], 0.5), NODES["N1"], 0.5, True)
    a2 = dict(c3[0])
    a2["zh"] = c3[0]["zh"].copy()
    a2["zh"][4] = np.nextafter(a2["zh"][4], np.inf)
    case("one array entry changed", a2, target(base, other, NODES["N1"], 1.0), NODES["N1"], 1.0, False)
    case("a second meta key changed", dict(c3[0]), target(base, other, NODES["N1"], 1.0), NODES["N1"], 1.0, False, dict(a=0.5))
    case("the wrong scale (1.0 for 0.5)", dict(c3[0]), target(base, other, NODES["N2"], 1.0), NODES["N2"], 0.5, False)
    case("N2_20, the right copy", dict(c3[0]), target(base, other, NODES["N2"], 2.0), NODES["N2"], 2.0, True)
    case("N1_025, the right copy", dict(c3[0]), target(base, other, NODES["N1"], 0.25), NODES["N1"], 0.25, True)
    case("the wrong scale (1.5 for 2.0)", dict(c3[0]), target(base, other, NODES["N1"], 1.5), NODES["N1"], 2.0, False)
    case("an unmoved node moved (P for N1)", dict(c3[0]), target(base, other, NODES["P"], 1.0), NODES["N1"], 1.0, False)
    case("the wrong node moved (N2 for N1)", dict(c3[0]), target(base, other, NODES["N2"], 1.0), NODES["N1"], 1.0, False)
    print("selftest", "passed" if bad_n == 0 else "FAILED", f"({n - bad_n} of {n})")
    return 0 if bad_n == 0 else 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    raw = args[0] if args else os.path.dirname(HERE)
    c3, a1 = load(os.path.join(raw, CONT3)), load(os.path.join(raw, A1))
    if "--selftest" in sys.argv:
        sys.exit(selftest(c3, a1))
    os.makedirs(os.path.join(HERE, "states"), exist_ok=True)
    log = []
    for name, nm, s in MAKE:
        nodes = NODES[nm]
        meta = dict(c3[1], segs=target(c3[1]["segs"], a1[1]["segs"], nodes, s))
        out = os.path.join(HERE, "states", f"{name}.npz")
        np.savez(out, meta=json.dumps(meta), **c3[0])
        new = load(out)
        bad = check(c3, a1, nodes, s, new)
        moved = ", ".join(f"[{i}][{j}] {c3[1]['segs'][i][j]!r} -> {new[1]['segs'][i][j]!r} "
                          f"({new[1]['segs'][i][j] - c3[1]['segs'][i][j]:+.4e})" for i, j in nodes)
        line = f"{name}: scale {s}, {moved}; problems {bad}"
        print(line)
        log.append(line)
        if bad:
            sys.exit(1)
    open(os.path.join(HERE, "states", "edit_log.txt"), "w").write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
