# formulation-mac: the nonlinear horizon toy, Newton basins of three formulations of the horizon data

Machine: the Mac, a coordinator subagent's study, 2026-11-04/05 (notes/QUAD_DOUBLE.md 13.21). The scripts are in the
code repository's `hp/horizon_toy_nl/` (toy_nl.py, run_basin.py, calib.py, diag.py, pade_nl.py, batch.sh), run from
that directory with the main venv's python and mpmath.

- `calib_32.jsonl`, `calib_32.log`: the toy's pole law against T5's table (QUAD_DOUBLE 13.6), `calib.py`.
- `basin_{series,inward_ue0.1,reseed}_{32,64}[_inexact].jsonl`, `log_*.txt`: planted truth, controls and basins per
  formulation, digits and s (`run_basin.py`, through `batch.sh`); `_inexact` runs start from an inexact first evaluation.
- `diag_64.jsonl`, `log_diag_64.txt`: G, the inward formulation's smallest singular value and the re-seeded horizon
  datum's error, `diag.py`.
- `log_pade_64_20.txt`: the Pade formulation at s 20.5, 64 digits, `pade_nl.py`.
- `lenient/`: runs whose residual stays defined beyond the slab (truncated divergent sums, backtracking).
