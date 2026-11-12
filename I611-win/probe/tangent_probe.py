#!/usr/bin/env python3
"""#611: where does scan_qd.py's tangent predictor go non-finite on win (venv-t151's hpkernel, a build before #523)?
usage: python tangent_probe.py          (cwd = the worktree's hp/, as for scan_qd.py; ~3 min at 3 threads)
Runs scan_qd.main() on the converged kf 13 D 50.007491 state with D_END 50.017491 and the tangent predictor, with
driver.tangent_q replaced by a copy of its body that prints, at each stage, whether the arrays are finite, and then exits."""
import os
import sys

import numpy as np

sys.path.insert(0, os.getcwd())
import scan_qd  # noqa: E402

RAW = r"C:\Users\nathan\Source\choptuik-large-d-raw\I611-win"


def fin(name, parts):
    parts = [np.asarray(v) for v in parts]
    print(f"  {name}: finite {[bool(np.isfinite(v).all()) for v in parts]}, max|.| {[float(np.nanmax(np.abs(v))) for v in parts]}", flush=True)


def probe(s, s_of_D, D, z, h=1e-10):
    print(f"tangent_q probe at D = {D}", flush=True)
    fin("z", z)
    Dp, Dm = D + h, D - h
    fs = []
    for Dx in (Dp, Dm):
        sx = s_of_D(Dx)
        sx.set_segs(s.get_segs())
        f = sx.residual_q(*z)
        fin(f"residual_q at D {Dx!r}", f)
        fs.append(f)
    g = tuple(np.ascontiguousarray(v / (Dp - Dm)) for v in scan_qd.qd_axpy(-1.0, *fs[1], *fs[0]))
    fin("g = dF/dD", g)
    s.newton_q(*z)
    print("  newton_q at z: done", flush=True)
    t = s.qlu_solve(*g)
    fin("t = qlu_solve(g)", t)
    sys.exit(0)


scan_qd.tangent_q = probe
sys.argv = ["scan_qd.py", os.path.join(RAW, "probe", "qd_probe.jsonl"), os.path.join(RAW, "kf13_D50_D50.007491.npz"), "50.017491",
            "--kfreeze", "13", "--threads", "3", "--tag", "probe", "--predictor", "tangent", "--dD", "0.01"]
scan_qd.main()
