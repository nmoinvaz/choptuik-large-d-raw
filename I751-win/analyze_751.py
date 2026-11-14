#!/usr/bin/env python3
"""#751: the single-node effects at 1e-3 on Delta, and their sum against the offsets of A1's and X2's plans.
usage: python analyze_751.py [--selftest]       (venv-t151 python, from this folder; reads NA..NF/base_pin13_D99.8750.npz, #741's S3, the repeat R_<X> when it exists)
Effect of a node = Delta(its polished state) - X2c's Delta (the root of cont3's plan), Delta the exact sum of the eight parts (arb, 600 bits).
Offsets: Delta(A1 on its own plan) - root and Delta(X2 on its own plan) - root (+2.9709e-26, -1.6580e-25, #727).
Literal test of the issue (c): the sum of the six effects, and the sum of seven with #741's S3 (segs[3][1], +1e-3), against each offset; 'within a factor 2' = the same sign and a ratio sum / offset between 0.5 and 2.
Extra, labelled as an assumption of linearity: each effect scaled by the plan's actual per-node shift from cont3's (shift / 1e-3), summed over the seven nodes.
(b): the repeat of the node with the largest |effect| (R_<X>, from A1's arrays) must reproduce that node's Delta to 1e-40.
--selftest: the factor-2 classifier on planted ratios (1.9 yes, 2.1 no, 0.51 yes, 0.49 no, opposite sign no) and a planted sum."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RAW, "I739-win"))
import cmp_739 as c          # noqa: E402

c.flint.ctx.prec = 600
ROOT = os.path.join(RAW, "I727-win", "X2c", "base_pin13_D99.8750.npz")
CONT3 = os.path.join(RAW, "I682-win", "cont3", "anm_pin13_D99.8750.npz")
OWN = {"A1": os.path.join(RAW, "I710-win", "A1", "anm_pin13_D99.8750.npz"), "X2": os.path.join(RAW, "I725-win", "X2", "anm_pin13_D99.8750.npz")}
NODES = {"A": (0, 1), "B": (0, 2), "C": (1, 1), "D": (1, 2), "E": (2, 1), "F": (3, 2), "S3": (3, 1)}
BASE = {k: os.path.join(HERE, k, "base_pin13_D99.8750.npz") for k in "ABCDEF"}
BASE = {("N" + k): v.replace(os.path.join(HERE, k), os.path.join(HERE, "N" + k)) for k, v in BASE.items()}
BASE["S3"] = os.path.join(RAW, "I741-win", "S3", "base_pin13_D99.8750.npz")


def within2(total, offset):
    """the same sign and 0.5 <= total / offset <= 2"""
    if offset == 0 or total == 0 or (total > 0) != (offset > 0):
        return False
    return 0.5 <= total / offset <= 2.0


def plan(path):
    return json.loads(str(np.load(path, allow_pickle=False)["meta"]))["segs"]


def selftest():
    bad = 0
    for total, off, want in ((1.9e-26, 1e-26, True), (2.1e-26, 1e-26, False), (5.1e-27, 1e-26, True), (4.9e-27, 1e-26, False), (-1e-26, 1e-26, False), (0.0, 1e-26, False)):
        got = within2(total, off)
        print(f"  planted sum {total:g} against offset {off:g}: within a factor 2 {got} (expected {want}) {'ok' if got == want else 'WRONG'}")
        bad += got != want
    s = sum([1e-26, -2e-27, 3e-27])
    ok = abs(s - 1.1e-26) < 1e-40
    print(f"  planted sum of three effects: {s:.4e} {'ok' if ok else 'WRONG'}")
    bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    root = c.delta(ROOT)
    offs = {k: float((c.delta(p) - root).mid()) for k, p in OWN.items()}
    c3 = plan(CONT3)
    eff, rows = {}, []
    for k, node in NODES.items():
        p = BASE[("N" + k) if k != "S3" else "S3"]
        if os.path.exists(p):
            eff[k] = float((c.delta(p) - root).mid())
    print(f"root (X2c): {root.str(40, radius=False)}")
    print(f"offsets against the root: A1 on its own plan {offs['A1']:+.4e}, X2 on its own plan {offs['X2']:+.4e}\n")
    print("| node | segs index | cont3's value | shift of A1's plan | shift of X2's plan | effect at +1e-3 (Delta - root) |\n|---|---|---|---|---|---|")
    pl = {k: plan(p) for k, p in OWN.items()}
    shifts = {}
    for k, (i, j) in NODES.items():
        shifts[k] = {a: pl[a][i][j] - c3[i][j] for a in pl}
        e = f"{eff[k]:+.4e}" if k in eff else "not run yet"
        print(f"| {k} | [{i}][{j}] | {c3[i][j]:.10f} | {shifts[k]['A1']:+.3e} | {shifts[k]['X2']:+.3e} | {e} |")
    done = [k for k in NODES if k in eff]
    if done:
        big = max(done, key=lambda k: abs(eff[k]))
        print(f"\nlargest single-node effect so far: node {big} {NODES[big]}, {eff[big]:+.4e}")
    six = [k for k in "ABCDEF"]
    if all(k in eff for k in six):
        s6 = sum(eff[k] for k in six)
        s7 = s6 + eff["S3"] if "S3" in eff else None
        print("\nliteral test (c): the sum of the effects at 1e-3 against each plan's offset\n")
        print("| sum | value | against A1's offset (ratio, within a factor 2) | against X2's offset (ratio, within a factor 2) |\n|---|---|---|---|")
        for label, s in (("six nodes", s6), ("seven nodes (with S3)", s7)):
            if s is None:
                continue
            cells = []
            for a in ("A1", "X2"):
                cells.append(f"{s / offs[a]:+.3f}, {'YES' if within2(s, offs[a]) else 'NO'}")
            print(f"| {label} | {s:+.4e} | {cells[0]} | {cells[1]} |")
        print("\nextra (an assumption of linearity, which #741 did not support for segs[3][1]): each effect scaled by the plan's actual node shift / 1e-3\n")
        print("| plan | scaled sum over the seven nodes | offset | ratio |\n|---|---|---|---|")
        for a in ("A1", "X2"):
            sc = sum(eff[k] * shifts[k][a] / 1e-3 for k in NODES if k in eff)
            print(f"| {a} | {sc:+.4e} | {offs[a]:+.4e} | {sc / offs[a]:+.3f} |")
    # (b) the repeat
    for k in "ABCDEF":
        rp = os.path.join(HERE, f"R_{k}", "base_pin13_D99.8750.npz")
        if os.path.exists(rp) and ("N" + k) in BASE and os.path.exists(BASE["N" + k]):
            d = float((c.delta(rp) - c.delta(BASE["N" + k])).mid())
            print(f"\n(b) repeat of node {k} from A1's arrays: Delta(R_{k}) - Delta(N{k}) = {d:+.4e}; bar 1e-40: {'met' if abs(d) <= 1e-40 else 'NOT MET'}")


if __name__ == "__main__":
    main()
