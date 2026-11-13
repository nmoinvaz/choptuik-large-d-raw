#!/usr/bin/env python3
"""#682, second measure of the first-order question (amendment 2): the quad-double max|F| of each saved RAW prediction (pred_pin13_D<D>.npz, before the horizon re-seed) at its own D, with the plan made at the prediction
(Solver.plan, tol 1e-32, hmax 0.05, anm_run's plan) and the full system (kfreeze 13).
usage: OPENBLAS_NUM_THREADS=1 python pred_residual_682.py          (cwd = the worktree's hp/, venv-t151; writes pred_residual_682.txt beside it)
The ladder's predictions are ladder/a1_<k>/pred_pin13_D<77 + a>.npz, the chain's are chain/pred_pin13_D78|79|80.0000.npz. The base's own value (the floor) is the stored D 77 state evaluated the same way.
max|F| = max |F_0 + F_1| of the four-part residual's first two parts, as hp/release_held.py reads it."""
import glob
import os
import sys

sys.path.insert(0, os.getcwd())
import numpy as np  # noqa: E402
from hpkernel.driver import load_q, make_solver  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = HERE


def maxF(path):
    z, m = load_q(path)
    z = [np.ascontiguousarray(np.asarray(p, dtype=float)) for p in z]
    s = make_solver(m.get("D_str", repr(float(m["D"]))), int(m["M"]), nodes=list(m["nodes"]), kt=m.get("kt", 36), kc=m.get("kc", 146), ks=m.get("ks", 130), threads=2, kfreeze=13)
    s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
    F = s.residual_q(*z)
    return float(m["D"]), float(np.abs(np.asarray(F[0]) + np.asarray(F[1])).max())


def main():
    rows = []
    D0, f0 = maxF(os.path.join(RAW, "..", "I642-win", "released_kf13_D77.0000.npz"))
    rows.append((0.0, f0, "the stored D 77 state (floor)"))
    paths = sorted(glob.glob(os.path.join(RAW, "ladder", "a1_*", "pred_pin13_D*.npz"))) + sorted(glob.glob(os.path.join(RAW, "chain", "pred_pin13_D*.npz")))
    for p in paths:
        D, f = maxF(p)
        rows.append((D - 77.0, f, os.path.relpath(p, RAW)))
    rows.sort()
    out = ["| a (= D - 77) | quad-double max abs F of the raw prediction | / floor | file |", "|---|---|---|---|"]
    for a, f, name in rows:
        out.append(f"| {a:g} | {f:.3e} | {f / f0:.1f} | {name} |")
    txt = "\n".join(out)
    print(txt)
    open(os.path.join(RAW, "pred_residual_682.txt"), "w").write(txt + "\n")


if __name__ == "__main__":
    main()
