# I996-dh170: the amplitude expansion of hier's truncated models M = 3, 5, 7 and 9 to K = 18 (discovery candidate 5)

Machine dh170 (Fedora 45, i7-7700, 4 cores / 8 threads). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/996 (coordinator's hc,
2026-11-19 about 01:25 UTC; notes/DIRECTION_REVIEW.md section 2.5). #949's intake runs beside it (two near_null lanes, nice 10).

## Run

- Worktree `~/Source/choptuik-large-d-996` at origin/main 005b99f3, Python of `~/Source/choptuik-large-d-935/.venv` (3.14.10, mpmath 1.3.0, python-flint 0.9.0); the
  script is Python only. From `solver/proof/`: `python3 -u amp_trunc_hiermodel.py M 18 1000 1.0` for M = 3, 5, 7, 9, four single-process jobs in parallel at
  nice 10, each under `timeout -s TERM 86400` (24 h), `run996.sh`.
- Each job's stdout is `M<M>.log`: one line per odd k, `k 17: sigma_8 = ... fit resid ... [seconds since the job's start]`, so the σ_k reached by a job that
  is cut at 24 h is in its log; the script writes `trunc_hier_M<M>_K18_J1000_w1.0000.json` (σ_k to 20 digits, the tuned f) only when it finishes. `exits_996.txt`
  has each job's start and exit with the wall seconds; the last line of a log is `time` and the maximum resident set.
- The analysis (whether the shifts Δσ_k^[M] reproduce p_3 − 1, p_5 − 1, p_7 − 1 and predict p_9) is the issue's second step and not part of this task.

## Pass criteria for the run, written before it started

| # | check | pass |
|---|---|---|
| 1 | each job exits | 0 within 24 h (exit 124 from `timeout` is a cap, reported with the last σ_k reached) |
| 2 | each log's fit residuals | stay below 1e-30 at every k (the stored M = 3 and M = 5 logs: 1e-44 to 1e-52) |
| 3 | the M = 3 and M = 5 logs against the stored ones (`solver/proof/trunc_hier_M3.log`, `trunc_hier_M5.log`, K 9 and 13) | the σ_k printed agree to the digits both print, at the k both reach |
| 4 | the JSON of a finished job | has σ_0 .. σ_8 (9 entries) and loads |

## Amendments (dated, the criteria above are left as written)

- 2026-11-19 02:02 UTC, second launch (`run996b.sh`). The M = 9 job of the first launch stopped at k = 1, 42 s, exit 1 (`M9.log`): `ValueError: matrix is numerically
  singular` from `mp.qr_solve` in `S_at`. The coordinator's diagnosis (hc and #996's latest comment): precision, the fit basis has 93 columns at M = 9 and is singular at
  60 mpmath digits (M 7 at 60 ok, M 9 at 60 refuses, M 9 at 120 ok), fixed in main e4d70167 by a 5th argument `dps`. Two more jobs from a second worktree
  `~/Source/choptuik-large-d-996b` at e4d70167 (the first worktree is not touched while its jobs run): `M9_dps120` and, as the precision control, `M7_dps120`
  (`amp_trunc_hiermodel.py M 18 1000 1.0 120`, nice 10, 24 h cap, JSON names with `_dps120`). Pass for the control, from the coordinator: M7 at 120 digits has the
  same σ_k as M7 at 60 digits to the fit residual at each k; if not, say so before anything else. The log prints 15 digits and the JSON 20, so the comparison can be
  made to that many digits only (`cmp996.py`, `--json`), which is far above the residual (1e-59); this is said in the report.
- 2026-11-19 02:05 UTC, criterion 3 as written does not hold, and it was a wrong criterion: the stored `solver/proof/trunc_hier_M3.log` and `trunc_hier_M5.log` are K 9 and
  K 13 at J = 500, these runs are K 18 at J = 1000. M = 3, new against stored (`cmp996.py M3.log .../trunc_hier_M3.log`): σ_1 differs by 2.7e-10 relative, σ_2 6.6e-10,
  σ_3 1.5e-9 (orders that are exact in this model), σ_4 1.3e-4 (the first truncated order, 3.4e-6 absolute against Δσ_4 = σ_4^[5] − σ_4^[3] of 4.1e-5 from the J = 1000 runs,
  8%). So the fit's J matters at 1e-10 to 1e-9 for the exact orders and at 8% of the shift for σ_{M+1}; reported, not fixed.
