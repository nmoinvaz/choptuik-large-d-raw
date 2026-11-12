#!/usr/bin/env python3
"""Where commit 2 (kfreeze on multishoot's projected rows) changes the residual: the dd, qd and od residuals at
kfreeze states, dumped by one build and compared between two (#523).

    PYTHONPATH=<site>:HPDIR python3 kf_rows.py dump RAWDIR OUT.npz
    python3 kf_rows.py cmp A.npz B.npz       # rows that differ, and the size of the change on the frozen rows
"""
import os
import sys

import numpy as np

STATES = ["anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz", "I461-win2/crawlG/anm_pin3_D232.6312.npz",
          "I461-win2/crawlJ/anm_pin3_D242.3642.npz"]


def dump(raw, out):
    from hpkernel.driver import make_solver
    from octo_corrector import load_o
    rec = {}
    for i, st in enumerate(STATES):
        p = os.path.join(raw, st)
        if not os.path.exists(p):
            continue
        z8, m = load_o(p)
        z8 = [np.ascontiguousarray(np.array(q, dtype=float)) for q in z8]
        D = m.get("D_str", repr(float(m["D"])))
        s = make_solver(D, int(m["M"]), nodes=list(m["nodes"]), kt=m.get("kt", 36), kc=m.get("kc", 146), ks=m.get("ks", 130),
                        threads=2, kfreeze=m.get("kfreeze", 3))
        s.set_segs(m["segs"] if m.get("segs") else s.plan(z8[0], z8[1], 1e-32, 0.05))
        rec[f"s{i}_meta"] = np.array([int(m["M"]), len(m["nodes"])])
        rec[f"s{i}_dd"] = np.array(s.residual(z8[0], z8[1]))
        rec[f"s{i}_qd"] = np.array(s.residual_q(*z8[:4]))
        rec[f"s{i}_od"] = np.array(s.residual_o(z8))
        print(st, "done", flush=True)
    np.savez(out, **rec)


def cmp(a, b):
    A, B = np.load(a), np.load(b)
    for i, st in enumerate(STATES):
        if f"s{i}_meta" not in A.files:
            continue
        M, K = A[f"s{i}_meta"]
        fr = np.arange(4 * M * K, 4 * M * K + M)
        for p in ("dd", "qd", "od"):
            x, y = A[f"s{i}_{p}"], B[f"s{i}_{p}"]
            rows = np.nonzero((x.view(np.uint64) != y.view(np.uint64)).any(axis=0))[0]
            outside = np.setdiff1d(rows, fr)
            # the change on the frozen rows, from the parts summed in f64 pairs (hi, then the rest)
            dx = np.abs((x[0] - y[0]) + (x[1:].sum(0) - y[1:].sum(0)))[fr]
            print(f"{st} {p}: {len(rows)} rows differ, {len(outside)} outside the frozen rows {fr[0]}..{fr[-1]}; "
                  f"max |change| on them {dx.max():.2e}, max |F| there {np.abs(x[0][fr]).max():.2e}")


if __name__ == "__main__":
    if sys.argv[1] == "dump":
        dump(sys.argv[2], sys.argv[3])
    else:
        cmp(sys.argv[2], sys.argv[3])
