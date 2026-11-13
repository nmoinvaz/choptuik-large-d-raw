#!/usr/bin/env python3
"""#727: the segment plan each of the three D 99.875 states carries in its meta (the plan the state solves), and how the plans differ.
usage: python plans_727.py          (venv-t151 python, from this folder; reads the three states of cmp_727.py's STATES)
--selftest is not needed: the comparison is exact equality and a max absolute difference of the stored floats; a planted copy of cont3's plan with one node moved by 1e-3 is checked inline."""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
STATES = {"cont3": "I682-win/cont3/anm_pin13_D99.8750.npz", "A1": "I710-win/A1/anm_pin13_D99.8750.npz", "X2": "I725-win/X2/anm_pin13_D99.8750.npz"}


def meta_of(path):
    d = np.load(path, allow_pickle=True)
    m = d["meta"]
    return json.loads(str(m)) if m.dtype.kind in "US" else m.item()


def compare(a, b):
    """(identical, max |difference| or None when the shapes differ)"""
    if len(a) != len(b) or any(len(x) != len(y) for x, y in zip(a, b)):
        return False, None
    pairs = [(u, v) for x, y in zip(a, b) for u, v in zip(x, y)]
    return all(u == v for u, v in pairs), max(abs(u - v) for u, v in pairs)


metas = {k: meta_of(os.path.join(RAW, p)) for k, p in STATES.items()}
ref = metas["cont3"]["segs"]
# control: a copy of cont3's plan with one interior node moved by 1e-3 must read as different, by 1e-3
planted = [list(s) for s in ref]
planted[1][1] += 1e-3
same, mx = compare(planted, ref)
print(f"control (one node moved by 1e-3): identical {same}, max difference {mx:.3e} {'ok' if (not same and abs(mx - 1e-3) < 1e-12) else 'WRONG'}")
print(f"control (cont3 against itself): identical {compare(ref, ref)[0]} {'ok' if compare(ref, ref)[0] else 'WRONG'}")
for k, m in metas.items():
    segs = m["segs"]
    print(f"{k}: D {m['D_str']}, a {m.get('a')}, steps in the plan {sum(len(s) - 1 for s in segs)}, source {m.get('source')}")
    for s in segs:
        print("   " + "  ".join(f"{x:.10f}" for x in s))
for k in ("A1", "X2"):
    same, mx = compare(metas[k]["segs"], ref)
    print(f"plan of {k} identical to cont3's: {same}; max |node difference| {mx:.4e}")

# the D 99.8125 states, where #725 found X1 and cont3 equal in Delta to 5.67e-34
import flint
flint.ctx.prec = 400
S2 = {"cont3": "I682-win/cont3/anm_pin13_D99.8125.npz", "A0": "I710-win/A0/anm_pin13_D99.8125.npz", "X1": "I725-win/X1/anm_pin13_D99.8125.npz"}


def delta(path):
    d = np.load(path, allow_pickle=True)
    s = flint.arb(0)
    for key in ("zh", "zl", "z2", "z3"):
        if key in d.files:
            s += flint.arb(float(d[key][-1]))
    return s


m2 = {k: meta_of(os.path.join(RAW, p)) for k, p in S2.items()}
d2 = {k: delta(os.path.join(RAW, p)) for k, p in S2.items()}
print("D 99.8125:")
for k in ("A0", "X1"):
    same, mx = compare(m2[k]["segs"], m2["cont3"]["segs"])
    print(f"  plan of {k} identical to cont3's: {same}; max |node difference| {mx:.4e}; |Delta {k} - Delta cont3| {abs(float((d2[k] - d2['cont3']).mid())):.3e}")
for k in ("A1", "X2"):
    dk = delta(os.path.join(RAW, STATES[k]))
    d0 = delta(os.path.join(RAW, STATES["cont3"]))
    print(f"D 99.875: plan difference {compare(metas[k]['segs'], ref)[1]:.3e}; |Delta {k} - Delta cont3| {abs(float((dk - d0).mid())):.3e}")
