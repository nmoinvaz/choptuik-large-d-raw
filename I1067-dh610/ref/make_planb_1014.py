#!/usr/bin/env python3
"""#1014 step B2: a state with its stored plan replaced by a finer one (coordinator's hc, 2026-11-20 about 06:50 UTC: at least 4388 steps).

    make_planb_1014.py SRC DST TOL HMAX MINSTEPS [--mutate]
      plans the state of SRC with s.plan(zh, zl, TOL, HMAX), saves it as DST (vector and every other meta key untouched).
Checks, written before the run: the plan has at least MINSTEPS steps; max|F| on it is at most 1e-26 (the floor class of the lifted states, 1.4e-27); the vector is byte-identical to SRC's;
the meta keys are SRC's plus nothing. --mutate: scale the saved vector's last unknown by 1+1e-9 and the |F| check must fail (exit 1); it writes DST with "_MUT" before ".npz", never DST itself."""
import sys

import numpy as np

from hpkernel.driver import load, make_solver, save

src, dst, tol, hmax, minsteps = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
mutate = "--mutate" in sys.argv
if mutate:
    dst = dst[:-4] + "_MUT.npz"
zh, zl, m = load(src)
s = make_solver(m["D"], m["M"], nodes=m["nodes"], kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=3)
zh, zl = np.array(zh), np.array(zl)
s.set_segs(s.plan(zh, zl, tol, hmax))
segs = [[float(x) for x in g] for g in s.get_segs()]
steps = sum(len(g) - 1 for g in segs)
m2 = dict(m)
m2["segs"] = segs
zs = zh.copy()
if mutate:
    zs[-1] *= 1 + 1e-9
save(dst, zs, zl, m2)
zh2, zl2, m3 = load(dst)
s.set_segs(m3["segs"])
fh, fl = s.residual(np.array(zh2), np.array(zl2))
F = float(np.abs(np.asarray(fh) + np.asarray(fl)).max())
s0 = np.load(src)
same = np.array_equal(zh2, s0["zh"]) and np.array_equal(zl2, s0["zl"])
keys = set(m3) == set(m)
ok = steps >= minsteps and F <= 1e-26 and same and keys
print(f"plan tol_step {tol:g} hmax {hmax:g}: {steps} steps (need >= {minsteps}), max|F| {F:.3e}, vector identical {same}, meta keys kept {keys}: {'pass' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
