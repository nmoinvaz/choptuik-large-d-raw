"""Check of the Moebius series' products with z by t2v's two-term recurrence (form_s.rs ae0b5453, #1088): at a
form-S state, the residual's horizon block in octo-double with the recurrence (mutate 0), with the full Cauchy sums
(mutate 54, the reference) and with the control (mutate 53, the recurrence's coefficient a t_l times 1 + 2^-60), and
each residual's time. Bars, written before the run: |recurrence - Cauchy| <= 1e-100 on every horizon row; the control
differs from the Cauchy sums by more than 1e-30.

    HP_DIR=<hp> python3 zcheck.py STATE.npz THREADS [KS]
"""
import os, sys, time
sys.path.insert(0, os.environ.get("HP_DIR", "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp"))
import numpy as np
import mpmath as mp
from form_s import make_solver_s, blocks_s, ks_mob
from octo_corrector import load_o
from multidouble import od_axpy

z8, meta = load_o(sys.argv[1])
thr = int(sys.argv[2])
M, nodes = meta["M"], meta["nodes"]
K = len(nodes)
with mp.workdps(60):
    D = mp.mpf(meta["D_str"])
ks = int(sys.argv[3]) if len(sys.argv) > 3 else (meta["ks"] if meta.get("hmob") else ks_mob(float(D)))
s = make_solver_s(D, M, nodes, kt=meta["kt"], kc=meta["kc"], ks=ks, threads=thr, segs=meta["segs"], mob=8.0)
r0 = K * 3 * M
out = {}
for nm, mu in (("recurrence", 0), ("Cauchy", 54), ("control", 53)):
    t0 = time.time()
    F = s.residual_s([np.ascontiguousarray(p) for p in z8], mu)
    out[nm] = [np.ascontiguousarray(np.asarray(p)[r0:r0 + 3 * M]) for p in F]
    print(f"  {nm} (mutate {mu}): horizon block {blocks_s(F, M, K)[K]:.3e} ({time.time() - t0:.1f} s)", flush=True)


def diff(a, b):
    return float(np.abs(np.asarray(od_axpy(-1.0, *out[a], *out[b])[0])).max())


d1, d2 = diff("Cauchy", "recurrence"), diff("Cauchy", "control")
print(f"D {float(D):g}, ks {ks}: |recurrence - Cauchy| {d1:.2e} ({'PASS' if d1 <= 1e-100 else 'FAIL'} against 1e-100); "
      f"|control - Cauchy| {d2:.2e} ({'fires' if d2 > 1e-30 else 'DOES NOT FIRE'} against 1e-30)", flush=True)
