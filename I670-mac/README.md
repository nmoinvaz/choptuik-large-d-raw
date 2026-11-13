# I670-mac: chord-twin size of the arc plant against the number of S₁ coefficients (n = 23-31), with controls

Machine: mac (the coordinator's Apple M5 Mac), one process under `nice -n 10`, single-threaded.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/670

Code: `solver/inner_amp/pade_twin_count.py` on the branch `wip/i670-subagent` of nmoinvaz/choptuik-large-d. Method and
frozen criteria: `notes/PADE_FAR_END.md` section 7.

- `selftest.log`, `selftest_mutate_*.log`: the selftest and its four mutations (each must exit 1).
- `run.log`, `rows.jsonl`, `twin_count.json`: the run stage. One row per (F, n, node, plant) with chi, l2, the largest
  |c_m| and |density| of the least-squares twin for every M from 6 to n, M_min, M_lo and the precision rows.
  `twin_count.json` also holds the error model per node, the visibility d_m of each Chebyshev term, the controls and
  the verdicts.
- `run_mutate_moment.*`: the run with one twin moment (T_0, order 26) times 1 + 1e-8; the control C0 must fail at
  n = 27 and 31 (it does, chi 540-1000, exit 1).
- `*.stdout`: the console copies of the two run logs.

Code at e6845dfb (wip/i670-subagent). Run 2026-11-13 09:20-09:33 UTC; every exit is the last line of its log.

The errors of orders 23-30 are an extrapolation (log-linear fit of the measured relative errors on k = 18-22), an
estimate, not a measurement.
