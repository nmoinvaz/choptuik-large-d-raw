"""where the residual after the full octo-double Newton step at 188.0246 sits (step0_D188_steps.npz from step0_step.py):
max |F| by block and field, and the step's largest entries by block"""
import os, sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e/hp")
import numpy as np, mpmath as mp
mp.mp.dps = 50
from hpkernel.driver import load_q
from multidouble import od_axpy
from octo_corrector import o8, o8_of_q, pinned_o

A = "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/octo_agent"
z4, meta = load_q("/Users/nathan/Source/choptuik-large-d-raw/T129-win2/chain/anm_pin3_D188.0246.npz")
z4 = o8(z4)
s, sp, sq, so = pinned_o(meta, z4, threads=1)
d = np.load(os.path.join(A, "step0_D188_steps.npz"))
M, K = 32, len(meta["nodes"])
for name in ("od", "qd"):
    dz = o8([d[f"{name}_{q}"] for q in range(8)])
    F = so.residual_o(o8(od_axpy(1.0, *dz, *o8_of_q(z4))))
    Fv = np.abs(F[0] + F[1])
    dv = np.abs(dz[0] + dz[1])
    print(f"{name}: after the full step max|F| {Fv.max():.2e}; by row block (residual blocks of 4M rows: p, m, a, c; block K the horizon block, then the phase row):")
    edges = [4 * M * i for i in range(K + 2)]
    edges[-1] = len(Fv)
    for b in range(len(edges) - 1):
        lo, hi = edges[b], edges[b + 1]
        sub = Fv[lo:hi]
        fields = [float(sub[q * M:(q + 1) * M].max()) for q in range(max(1, (hi - lo) // M))]
        print(f"  rows [{lo}, {hi}): max {sub.max():.2e}; by field of M: " + " ".join(f"{x:.1e}" for x in fields)
              + f"; step there max {dv[lo:hi].max():.1e}")
