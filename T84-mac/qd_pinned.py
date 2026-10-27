"""T84: the quad-double Newton on the pinned system of T73-T85 (hp/pinning.py's PinnedSolver in quad-double): p1's
harmonics in (PIN, 13] held at the state's own values, the solver built with kfreeze PIN, the band's field c subtracted
from the horizon block's p rows of the residual and J^-1 c added to the step. The pinned double-double system has
pivots 1e-7 (0.7 layout) to 1e-5 (0.8) where the full system is singular to 1e-29.

    python3 qd_pinned.py STATE.npz [PIN] [threads]
"""
import json
import os
import sys
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
from hpkernel import qd_axpy  # noqa: E402
from hpkernel.driver import load_q, make_solver, newton_qd, qmax, save_q  # noqa: E402
from pinning import band_coeffs, band_field  # noqa: E402


class PinnedQ:
    """PinnedSolver for the quad-double methods: residual_q and newton_q see F - c, the step gains J^-1 c"""

    def __init__(self, s, M, hh, hl):
        self.s = s
        L = s.size
        K = (L - 1) // (4 * M) - 1
        self.c = [np.zeros(L) for _ in range(4)]
        self.c[0][K * 4 * M:K * 4 * M + M] = hh
        self.c[1][K * 4 * M:K * 4 * M + M] = hl
        self.c = tuple(np.ascontiguousarray(v) for v in self.c)
        self.zero = np.zeros(L)

    def __getattr__(self, name):
        return getattr(self.s, name)

    def residual_q(self, *z):
        F = self.s.residual_q(*z)
        return qd_axpy(-1.0, *self.c, *[np.ascontiguousarray(np.asarray(p)) for p in F])

    def newton_q(self, *z, mutate=0):
        st = self.s.newton_q(*z, mutate=mutate)
        x = self.s.qlu_solve(*self.c)
        d = qd_axpy(1.0, *[np.ascontiguousarray(np.asarray(p)) for p in x], *[np.ascontiguousarray(np.asarray(p)) for p in st[:4]])
        F = qd_axpy(-1.0, *self.c, np.ascontiguousarray(np.asarray(st[4])), np.ascontiguousarray(np.asarray(st[5])), self.zero, self.zero)
        return (*d, F[0], F[1] + F[2] + F[3], st[6], st[7])


path = sys.argv[1]
pin = int(sys.argv[2]) if len(sys.argv) > 2 else 7
threads = int(sys.argv[3]) if len(sys.argv) > 3 else 2
z, m = load_q(path)
D, M = m["D"], m["M"]
ks = list(range(pin + 2, 14, 2))
co = np.ravel(band_coeffs(z[0][:M], z[1][:M], M, ks))
hh, hl = band_field([(co[2 * i], co[2 * i + 1]) for i in range(len(ks))], ks, M)
s0 = make_solver(D, M, nodes=list(m["nodes"]), kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads, kfreeze=pin)
s0.set_segs(s0.plan(z[0], z[1], 1e-32, 0.05))
s = PinnedQ(s0, M, np.asarray(hh), np.asarray(hl))
print(f"{os.path.basename(path)}: D {D}, nodes {m['nodes']}, pin {pin}, held harmonics {ks} at " + " ".join(f"{np.hypot(co[2*i], co[2*i+1]):.1e}" for i in range(len(ks))), flush=True)
print(f"  start: full-system |F| (kfreeze 13) n/a here; pinned |F| {qmax(s.residual_q(*z)):.2e}, unpinned kfreeze-{pin} |F| {qmax(s0.residual_q(*z)):.2e}, Delta {z[0][-1]:.16f}", flush=True)
t0 = time.time()
zq, hist, conv = newton_qd(s, z, tol=1e-50, it_max=14, verbose=True)
f = hist[-1].get("F_new", hist[-1]["F"])
print(f"pinned (pin {pin}): {'converged' if conv else 'NOT converged'}, |F| {f:.2e}, {len(hist)} steps, {time.time() - t0:.0f} s, "
      f"Delta {zq[0][-1]:.17f} {zq[1][-1]:+.6e} {zq[2][-1]:+.3e} {zq[3][-1]:+.3e}", flush=True)
with open(path[:-4] + f"_pinned{pin}.jsonl", "a") as fh:
    fh.write(json.dumps(dict(state=os.path.basename(path), D=D, pin=pin, conv=conv, F=f, steps=len(hist),
                             Delta_q=[float(p[-1]) for p in zq], seconds=round(time.time() - t0), hist=hist)) + "\n")
if conv:
    save_q(path[:-4] + f"_pinned{pin}.npz", zq, dict(m, solver="qd", pin=pin))
