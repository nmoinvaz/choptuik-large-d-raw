"""step 0d: plain octo-double Newton (octo_corrector.newton_od on PinnedO, no projection) from stored converged states,
tol 1e-45, it_max 5, on the plan at PLAN_TOL: the octo-double counterpart of step0_floor.py.
python step0_od.py RAW PLAN_TOL STATE..."""
import os, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e/hp")
import numpy as np, mpmath as mp
mp.mp.dps = 50
from hpkernel.driver import load_q
from octo_corrector import newton_od, o8, o8_of_q, omax, pinned_o, _delta

raw, plan_tol = sys.argv[1], float(sys.argv[2])
for p in sys.argv[3:]:
    z4, meta = load_q(os.path.join(raw, p))
    z4 = o8(z4)
    t0 = time.time()
    s, _, sq, so = pinned_o(meta, z4, threads=3, plan_tol=plan_tol)
    z, hist, conv = newton_od(so, o8_of_q(z4), tol=1e-45, it_max=5, verbose=True)
    Fs = [h["F"] for h in hist] + [h["F_new"] for h in hist if "F_new" in h]
    print(f"{float(mp.mpf(meta['D_str'])):.4f} plan {plan_tol:.0e} od: start {hist[0]['F']:.2e} min {min(Fs):.2e} last "
          f"{hist[-1].get('F_new', hist[-1]['F']):.2e} steps {len(hist)} {'converged' if conv else 'not converged'} lams "
          f"{[h.get('lam') for h in hist]} dDelta {mp.nstr(_delta(z) - _delta(z4), 5)} Delta {mp.nstr(_delta(z), 30)} "
          f"{time.time() - t0:.0f} s", flush=True)
