#!/usr/bin/env python3
"""#682: Delta_full - Delta_held at the integer D the chain reached, and the control (the base polish against the stored state).
usage: python deltas_682.py          (from this folder; uses the venv's mpmath-free arithmetic through python-flint at 400 bits)
Delta of a saved state = the sum of the last entry of each of its parts (hp's convention, summed exactly in arb). Delta_full: chain/anm_pin13_D<D>.0000.npz. Delta_held: the stage checkout's T138-win2/chain/anm_pin3_D<D>.0000.npz
(T138-win2, the held chain of the 1/n fit). The base: I642-win/released_kf13_D77.0000.npz (the stored state) against the chain's polished base (--save_base 0 here, so the control is read from the log's first Newton step, dDelta +7.73e-48)."""
import os

import flint
import numpy as np

flint.ctx.prec = 400
arb = flint.arb
HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = r"C:\Users\nathan\Source\choptuik-large-d-raw-stage"


def delta(path):
    d = np.load(path, allow_pickle=True)
    parts = [k for k in ("zh", "zl", "z2", "z3") if k in d.files]
    s = arb(0)
    for k in parts:
        s += arb(float(d[k][-1]))
    return s, parts


def main():
    base, parts = delta(os.path.join(HERE, "..", "I642-win", "released_kf13_D77.0000.npz"))
    print(f"stored base, D 77 (I642-win), parts {parts}: Delta {base.str(36, radius=False)}")
    kf7 = {80: 3.665e-14, 100: 9.694e-13}
    prev = {74: 4.623e-16, 75: 1.252e-15, 76: 2.432e-15, 77: 4.062e-15}
    print("\n| D | Delta_full (chain, this task) | Delta_held (T138-win2 chain) | Delta_full - Delta_held | #641's kfreeze 7 shift | #642 full release at integer D |\n|---|---|---|---|---|---|")
    for D in (78, 79, 80):
        f = os.path.join(HERE, "chain", f"anm_pin13_D{D}.0000.npz")
        h = os.path.join(STAGE, "T138-win2", "chain", f"anm_pin3_D{D}.0000.npz")
        if not (os.path.exists(f) and os.path.exists(h)):
            print(f"| {D} | {'missing' if not os.path.exists(f) else ''} | {'missing' if not os.path.exists(h) else ''} | | | |")
            continue
        a, pa = delta(f)
        b, pb = delta(h)
        diff = float((a - b).mid())
        print(f"| {D} | {a.str(30, radius=False)} | {b.str(30, radius=False)} | {diff:+.4e} | {('%+.3e' % kf7[D]) if D in kf7 else 'not measured at D %d' % D} | {('%+.3e' % prev[D]) if D in prev else '(D 74 to 77: +4.623e-16, +1.252e-15, +2.432e-15, +4.062e-15)'} |")


if __name__ == "__main__":
    main()
