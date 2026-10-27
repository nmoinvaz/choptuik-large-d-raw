"""T84: the full system (kfreeze 13) converged in quad-double from the polished pinned states of T73 and T75 (both
pins' states as independent starts), where notes 12.4's basin is open. Prints Delta per start.

    python3 qd_fullleg.py OUT.jsonl STATE.npz [STATE.npz ...] [--threads N]
"""
import json
import os
import sys
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from hpkernel.driver import load_q, make_solver, newton_qd, qmax, save_q  # noqa: E402

args = list(sys.argv[1:])
threads = 2
if "--threads" in args:
    i = args.index("--threads"); threads = int(args[i + 1]); del args[i:i + 2]
out, paths = args[0], args[1:]
for path in paths:
    z, m = load_q(path)
    D, M = m["D"], m["M"]
    s = make_solver(D, M, nodes=list(m["nodes"]), kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads, kfreeze=13)
    s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
    t0 = time.time()
    zq, hist, conv = newton_qd(s, z, tol=1e-50, it_max=10, verbose=False)
    f = hist[-1].get("F_new", hist[-1]["F"])
    print(f"{os.path.basename(path)}: D {D}: {'converged' if conv else 'NOT converged'}, |F| {f:.2e}, {len(hist)} steps, "
          f"{time.time() - t0:.0f} s, Delta {zq[0][-1]:.17f} {zq[1][-1]:+.6e} {zq[2][-1]:+.3e}", flush=True)
    with open(out, "a") as fh:
        fh.write(json.dumps(dict(state=os.path.basename(path), D=D, conv=conv, F=f, steps=len(hist),
                                 Delta_q=[float(p[-1]) for p in zq], seconds=round(time.time() - t0), hist=hist)) + "\n")
    if conv:
        save_q(path[:-4] + "_full.npz", zq, dict(m, solver="qd", kfreeze=13))
