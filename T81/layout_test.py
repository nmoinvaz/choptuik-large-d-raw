"""T81 layout test (notes/QUAD_DOUBLE.md 12.2). The quad-double D = 73.0 state (conv_pin5_D73.0000, |F| 2.5e-53, nodes
0.3..0.7) gets one node x_last beyond 0.7 (driver.renode, from the horizon series; the old entries keep all four parts),
is converged by driver.newton_qd at D = 73.0, and its blocks' response to D is measured at fixed state and plan, as
blocks_dD.py did for the old layout. Then Newton from that state at D + dD.

Prediction, written before the run: 12.2's growth of 1.34 per order at u0 = 0.3 puts the radius of generic horizon data
near 0.22 in u. So at x_last = 0.75 (u0 = 0.25) the horizon block's response stays explosive (the control), and at
0.8, 0.85, 0.9 (u0 = 0.2, 0.15, 0.1) it becomes linear in dD, about 4e-5 per unit of D like the other blocks, with a
continuation step then converging. Layout agreement: Delta within about 1e-27 of the old layout's (the Taylor plan's
definition of Delta, 12.1).

    python3 layout_test.py OUT.jsonl 0.75,0.8,0.85,0.9 [threads]
"""
import json
import sys
import time

import numpy as np
from hpkernel import qd_axpy
from hpkernel.driver import block_norms, load_q, make_solver, newton_qd, qmax, renode, save_q

R = "/Users/nathan/Source/raw-T81/"
out = sys.argv[1]
threads = int(sys.argv[3]) if len(sys.argv) > 3 else 6
zs, meta = load_q(R + "conv_pin5_D73.0000_D73.000000.npz")
D, M, old = meta["D"], meta["M"], list(meta["nodes"])
kw = dict(kt=meta["kt"], kc=meta["kc"], threads=threads, kfreeze=13)
s_old = make_solver(D, M, nodes=old, ks=meta["ks"], **kw)
s_old.set_segs(s_old.plan(zs[0], zs[1], 1e-32, 0.05))
print(f"old layout {old}: |F| {qmax(s_old.residual_q(*zs)):.2e}, Delta {zs[0][-1]:.17f} {zs[1][-1]:+.6e}", flush=True)


def log(rec):
    with open(out, "a") as fh:
        fh.write(json.dumps(rec) + "\n")


def blocks(s, z):
    F = s.residual_q(*z)
    return [float(v) for v in block_norms(s, F[0], F[1])]


def fmt(b):
    return " ".join(f"{v:.1e}" for v in b)


for xl in [float(x) for x in sys.argv[2].split(",")]:
    new = old + [xl]
    zh, zl = renode(s_old, zs[0], zs[1], old, new, M)
    # lower parts: the old entries' (centre data, old nodes, horizon data and Delta), zero at the new node
    nh = 2 * M + 4 * M * len(old)
    low = [np.concatenate([p[:nh], np.zeros(4 * M), p[nh:]]) for p in (zs[2], zs[3])]
    z = tuple(np.ascontiguousarray(p) for p in (zh, zl, *low))
    s = make_solver(D, M, nodes=new, ks=meta["ks"], **kw)
    s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
    segs = s.get_segs()
    b0 = blocks(s, z)
    print(f"\nx_last {xl} (u0 {1 - xl:.2f}), nodes {new}, L {len(z[0])}: start blocks {fmt(b0)}", flush=True)
    t0 = time.time()
    z, hist, conv = newton_qd(s, z, tol=1e-50, it_max=12, verbose=1)
    f = hist[-1].get("F_new", hist[-1]["F"])
    dd = qd_axpy(-1.0, *(np.array([p[-1]]) for p in zs), *(np.array([p[-1]]) for p in z))
    dDelta = float(dd[0][0] + dd[1][0])
    print(f"x_last {xl}: {'converged' if conv else 'NOT converged'}, |F| {f:.2e} in {len(hist)} steps "
          f"({time.time() - t0:.0f} s), Delta {z[0][-1]:.17f} {z[1][-1]:+.6e}, minus the old layout's {dDelta:+.2e}",
          flush=True)
    rec = dict(x_last=xl, nodes=new, conv=conv, F=f, steps=len(hist), dDelta_layout=dDelta, start_blocks=b0,
               Delta_q=[float(p[-1]) for p in z], hist=hist)
    save_q(R + f"layout_x{xl}_D73.npz", z, dict(meta, nodes=new, solver="qd", source="conv_pin5_D73.0000"))
    # the blocks' response to D at fixed state and plan, and the horizon series' terms at u0
    resp = {}
    for ks in (meta["ks"], 200):
        for h in (0.0, 1e-8, 1e-6, 1e-4, 1e-2):
            sx = make_solver(D + h, M, nodes=new, ks=ks, **kw)
            sx.set_segs(segs)
            resp[f"{ks}:{h:.0e}"] = b = blocks(sx, z)
            print(f"  ks {ks} dD {h:.0e}: blocks {fmt(b)}", flush=True)
        sx = make_solver(D, M, nodes=new, ks=ks, **kw)
        sx.set_segs(segs)
        hh, hl = sx.series(z[0], z[1], 1)
        c = np.abs((hh + hl).reshape(-1, 4, M)).max(axis=(1, 2))
        print(f"  ks {ks} horizon terms c_k u0^k: "
              + " ".join(f"{k}:{c[k] * (1 - xl) ** k:.1e}" for k in range(0, len(c), max(1, len(c) // 10))), flush=True)
    rec["response"] = resp
    # Newton from this state at D + dD (constant predictor, the same plan)
    steps = {}
    if conv:
        for dD in (1e-3, 1e-2, 5e-2):
            sx = make_solver(D + dD, M, nodes=new, ks=meta["ks"], **kw)
            sx.set_segs(segs)
            t0 = time.time()
            zn, hn, cn = newton_qd(sx, z, tol=1e-50, it_max=12, verbose=1)
            fn = hn[-1].get("F_new", hn[-1]["F"])
            steps[f"{dD:.0e}"] = dict(conv=cn, F=fn, steps=len(hn), Delta_q=[float(p[-1]) for p in zn],
                                      seconds=round(time.time() - t0))
            print(f"  step dD {dD:.0e}: {'converged' if cn else 'NOT converged'}, |F| {fn:.2e} in {len(hn)} steps "
                  f"({time.time() - t0:.0f} s), Delta {zn[0][-1]:.17f} {zn[1][-1]:+.6e}", flush=True)
            if cn:
                save_q(R + f"layout_x{xl}_D{D + dD:.4f}.npz", zn, dict(meta, D=D + dD, nodes=new, solver="qd"))
    rec["steps"] = steps
    log(rec)
