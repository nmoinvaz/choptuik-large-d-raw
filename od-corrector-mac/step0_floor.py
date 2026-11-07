"""step 0c: rungdiag/qd_floor.py with the segment plan's tolerance as an argument. python step0_floor.py RAW PLAN_TOL
STATE...: plain newton_qd (tol 1e-45, it_max 5) on the pinned system from each stored converged state, the residual
it reaches, measured by newton_qd (PinnedQ: the kernel's F rounded to double-double, minus c) and at the last iterate
by the octo-double pinned residual (PinnedO.residual_o)."""
import os, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e/hp")
import numpy as np, mpmath as mp
mp.mp.dps = 50
from hpkernel.driver import load_q, newton_qd
from octo_corrector import o8, o8_of_q, omax, pinned_o

raw, plan_tol = sys.argv[1], float(sys.argv[2])
for p in sys.argv[3:]:
    z4, meta = load_q(os.path.join(raw, p))
    z4 = o8(z4)
    t0 = time.time()
    s, _, sq, so = pinned_o(meta, z4, threads=3, plan_tol=plan_tol)
    z, hist, conv = newton_qd(sq, z4, tol=1e-45, it_max=5, verbose=False)
    Fs = [h["F"] for h in hist] + [h["F_new"] for h in hist if "F_new" in h]
    Fo = omax(so.residual_o(o8_of_q(o8(z))))
    print(f"{float(mp.mpf(meta['D_str'])):.4f} plan {plan_tol:.0e}: start {hist[0]['F']:.2e} min {min(Fs):.2e} last "
          f"{hist[-1].get('F_new', hist[-1]['F']):.2e} (octo {Fo:.2e}) steps {len(hist)} lams {[h.get('lam') for h in hist]} "
          f"dDelta {float(z[0][-1] - z4[0][-1]) + float(z[1][-1] - z4[1][-1]):+.1e} {time.time() - t0:.0f} s", flush=True)
