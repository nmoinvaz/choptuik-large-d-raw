"""#1102: where ellrs's block 12 spends its time (one evaluation), beside one DDEll RK4 stage in Python.
usage: profile_b12.py MATTER_DIR STUB STATE D LAM THREADS [--lu=scipy|native] [--py_stage=1]"""
import sys, os, time, json
sys.path.insert(0, sys.argv[1])
import numpy as np
from ell_fastm import load_system
import ell_ddm, ell_b12rs
from ell_ddm import DT
import ddnp as dd
args = [a for a in sys.argv[2:] if not a.startswith("--")]
opts = dict(a[2:].split("=", 1) for a in sys.argv[2:] if a.startswith("--"))
stub, st, D, lam, T = args[0], args[1], float(args[2]), float(args[3]), int(args[4])
lu = opts.get("lu", "scipy")
S, z, rec, same, msg = load_system(stub, st, D)
print(msg, flush=True)
E = ell_ddm.DDEll(S)
R = ell_b12rs.RsB12(S, E, threads=T)
steps = len(R.e)
nf = R.nf
print(f"k_c {S.kc}: N {S.N}, n_odd {S.n_odd}, n_even {S.n_even}, nf {nf}, horizon steps {steps}; ellrs threads {R.R.threads}, lu {lu}", flush=True)
R.R.profile(True)
t0 = time.time()
R.block12(z, lam, lu)
wall = time.time() - t0
p = R.R.profile(True)
ser, rk = {k[7:]: v for k, v in p.items() if k.startswith("series_")}, {k[3:]: v for k, v in p.items() if k.startswith("rk_")}
ns = 4 * steps
rk_cpu = rk["wall"]
rk_ew = rk_cpu - rk["slice"] - rk["gemm"] - rk["combine"]
out = dict(kc=S.kc, D=D, lam=lam, threads=R.R.threads, lu=lu, steps=steps, nf=nf, N=S.N, wall=wall, series=ser, rk=rk,
           rk_wall=wall - ser["wall"], rk_elementwise_cpu=rk_ew)
print(f"one evaluation: {wall:.2f} s wall = series {ser['wall']:.2f} s + RK4 {wall - ser['wall']:.2f} s", flush=True)
print(f"  series CPU: Ozaki slicing {ser['slice']:.2f} s, f64 products {ser['gemm']:.2f} s ({ser['madd']:.3g} madd), "
      f"level sums {ser['combine']:.2f} s, f64 LU (factor + solves) {ser['lu']:.2f} s", flush=True)
print(f"  RK4 CPU (chunks summed) {rk_cpu:.2f} s: Ozaki slicing {rk['slice']:.2f} s, f64 products {rk['gemm']:.2f} s "
      f"({rk['madd']:.3g} madd, {rk['madd'] / max(rk['gemm'], 1e-9) / 1e9:.2f} Gmadd/s per thread), level sums "
      f"{rk['combine']:.2f} s, elementwise double-double and copies {rk_ew:.2f} s", flush=True)
print(f"  per RK4 stage ({ns} stages): wall {(wall - ser['wall']) / ns * 1e3:.1f} ms; CPU {rk_cpu / ns * 1e3:.1f} ms = products "
      f"{rk['gemm'] / ns * 1e3:.1f} + slicing {rk['slice'] / ns * 1e3:.1f} + level sums {rk['combine'] / ns * 1e3:.1f} + "
      f"elementwise {rk_ew / ns * 1e3:.1f} ms", flush=True)
if opts.get("py_stage", "1") == "1":
    # one DDEll.rhs on a dual state of block 12's shapes (values: node 11's state; tangents: nf random rows)
    blocks, offs = S._block_list()
    no, ne = S.n_odd, S.n_even
    c0 = offs[2 + 5 * 11]
    g = np.random.default_rng(1)
    s = []
    o = c0
    for sz in (no, no, ne, ne, no):
        s.append(DT(dd.R(z[None, o:o + sz].copy()), dd.R(g.standard_normal((nf, sz)) * 1e-3)))
        o += sz
    E.om = 2 * np.pi / z[-1]; E.lam = lam
    with np.errstate(all="ignore"):
        tt = []
        for _ in range(2):
            t0 = time.time(); E.rhs(0.93, s); tt.append(time.time() - t0)
    E.lam = 0.0
    out["py_stage"] = min(tt)
    print(f"  DDEll.rhs, one stage in Python on the same shapes: {min(tt) * 1e3:.0f} ms (best of 2)", flush=True)
if "out" in opts:
    open(opts["out"], "a").write(json.dumps(out) + "\n")
