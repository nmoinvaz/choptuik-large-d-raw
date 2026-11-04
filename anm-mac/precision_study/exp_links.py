"""Which part of the horizon block's jet derivative carries the float64-level error (anm_run --probe 2's rows 649-654)?
At the base D 82.1642 (run_trend_pin3_qd6), dF/dD by the double-double jet (Solver.residual_jet, order 1) against
quad-double central differences in D (Solver.residual_q at D +- e, e = 2^-42, 2^-43, Richardson), in two arithmetic
forms of the same model: horizon_alpha 0 (the chain's) and 1 (the horizon series in alpha = a - 1). The two forms are
the same function, so the quad-double references must agree to quad-double rounding (the control), and a difference of
the jet's error between the forms is rounding in the horizon series. Read-only; one thread."""
import json, os, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import numpy as np
import mpmath as mp
from hpkernel.driver import make_solver, load_q, qparts
from multidouble import dd_add, dd_scale
from pinning import qd_axpy

mp.mp.dps = 50
RAW = "/Users/nathan/Source/choptuik-large-d-raw"
state = sys.argv[1] if len(sys.argv) > 1 else "anm-mac/run_trend_pin3_qd6/anm_pin3_D82.1642.npz"
zq, m = load_q(os.path.join(RAW, state))
zq = tuple(np.ascontiguousarray(p) for p in zq)
zh, zl = zq[0], zq[1]
D, M, nodes = mp.mpf(m["D_str"]), int(m["M"]), list(m["nodes"])
kt, kc, ks, kf = m["kt"], m["kc"], m["ks"], 3
mk = lambda Dx, al: make_solver(Dx, M, nodes=nodes, kt=kt, kc=kc, ks=ks, threads=1, kfreeze=kf, horizon_alpha=al)
s0 = mk(D, 0)
t = time.time(); segs = s0.plan(zh, zl, 1e-32, 0.05); s0.set_segs(segs); print(f"plan {time.time()-t:.1f} s", flush=True)
K = len(nodes); L = len(zh); hb = K * 4 * M
c4 = lambda v: tuple(np.ascontiguousarray(np.asarray(p)) for p in v)

def fd_D(al, e):
    Ks = []
    for sg in (1.0, -1.0):
        sx = mk(D + sg * mp.mpf(e), al); sx.set_segs(segs)
        Ks.append(sx.residual_q(*zq))
    d = qd_axpy(-1.0, *c4(Ks[1]), *c4(Ks[0]))
    return dd_scale(np.asarray(d[0]), np.asarray(d[1]), 0.5 / e)

def rich(f, e):
    r1, r2 = f(e), f(e / 2)
    return dd_add(*dd_scale(r2[0], r2[1], 4.0 / 3.0), *dd_scale(r1[0], r1[1], -1.0 / 3.0))

out = {}
for al in (0, 1):
    s = mk(D, al); s.set_segs(segs)
    t = time.time(); Hs, Ls = s.residual_jet([zh], [zl], 2, 0); tj = time.time() - t
    jet = (np.asarray(Hs[1]), np.asarray(Ls[1]))
    t = time.time(); fd = rich(lambda e: fd_D(al, e), 2.0 ** -42); tf = time.time() - t
    out[al] = (jet, fd)
    print(f"alpha {al}: jet {tj:.1f} s, central differences {tf:.1f} s", flush=True)
v = lambda p: np.asarray(p[0]) + np.asarray(p[1])
dd_diff = lambda a, b: v(dd_add(np.asarray(a[0]), np.asarray(a[1]), -np.asarray(b[0]), -np.asarray(b[1])))
fd0, fd1 = out[0][1], out[1][1]
ctl = np.abs(dd_diff(fd0, fd1))
print(f"control: quad-double references of the two forms differ by max {ctl.max():.3e} (|dF/dD| max {np.abs(v(fd0)).max():.3e})")
err0 = dd_diff(out[0][0], fd0); err1 = dd_diff(out[1][0], fd1); jj = dd_diff(out[0][0], out[1][0])
val = v(fd0)
rows = list(range(hb, hb + 4 * M))
print("row  field idx   dF/dD          err(alpha0)/|val|  err(alpha1)/|val|  jet0-jet1 / |val|")
for i in list(range(hb, hb + M)) + [hb + 3 * M + 31]:
    print(f"{i:4d}  {(i - hb) // M}  {(i - hb) % M:3d}  {val[i]:+.4e}  {err0[i] / abs(val[i]):+.3e}  {err1[i] / abs(val[i]):+.3e}  {jj[i] / abs(val[i]):+.3e}")
blk = slice(hb, L - 1)
print(f"horizon block: max |err| alpha0 {np.abs(err0[blk]).max():.3e} (row {hb + int(np.argmax(np.abs(err0[blk])))}), alpha1 {np.abs(err1[blk]).max():.3e}; "
      f"other blocks: alpha0 {np.abs(err0[:hb]).max():.3e}, alpha1 {np.abs(err1[:hb]).max():.3e}")
rel0 = np.abs(err0[blk]) / np.maximum(np.abs(val[blk]), 1e-300); rel1 = np.abs(err1[blk]) / np.maximum(np.abs(val[blk]), 1e-300)
print(f"horizon block, median relative error: alpha0 {np.median(rel0):.2e}, alpha1 {np.median(rel1):.2e}")
np.savez("/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/agentA/exp_links.npz",
         err0=err0, err1=err1, val=val, jj=jj, ctl=ctl)
