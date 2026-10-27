"""T84: Newton's basin against D on the saved pinned states of T73 and T75 (folders T73 and T75 of the raw-data
repository). At each state, for the pinned (kfreeze 7) and the full (kfreeze 13) system in quad-double: the LU's
smallest pivot (sigma, a lower bound's proxy), |F| at the state, the Newton step |dz|, |F| after the full step and
c = |F(z + dz)| / |dz|^2 (the second-order constant), and the basin estimate sigma^2 / c that |F| must be below for
Newton to converge (notes/QUAD_DOUBLE.md 12.3). The double-double floor is |F| at the state.

    python3 qd_basin.py OUT.jsonl STATE.npz [STATE.npz ...] [--threads N]
"""
import json
import os
import sys
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from hpkernel import qd_axpy  # noqa: E402
from hpkernel.driver import load_q, make_solver, qmax  # noqa: E402

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pinning import band_coeffs, band_field  # noqa: E402
from qd_pinned import PinnedQ  # noqa: E402

args = [a for a in sys.argv[1:]]
threads = 4
if "--threads" in args:
    i = args.index("--threads"); threads = int(args[i + 1]); del args[i:i + 2]
out, paths = args[0], args[1:]
print(f"{'D':>8} {'system':>7} {'pivot min':>10} {'|F0|':>9} {'|dz|':>9} {'|F(z+dz)|':>10} {'c':>9} {'sigma^2/c':>10} {'F0 in basin?':>13}", flush=True)
for path in paths:
    z, m = load_q(path)
    D, M = m["D"], m["M"]
    for name, kf in (("pinned", 7), ("full", 13)):
        t0 = time.time()
        s = make_solver(D, M, nodes=list(m["nodes"]), kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads, kfreeze=kf)
        s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
        if kf < 13:         # the pinned system of T73-T85: the band of the held harmonics subtracted (qd_pinned.PinnedQ)
            ks = list(range(kf + 2, 14, 2))
            co = np.ravel(band_coeffs(z[0][:M], z[1][:M], M, ks))
            hh, hl = band_field([(co[2 * i], co[2 * i + 1]) for i in range(len(ks))], ks, M)
            s = PinnedQ(s, M, np.asarray(hh), np.asarray(hl))
        st = s.newton_q(*z)
        f0, nd = qmax(st[4:6]), float(np.abs(st[0]).max())
        F1 = s.residual_q(*qd_axpy(1.0, *st[:4], *z))
        f1 = qmax(F1)
        c = f1 / nd ** 2 if nd > 0 else float("nan")
        basin = st[6] ** 2 / c if c > 0 else float("nan")
        rec = dict(state=os.path.basename(path), D=D, system=name, kfreeze=kf, pivot_min=st[6], pivot_max=st[7], F0=f0, dz=nd,
                   F1=f1, c=c, basin=basin, seconds=round(time.time() - t0, 1))
        print(f"{D:8.4f} {name:>7} {st[6]:10.1e} {f0:9.1e} {nd:9.1e} {f1:10.1e} {c:9.1e} {basin:10.1e} {'yes' if f0 < basin else 'no':>13}", flush=True)
        with open(out, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
