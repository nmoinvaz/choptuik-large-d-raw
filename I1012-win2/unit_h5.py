"""Unit check of --h5/--h7 plumbing on a scratch extract of main 23844822: LazyHier.h(l, x) with HIER_NB_H5 / HIER_NB_H7 in the environment (what hier_nb's main sets from --h5=/--h7=,
and what the spawn workers inherit). x is #999's pretuned x. Prints the level-5 step against the formula and against hier's default; exit 0 when all agree."""
import os, sys
import numpy as np
SRC = sys.argv[1]; mode = sys.argv[2]            # mode: default | h5 | h5_1e-6 | wrongenv
if mode == "h5": os.environ["HIER_NB_H5"] = "1e-4"
if mode == "h5_1e-6": os.environ["HIER_NB_H5"] = "1e-6"
if mode == "wrongenv": os.environ["HIER_NB_H5X"] = "1e-4"
sys.path.insert(0, SRC)
import hier_nb as HN, hier as H
x = np.array([2.719219, 1.000022, 0.148977988, 0.014770713, 0.008424206, 0.001511189, 0.000474205, 0.00012168, 2.6602985034854245e-05, 8.947854197796251e-06])
h = HN.LazyHier(9, 0.15, top=99, verbose=0)
PARENT = HN.LazyHier.__mro__[1]                  # hier_nb replaces H.Hier by LazyHier on import: the baseline is the parent class
base = h
for l in (3, 5, 7):
    b = x[H.idx(l)]
    default = 1e-6 * np.maximum(np.abs(b), 1e-3 * np.abs(x[0]))
    got = h.h(l, x); bd = PARENT.h(h, l, x)
    print(f"mode {mode} level {l}: FD_STEP {HN.FD_STEP.get(l)}, LazyHier.h {got}, hier default {bd}, relative to the default {got / default}")
    assert np.array_equal(bd, default), "hier's default is not the formula"
    want = default if HN.FD_STEP.get(l) is None else HN.FD_STEP[l] * np.maximum(np.abs(b), 1e-3 * np.abs(x[0]))
    assert np.array_equal(got, want), f"level {l}: LazyHier.h differs from the formula"
r5 = h.h(5, x) / (1e-6 * np.maximum(np.abs(x[H.idx(5)]), 1e-3 * np.abs(x[0])))
expect = {"h5": 100.0, "h5_1e-6": 1.0, "default": 1.0, "wrongenv": 1.0}[mode]
assert np.allclose(r5, expect, rtol=1e-12), f"level-5 step is {r5} times the default, expected {expect}"
r37 = [float(np.max(np.abs(h.h(l, x) / (1e-6 * np.maximum(np.abs(x[H.idx(l)]), 1e-3 * np.abs(x[0])))))) for l in (3, 7)]
assert r37 == [1.0, 1.0], f"levels 3 and 7 moved: {r37}"
print(f"mode {mode}: level-5 step = {r5} x default (expected {expect}), levels 3 and 7 unchanged: OK")
