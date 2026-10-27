"""T84: the quad-double Newton on the full system (kfreeze 13) with p1's harmonics from KMIN to 13 frozen at the
state's values, exactly: the frozen directions are the band fields of those harmonics (cos and sin), orthonormalized,
passed to driver.newton_qd as V. The near-null directions of the full system are those harmonics (qd_weak.py); the
numerical junk subspace of junk_subspace_q is an f64 Rayleigh-Ritz on ten orders of magnitude and leaked.

    python3 qd_freezeh.py STATE.npz KMIN [threads]        (KMIN 15: nothing frozen, the plain Newton)
"""
import json
import os
import sys
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
from hpkernel.driver import load_q, make_solver, newton_qd, qmax, save_q  # noqa: E402
from pinning import band_field  # noqa: E402

path, kmin = sys.argv[1], int(sys.argv[2])
threads = int(sys.argv[3]) if len(sys.argv) > 3 else 2
z, m = load_q(path)
D, M = m["D"], m["M"]
s = make_solver(D, M, nodes=list(m["nodes"]), kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads, kfreeze=13)
s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
L = s.size
ks = list(range(kmin, 14, 2))
cols = []
for k in ks:
    for co in ((1.0, 0.0), (0.0, 1.0)):
        hh, hl = band_field([co], [k], M)
        v = np.zeros(L); v[:M] = np.asarray(hh) + np.asarray(hl)
        cols.append(v)
V = np.linalg.qr(np.array(cols).T)[0] if cols else None
print(f"{os.path.basename(path)}: D {D}, nodes {m['nodes']}, full system; frozen p1 harmonics {ks} ({0 if V is None else V.shape[1]} directions); "
      f"start |F| {qmax(s.residual_q(*z)):.2e}", flush=True)
t0 = time.time()
zq, hist, conv = newton_qd(s, z, tol=1e-50, it_max=14, verbose=True, V=V)
f = hist[-1].get("F_new", hist[-1]["F"])
print(f"freeze >= {kmin}: {'converged' if conv else 'NOT converged'}, |F| {f:.2e}, {len(hist)} steps, {time.time() - t0:.0f} s, "
      f"Delta {zq[0][-1]:.17f} {zq[1][-1]:+.6e} {zq[2][-1]:+.3e} {zq[3][-1]:+.3e}", flush=True)
with open(path[:-4] + f"_freezeh{kmin}.jsonl", "a") as fh:
    fh.write(json.dumps(dict(state=os.path.basename(path), D=D, kmin=kmin, conv=conv, F=f, steps=len(hist),
                             Delta_q=[float(p[-1]) for p in zq], seconds=round(time.time() - t0), hist=hist)) + "\n")
if conv:
    save_q(path[:-4] + f"_freezeh{kmin}.npz", zq, dict(m, solver="qd", kfreeze=13, frozen_harmonics=ks))
