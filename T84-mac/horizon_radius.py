"""T84, investigation 2: the horizon series' radius on and off the solution against D. At each saved state, with the
state held and D moved by dD (0, 1e-8, 1e-6, 1e-4, 1e-2), the horizon series' terms at u0, t_k = |c_k| u0^k (largest
over fields and tau points), their growth per order over the last 40 orders, r = (t_K / t_{K-40})^(1/40), and the
radius they imply, R = u0 / r (R < u0: the series diverges at the matching node). dD = 0 is the solution's own
radius (BEYOND_LIGHT_CONE 2.3: 0.75 at D 60 by root tests); dD > 0 the radius for data off the solution by about
4e-5 dD (12.2 estimated 0.22 at D 73 for dD 1e-4..1e-2).

    python3 horizon_radius.py OUT.jsonl STATE.npz [STATE.npz ...] [--threads N]
"""
import json
import os
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from hpkernel.driver import load, make_solver  # noqa: E402

args = list(sys.argv[1:])
threads = 2
if "--threads" in args:
    i = args.index("--threads"); threads = int(args[i + 1]); del args[i:i + 2]
out, paths = args[0], args[1:]
print(f"{'D':>8} {'u0':>5} {'ks':>4} " + " ".join(f"{'R(dD=' + f'{h:.0e}' + ')':>12}" for h in (0.0, 1e-8, 1e-6, 1e-4, 1e-2)) + "   terms at K (dD 0, 1e-4)", flush=True)
for path in paths:
    zh, zl, m = load(path)
    D, M, nodes = m["D"], m["M"], list(m["nodes"])
    kc, ks = m.get("kc", 146), m.get("ks", 130)
    u0 = 1.0 - nodes[-1]
    kf = 13 if D >= 35 else None
    s0 = make_solver(D, M, nodes=nodes, kt=m.get("kt", 36), kc=kc, ks=ks, threads=threads, kfreeze=kf)
    s0.set_segs(s0.plan(zh, zl, 1e-32, 0.05))
    segs = s0.get_segs()
    rec = dict(state=os.path.basename(path), D=D, u0=u0, ks=ks, kc=kc, R={}, tK={})
    Rs, tKs = [], []
    for h in (0.0, 1e-8, 1e-6, 1e-4, 1e-2):
        s = make_solver(D + h, M, nodes=nodes, kt=m.get("kt", 36), kc=kc, ks=ks, threads=threads, kfreeze=kf)
        s.set_segs(segs)
        hh, hl = s.series(zh, zl, 1, True)                 # c_k sigma^k, sigma = series_scale(u0)
        sig = s.series_scale(1)
        c = np.abs(np.asarray(hh) + np.asarray(hl)).reshape(-1, 4, M).max(axis=(1, 2))
        k = np.arange(len(c))
        t = c * (u0 / sig) ** k                              # the terms at u0
        K = len(t) - 1
        good = (t[K] > 0) and (t[K - 40] > 0) and np.isfinite(t[K]) and np.isfinite(t[K - 40])
        r = (t[K] / t[K - 40]) ** (1 / 40) if good else float("nan")
        R = u0 / r if good and r > 0 else float("nan")
        rec["R"][f"{h:.0e}"] = R
        rec["tK"][f"{h:.0e}"] = float(t[K]) if np.isfinite(t[K]) else None
        Rs.append(R); tKs.append(t[K])
    print(f"{D:8.4f} {u0:5.2f} {ks:4d} " + " ".join(f"{R:12.3f}" for R in Rs) + f"   {tKs[0]:.1e}, {tKs[3]:.1e}", flush=True)
    with open(out, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
