"""#1078: mode_det at given lambdas on one state, one jsonl row per lambda (sign, ln|det|, pivot range, with float hex).

    python3 mequil_probe.py HPDIR OUT.jsonl STATE.npz LAM [LAM ...] [--threads=6] [--hmax=0.05]

HPDIR is the hp/ directory of the worktree whose kernel (the python on the command line) is under test. The environment's
HP_MODE_EQUIL is recorded in every row. Same plan as lowD_gamma.py: s.plan(zh, zl, 1e-32, hmax)."""
import json
import os
import sys
import time

args = [a for a in sys.argv[1:] if not a.startswith("--")]
o = dict(a[2:].split("=", 1) if "=" in a else (a[2:], "1") for a in sys.argv[1:] if a.startswith("--"))
if len(args) < 4:
    print(__doc__)
    sys.exit(2)
sys.path.insert(0, os.path.abspath(args[0]))
import lowD_gamma as LG                                                    # noqa: E402
from hpkernel.driver import load                                           # noqa: E402

out, state, lams = args[1], args[2], [float(x) for x in args[3:]]
zh, zl, meta = load(state)
D, M = meta["D"], meta["M"]
s, grid = LG.build_solver(D, M, meta, int(o.get("threads", 6)))
tp = time.time()
segs = s.plan(zh, zl, 1e-32, float(o.get("hmax", 0.05)))
s.set_segs(segs)
try:
    from tau_map_gain import nsteps                                        # noqa: E402
    plan_steps = nsteps(segs)
except Exception:
    plan_steps = None
plan_sec = round(time.time() - tp, 1)
for lam in lams:
    t = time.time()
    sg, la, pmin, pmax = s.mode_det(zh, zl, lam, 0.0)
    row = dict(D=D, M=M, lam=lam, sign=float(sg), ln=float(la), ln_hex=float(la).hex(), pmin=float(pmin),
               pmin_hex=float(pmin).hex(), pmax=float(pmax), pmax_hex=float(pmax).hex(), ratio=float(pmin) / float(pmax),
               equil=os.environ.get("HP_MODE_EQUIL"), state=os.path.basename(state), map=grid,
               hpdir=os.path.abspath(args[0]), hmax=float(o.get("hmax", 0.05)), plan_steps=plan_steps, plan_sec=plan_sec,
               sec=round(time.time() - t, 1))
    with open(out, "a") as fh:
        fh.write(json.dumps(row) + "\n")
    print(f"lam {lam!r}: sign {sg:+.0f} ln|det| {la!r} pivots {pmin:.3e}..{pmax:.3e} ratio {row['ratio']:.1e} "
          f"HP_MODE_EQUIL={row['equil']} hmax {row['hmax']} plan {plan_steps} steps ({row['sec']} s)", flush=True)
