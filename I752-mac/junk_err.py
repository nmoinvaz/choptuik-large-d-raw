#!/usr/bin/env python3
"""#752: the error of each point of an attempt in p1's odd harmonics against a converged root of the same plan: the
prediction (before its re-seed), the iterate at Newton step 1, and its full-step trial z1 + d1, as |(a_k, b_k)| of
p1 minus the root's (crawl_probe.harmonics' convention), with the max over all unknowns for scale. Numpy only.
usage: python3 junk_err.py RAW [--mutate k17]
The roots: the crawl's from fixrun (from the refused full step, the same plan as the crawl's attempt); the control's
is #742's M state at D 117.5 (the control's attempt is M's first, the same plan). --mutate k17 adds 1e-20 cos(17
theta) to the last part of the crawl iterate's p1, where its error is about 1e-30: the iterate's k 17 must then read
1e-20 within a factor 2 (the control of the reading). Exit 1 when the control reading misses."""
import json
import sys

import numpy as np

raw = sys.argv[1]
mutate = "--mutate" in sys.argv
M = 32
th = np.pi * np.arange(M) / M
ks = np.arange(1, M, 2)


def harm(v):
    a = (2.0 / M) * np.cos(np.outer(ks, th)) @ v
    b = (2.0 / M) * np.sin(np.outer(ks, th)) @ v
    return np.hypot(a, b)


def parts(path, keys):
    d = np.load(f"{raw}/{path}")
    return [np.asarray(d[k], dtype=float) for k in keys if k in d.files]


def lead_diff(x, y):
    """x - y as the sum of the parts' differences, smallest first: the leading parts' difference is exact for
    neighbouring values (Sterbenz), so the result is good to about 1e-32 of the values"""
    n = max(len(x), len(y))
    z = np.zeros_like(x[0])
    x, y = list(x) + [z] * (n - len(x)), list(y) + [z] * (n - len(y))
    e = np.zeros_like(z)
    for q in range(n - 1, -1, -1):
        e = e + (x[q] - y[q])
    return e


Q = ("zh", "zl", "z2", "z3")
O = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
cases = {
    "crawl (a = 1, D 118)": dict(pred="I752-mac/R/pred_pin13_D118.0000.npz", it="I752-mac/R/crawl_iter_D118.0000_s1.npz",
                                 root="I752-mac/fix/fixrun_D118.0000_s1_switch0_own_from1.npz"),
    "control (a = 1/2, D 117.5)": dict(pred="I752-mac/R/pred_pin13_D117.5000.npz", it="I752-mac/R/crawl_iter_D117.5000_s1.npz",
                                       root="I742-win/M/anm_pin13_D117.5000.npz"),
}
bad = 0
for name, c in cases.items():
    root = parts(c["root"], O if "fixrun" not in c["root"] else [f"z{q}" for q in range(8)])
    pred = parts(c["pred"], Q)
    it = parts(c["it"], [f"z{q}" for q in range(8)])
    if mutate and name.startswith("crawl"):
        it[7] = it[7].copy()
        it[7][:M] += 1e-20 * np.cos(17 * th)
    dd = parts(c["it"], [f"d{q}" for q in range(8)])
    print(f"{name}: root {c['root']}")
    e_it = lead_diff(it, root)
    for lab, e in (("prediction", lead_diff(pred, root)), ("iterate z1", e_it), ("trial z1 + d1", e_it + (dd[0] + dd[1]))):
        h = harm(np.asarray(e[:M], dtype=float))
        row = ", ".join(f"k {k} {x:.2e}" for k, x in zip(ks, h) if k >= 7 and k <= 17)
        print(f"  {lab}: max|z - root| {float(np.abs(e).max()):.2e}; p1 {float(np.abs(e[:M]).max()):.2e}; harmonics {row}")
        if mutate and name.startswith("crawl") and lab == "iterate z1":
            ok = 0.5e-20 < h[ks.tolist().index(17)] < 2e-20
            print(f"  control: the planted 1e-20 in k 17 reads {h[ks.tolist().index(17)]:.2e}: {'ok' if ok else 'MISSED'}")
            bad += not ok
sys.exit(1 if bad else 0)
