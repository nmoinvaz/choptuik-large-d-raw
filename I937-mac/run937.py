"""#937 launcher: runs hp/anm_run.py's main() unchanged, with two logging wrappers that change no result.

  reseed.Reseeder.project   after each call, one line: the outcome (u0q, u0, ladder, failed) and each stage of
                            last_project (pred_q under --project_start pred, u0, u0q, ladder) with its iterations and
                            |R| before and after, and the seconds. why_failed does not print the pred_q stage.
  octo_corrector.with_horizon
                            after each call with rs.od > 0, one line: rs.last_o, the rung max|R| of each refine_o
                            correction (the coordinator's question: does refine_o run inside the corrector's
                            projections, or only at the start's re-seed?).

The wrappers are set before anm_run is imported, so its own name with_horizon is the wrapper too (the start's
re-seed, which anm_run also logs). ElimO.project calls with_horizon by its module name.
Run: python3 run937.py ANM_RUN_ARGS... (from hp/ of the worktree; sys.argv as anm_run.py's)
"""
import os
import sys
import time

sys.path.insert(0, os.getcwd())
import octo_corrector  # noqa: E402
import reseed  # noqa: E402

_project = reseed.Reseeder.project
_with_horizon = octo_corrector.with_horizon


def project(self, z):
    t0 = time.time()
    out, how = _project(self, z)
    lp = getattr(self, "last_project", {}) or {}
    parts = []
    for k in ("pred_q", "u0", "u0q"):
        if k in lp:
            d = lp[k]
            parts.append(f"{k} {'conv' if d.get('conv') else 'NOT conv'} {d.get('its')} its |R| {d.get('R0', float('nan')):.2e}"
                         f" -> {d.get('R', float('nan')):.2e}")
    if "ladder" in lp:
        parts.append(f"ladder {'ok' if lp['ladder'].get('ok') else 'FAILED'} {lp['ladder'].get('rungs')} rungs")
    print(f"      [937] project: {how}; " + "; ".join(parts) + f"; {time.time() - t0:.1f} s", flush=True)
    return out, how


def with_horizon(z8, z4, rs):
    out = _with_horizon(z8, z4, rs)
    if getattr(rs, "od", 0):
        lo = getattr(rs, "last_o", None)
        print("      [937] with_horizon: refine_o rung max|R| "
              + (" -> ".join(f"{r:.2e}" for r in lo) if lo is not None else "none"), flush=True)
    return out


reseed.Reseeder.project = project
octo_corrector.with_horizon = with_horizon
sys.argv = ["anm_run.py"] + sys.argv[1:]
import anm_run  # noqa: E402

anm_run.main()
