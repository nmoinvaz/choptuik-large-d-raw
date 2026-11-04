"""Per-step cost of the quad-double chain with --fix1 (anm-mac/run_trend_pin3_qd7..qd9/anm_run.jsonl): coefficient time
(jets, LU, fix1) per base, corrector time of accepted and of failed attempts, D advanced, and the predicted |F| (2-norm,
double-double) of converged and failed attempts.   python step_cost.py RAWDIR"""
import glob, json, os, sys
import numpy as np
raw = sys.argv[1]
for run in ("run_trend_pin3_qd7", "run_trend_pin3_qd8", "run_trend_pin3_qd9"):
    p = os.path.join(raw, "anm-mac", run, "anm_run.jsonl")
    if not os.path.exists(p):
        continue
    R = [json.loads(l) for l in open(p)]
    tc = sum(r["t_coef"] for r in R)
    ok = [a for r in R for a in r.get("attempts", []) if a["accepted"]]
    bad = [a for r in R for a in r.get("attempts", []) if not a["accepted"]]
    dD = sum(a["a"] for a in ok)
    t_ok, t_bad = sum(a["t_corr"] for a in ok), sum(a["t_corr"] for a in bad)
    print(f"{run}: {len(R)} bases, D {R[0]['D0']:.3f} -> {R[-1]['D0'] + (ok[-1]['a'] if R[-1].get('converged') else 0):.3f}; {len(ok)} accepted "
          f"(median a {np.median([a['a'] for a in ok]):.3f}), {len(bad)} failed; hours: jets {tc / 3600:.2f}, corrector accepted {t_ok / 3600:.2f}, failed {t_bad / 3600:.2f}; "
          f"per accepted step {(tc + t_ok + t_bad) / 60 / max(len(ok), 1):.1f} min (accepted only {(t_ok + tc) / 60 / max(len(ok), 1):.1f}); "
          f"hours per unit D {(tc + t_ok + t_bad) / 3600 / max(dD, 1e-9):.2f}")
    if ok:
        print(f"   predicted |F| of accepted: max {max(a['F_pred'] for a in ok):.2e}; of failed: min {min([a['F_pred'] for a in bad] or [float('nan')]):.2e}; "
              f"median t_corr accepted {np.median([a['t_corr'] for a in ok]):.0f} s, failed {np.median([a['t_corr'] for a in bad] or [float('nan')]):.0f} s")
