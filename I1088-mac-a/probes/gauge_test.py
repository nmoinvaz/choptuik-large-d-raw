"""Which field's inconsistency breaks the ladder? The chain's state at D 245.5586 with its last node's field F (p, m, a
or c) moved by rel times a smooth tau profile (1 + 0.5 cos theta, all eight parts' sum moved), then the octo-double
ladder (jump.OLadder) from the state's own horizon data. Printed: each rung's start and end |R|, and the inner
rungs' target mismatch of the state's own data in rows p, m, a, c. The hypothesis to test: a c move at the node
(the gauge c(tau, 1) = 1) breaks the ladder at its second rung, as the D 250 guess's did, and p, m, a moves of the same
size do not.

    python3 gauge_test.py STATE.npz FIELD REL
"""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
from jump import OLadder, D_mp
from octo_corrector import load_o, o8
from multidouble import od_axpy

z, meta = load_o(sys.argv[1])
field, rel = sys.argv[2], float(sys.argv[3])
D = D_mp(meta)
M, K = meta["M"], len(meta["nodes"])
lad = OLadder(meta, D, threads=2, verbose=True)
o = lad.rs.off
nk = o["node"](K - 1)
f = "pmac".index(field)
th = np.pi * np.arange(M) / M
prof = 1 + 0.5 * np.cos(th)
zv = np.asarray(z[0]) + np.asarray(z[1])
pert = np.zeros(len(zv))
sl = slice(nk + f * M, nk + (f + 1) * M)
pert[sl] = rel * prof * np.where(np.abs(zv[sl]) > 0, np.abs(zv[sl]), 1.0)
zero = np.zeros(len(zv))
zp = o8(od_axpy(1.0, pert, *([zero] * 7), *z))
print(f"D {meta['D']}: last node's {field} moved by {rel:g} (relative, smooth); rungs log10 G "
      f"{', '.join(f'{d:.1f}' for d in lad.decs)}", flush=True)
t = time.time()
zz, info = lad.project(zp)
print(f"ladder {'ok' if info['ok'] else 'FAILED'} in {info['s']} s: " +
      "; ".join(f"G 1e{r['G']}: {r['R0']:.2e} -> {r['R']:.2e}" for r in info["rungs"] if "R0" in r), flush=True)
