"""step 0b: one Newton step from a stored converged state, quad-double against octo-double, on the segment plan at
PLAN_TOL. python step0_step.py RAW PLAN_TOL STATE [--qd_refine4 1] [--octo 1] [--out OUT.npz]
Prints the pinned residual (octo-double, the reference) at the start and after each full step: the quad-double step
(PinnedQ.newton_q; with --qd_refine4 1 also its horizon solves refined four steps, mutate 8) and the octo-double step
(PinnedO.newton_o), and the max differences between the steps. A quad-double step that raises |F| where the
octo-double one lowers it is wrong in quad-double, not in the model or the plan."""
import os, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e/hp")
import numpy as np, mpmath as mp
mp.mp.dps = 50
from hpkernel.driver import load_q
from multidouble import od_axpy
from octo_corrector import o8, o8_of_q, omax, pinned_o

raw, plan_tol, path = sys.argv[1], float(sys.argv[2]), sys.argv[3]
argv = sys.argv[4:]
opt = dict(qd_refine4=0, octo=1, out="")
for k in list(opt):
    if "--" + k in argv:
        i = argv.index("--" + k); opt[k] = type(opt[k])(argv[i + 1])
z4, meta = load_q(os.path.join(raw, path))
z4 = o8(z4)
z8 = o8_of_q(z4)
s, sp, sq, so = pinned_o(meta, z4, threads=3, plan_tol=plan_tol)
nsteps = sum(len(sg) - 1 for sg in s.get_segs())
F0 = omax(so.residual_o(z8))
print(f"{path}: D {float(mp.mpf(meta['D_str'])):.4f}, plan {plan_tol:.0e} ({nsteps} Taylor steps), pinned max|F| (octo) at the "
      f"state {F0:.2e}", flush=True)
steps = {}
for name, mu in [("qd", 0)] + ([("qd_refine4", 8)] if opt["qd_refine4"] else []):
    t0 = time.time()
    st = sq.newton_q(*z4, mutate=mu)
    d = o8_of_q(st[:4])
    steps[name] = d
    Fn = omax(so.residual_o(o8(od_axpy(1.0, *d, *z8))))
    print(f"  {name} step: |dz| {np.abs(d[0]).max():.2e}, dDelta {d[0][-1] + d[1][-1]:+.3e}, piv {st[6]:.1e}..{st[7]:.1e}; "
          f"max|F| (octo) after the full step {Fn:.2e}; {time.time() - t0:.0f} s", flush=True)
if opt["octo"]:
    t0 = time.time()
    st = so.newton_o(z8)
    d = st[0]
    steps["od"] = d
    Fn = omax(so.residual_o(o8(od_axpy(1.0, *d, *z8))))
    print(f"  od step: |dz| {np.abs(d[0]).max():.2e}, dDelta {d[0][-1] + d[1][-1]:+.3e}, piv {st[3]:.1e}..{st[4]:.1e}, newton_o's |F| "
          f"{omax(st[1:3]):.2e}; max|F| (octo) after the full step {Fn:.2e}; {time.time() - t0:.0f} s", flush=True)
    for name in [k for k in steps if k != "od"]:
        e = o8(od_axpy(-1.0, *steps["od"], *steps[name]))
        ev = np.abs(np.asarray(e[0]) + np.asarray(e[1]))
        i = int(np.argmax(ev))
        print(f"  |dz_{name} - dz_od| {ev.max():.2e} (row {i}, block {i // 128 if i >= 64 else 'centre'}), relative to |dz_od| "
              f"{ev.max() / max(np.abs(steps['od'][0]).max(), 1e-300):.2e}", flush=True)
if opt["out"]:
    np.savez(opt["out"], **{f"{k}_{q}": v[q] for k, v in steps.items() for q in range(len(v))})
