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
- 2026-11-19 02:02 UTC, criterion 3 as written does not hold, and it was a wrong criterion: the stored `solver/proof/trunc_hier_M3.log` and `trunc_hier_M5.log` are K 9 and
  K 13 at J = 500, these runs are K 18 at J = 1000. M = 3, new against stored (`cmp996.py M3.log .../trunc_hier_M3.log`): σ_1 differs by 2.7e-10 relative, σ_2 6.6e-10,
  σ_3 1.5e-9 (orders that are exact in this model), σ_4 1.3e-4 (the first truncated order, 3.4e-6 absolute against Δσ_4 = σ_4^[5] − σ_4^[3] of 4.1e-5 from the J = 1000 runs,
  8%). So the fit's J matters at 1e-10 to 1e-9 for the exact orders and at 8% of the shift for σ_{M+1}; reported, not fixed.
- 2026-11-19 02:23 UTC, third launch (`run996c.sh`, coordinator's hc). The precision control failed (M 7 at 60 digits is wrong: σ_1, σ_2 off by 1.6e-6 and 6.6e-6 against 120 digits while its fit
  residual reads 1e-61; M 3, M 5, M 7 (120) and M 9 (120) agree to about 1e-12 at σ_1 and σ_2). The 60-digit M 7 job (pid 487040) was stopped at 02:22:40 UTC (exit 143, 3267 s, its log
  `M7.log` kept to k 11, not usable). The 60-digit M 5 job keeps running as the comparison. Three new jobs from a third worktree `~/Source/choptuik-large-d-996c` at origin/main
  2d393061 (the code of e4d70167, a docstring added): `M5_dps120` and `M3_dps120` (`amp_trunc_hiermodel.py M 18 1000 1.0 120`) and `M9_K9_dps180` (`amp_trunc_hiermodel.py 9 9 1000 1.0 180`,
  M 9's own precision control against the 120-digit M 9). Rule for every M (coordinator): accept σ_k only where a run at higher digits agrees to 1% of Δσ_{M+1} or better, the agreement
  reported per k (`agree996.py`, selftest `selftest_agree996.log`, and its mutated run `selftest_agree996_mutated.log`, exit 1). Δσ_{M+1} = σ_{M+1}^[M+2] − σ_{M+1}^[M] from the
  highest-digit runs; it does not exist for M 9 (needs M 11). The Mac runs M 3 and M 5 at J 1500 and 120 digits for the J question.
- 2026-11-19 06:37 UTC, state after the account switch (the old session's shell tasks never reported; the jobs were checked from logs and exits). All eight jobs ended by themselves:
  `M3` 1942 s, `M3_dps120` 2137 s, `M5` 4331 s, `M5_dps120` 4144 s, `M7_dps120` 6316 s, `M9_dps120` 10314 s, `M9_K9_dps180` 3422 s, all exit 0 (`exits_996.txt`), and the stopped
  `M7` (60 digits, exit 143 after k 11, invalid) and the failed `M9` (60 digits, exit 1 at k 1). Their JSONs are here. Tables: `agree996_table.txt` (per k, higher against lower digits,
  fit residuals, in units of Δσ_{M+1}) and `exact996_table.txt` (the exact orders σ_0..σ_M agree across models M, so a run of M' > M is a second check of M's exact orders at no
  extra digits; in units of Δσ_{M+1}).
  Findings in them: M 3 and M 5 at 120 digits equal their 60-digit runs (20 JSON digits for M 3; at most 7.3e-7 of Δσ_6 at σ_7 for M 5): accepted at every k. M 7 has no higher-digit
  run; against M 9 at 180 digits its σ_0..σ_4 agree to 1.2e-4 of Δσ_8 or better (accepted), but its σ_6 and σ_7 differ from M 9's at 120 digits by 1.6e-3 and **1.7e-2** of Δσ_8
  (1.2e-11 and 1.2e-10 absolute, Δσ_8 = 7.34e-9), over the 1% rule at σ_7, and which of the two is the less accurate there cannot be told without a higher-digit run of M 7
  or of M 9 beyond k 9. M 9 at K 18 does not reach its own σ_{M+1} = σ_10 (k 21), so it has no residual there and no Δσ_10.
- 2026-11-19 08:12 UTC, fourth launch (`run996d.sh`, coordinator's go): `M7_K15_dps180` ended exit 0 after 5487 s: **M 7 at 180 digits equals M 7 at 120 digits in every stored digit at σ_0 to σ_7** (difference 0.0 in the 20-digit JSONs, fit residuals equal in 2 digits), so
  the 120-digit M 7 is precise at the exact orders and the 1.7% mismatch with M 9 at σ_7 is not M 7's digits. σ_8 (= σ_{M+1} of M 7, k 17) is beyond this run's K 15 and is checked only by the 60-digit run's absence: unchecked at higher digits. `M9_K15_dps180` is still running (k 7 of 15 at 07:38).
