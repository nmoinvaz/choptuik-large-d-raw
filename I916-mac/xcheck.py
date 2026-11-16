#!/usr/bin/env python3
"""#916 part 1: the x direction of the kernel's solution at eta = 0.3, D 10.5, M = 32.

    PYTHONPATH=<site> python3 xcheck.py <sigma_ms directory> <21-node state.npz> <27-node state.npz> <out.json>

Each variant builds the kernel's system, plans its Taylor steps from the state, and takes Newton steps (Solver.newton,
exact double-double Jacobian) until max |F| <= 1e-30, at least one and at most three. Variants:
  base      the 21 nodes, plan tolerance 1e-32 (the system of #913 and #915), as the reference of this script
  nodes27   27 nodes (six added inside), from the state carried there by renode.py
  plan1e-28 the 21 nodes, plan tolerance 1e-28
  plan1e-24 the 21 nodes, plan tolerance 1e-24 (an extra)
  plan1e-28_fixed, plan1e-24_fixed
            the same with the Taylor steps planned once, from the starting state, and kept: the residual of a
            re-planned system stays at the plan's own error, about 3e-29 and 3e-25, and cannot reach 1e-30
With a fifth argument "fixed", only the two fixed variants are run and added to the json.
Prints and saves, for each, the Taylor steps, max |F| before and after each step, and Delta minus the reference
1.14298098647245020553724 (the mean of #913's three M = 32 states) and minus this script's own base."""
import json
import sys

import mpmath as mp
import numpy as np

sys.path.insert(0, sys.argv[1])
import smdriver as sd  # noqa: E402
from multidouble import dd_add  # noqa: E402

mp.mp.dps = 50
REF = mp.mpf("1.142980986472450205537238888")


def solve(state, plan_tol, replan=True):
    z, m = sd.load(state)
    zh, zl = np.asarray(z[0], float), np.asarray(z[1], float)
    s = sd.make_solver(float(m["eta"]), int(m["M"]), nodes=m["nodes"], kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=2,
                       D=float(m["D"]))
    s.set_segs(s.plan(zh, zl, plan_tol, sd.PLAN_HMAX))
    steps = sum(len(g) - 1 for g in s.get_segs())
    hist = [dict(F=sd.fnorm(s.residual([zh, zl])), Delta=mp.nstr(mp.mpf(zh[-1]) + mp.mpf(zl[-1]), 34))]
    for it in range(3):
        dz, F, pmin, pmax = s.newton([zh, zl])
        zh, zl = dd_add(zh, zl, dz[0], dz[1])
        if replan:
            s.set_segs(s.plan(zh, zl, plan_tol, sd.PLAN_HMAX))
        hist.append(dict(F=sd.fnorm(s.residual([zh, zl])), dz=float(np.linalg.norm(dz[0] + dz[1])),
                         dDelta=float(dz[0][-1] + dz[1][-1]), Delta=mp.nstr(mp.mpf(zh[-1]) + mp.mpf(zl[-1]), 34)))
        if hist[-1]["F"] <= 1e-30:
            break
    return dict(nodes=len(m["nodes"]), unknowns=len(zh), plan_tol=plan_tol, replan=replan, taylor_steps=steps,
                history=hist, Delta=hist[-1]["Delta"], F=hist[-1]["F"])


def main():
    s21, s27, out = sys.argv[2], sys.argv[3], sys.argv[4]
    res = {}
    todo = (("base", s21, 1e-32, True), ("nodes27", s27, 1e-32, True), ("plan1e-28", s21, 1e-28, True),
            ("plan1e-24", s21, 1e-24, True))
    if len(sys.argv) > 5 and sys.argv[5] == "fixed":
        res = json.load(open(out))
        todo = (("plan1e-28_fixed", s21, 1e-28, False), ("plan1e-24_fixed", s21, 1e-24, False))
    for name, state, tol, replan in todo:
        r = solve(state, tol, replan)
        res[name] = r
        d = mp.mpf(r["Delta"])
        r["minus_ref"] = mp.nstr(d - REF, 5)
        r["minus_base"] = mp.nstr(d - mp.mpf(res["base"]["Delta"]), 5)
        print(f"{name}: {r['nodes']} nodes, plan tolerance {tol:g}, {r['taylor_steps']} Taylor steps; max |F| "
              + " -> ".join(f"{h['F']:.2e}" for h in r["history"]) + f"; Delta {r['Delta']}; minus the reference "
              f"{r['minus_ref']}, minus base {r['minus_base']}", flush=True)
        with open(out, "w") as fh:
            json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
