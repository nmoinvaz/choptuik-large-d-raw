"""probe for check (a)'s start: the residual of the planted start at 180.5246 and of its projection, at rel in argv"""
import os, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e/hp")
import numpy as np, mpmath as mp
mp.mp.dps = 50
from hpkernel.driver import load_q, qd_axpy
from reseed import Reseeder
from octo_corrector import ElimO, o8, o8_of_q, omax, pinned_o

raw = "/Users/nathan/Source/choptuik-large-d-raw"
z4, meta = load_q(os.path.join(raw, "T129-win2/chain/anm_pin3_D180.5246.npz"))
z4 = o8(z4)
D = mp.mpf(meta["D_str"])
s, sp, sq, so = pinned_o(meta, z4, threads=3)
rs = Reseeder(meta, D, threads=3, qd=True)
n = rs.off["node"](rs.K - 1) if os.environ.get("EXCL_LAST") else rs.off["mh"]
for rel in [float(x) for x in sys.argv[1:]]:
    rng = np.random.default_rng(1)
    r = rng.uniform(0.5, 1.0, n) * rng.choice([-1.0, 1.0], n)
    dz = np.zeros(len(z4[0]))
    dz[:n] = rel * r * z4[0][:n]
    zero = np.zeros(len(dz))
    zs = o8(qd_axpy(1.0, dz, zero, zero, zero, *z4))
    F = so.residual_o(o8_of_q(zs))
    Fv = np.abs(F[0] + F[1])
    t0 = time.time()
    el = ElimO(so, rs)
    zp = el.project(o8_of_q(zs))
    print(f"rel {rel:.0e}: start max|F| {Fv.max():.2e} (row {int(np.argmax(Fv))}), projected {el.counts} max|F| {omax(so.residual_o(zp)):.2e}, "
          f"{time.time() - t0:.0f} s", flush=True)
