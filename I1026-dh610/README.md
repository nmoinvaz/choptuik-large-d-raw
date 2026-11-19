# I1026-dh610: do the three radius-stable M = 3 zeros of #1020 persist at M = 5?

Machine: dh610 (Fedora, i7-12700, 20 threads, 62 GB), beside #1003's K 49 run (5 procs). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1026 (after #1013 and #1020; coordinator's order of
2026-11-19 ~12:50 UTC). Code: `hier_nb.py` of the worktree `~/Source/cl-995` (wip/excited-zeros fc7dee4d), venv `~/Source/venv-i1026` (python 3.14, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, numba 0.68.1:
the main venv has no numba), 2 procs per solve, nice 10.

## Why not `hier_nb.py 5` as it stands

`hier_nb.py 5 A w --x=B3,C3 --schur --procs 2` from the known zero's M = 3 place stops at |r_1| = 121 with no step: the nested level-3 re-solves fail at the level-1 Newton's trial points (|r_3| 3e2 to 5e6),
with or without `--predict --floor`. A complete fixed-(A, w) solve (`--fixA`) from the same M = 3 harmonics converges at the stored M = 5 zero and half-way (|r_3| 1e-8, 15 s). So the route is the outer Newton
over complete fixed-(A, w) solves, as `m7_outer.py`'s newton mode (written for M = 7 for this situation): `walk1026.py` (details in its docstring). The two probes are `logs/probe_hier_start.log`, `logs/probe_hier_start_predict_floor.log`, `logs/probe_fixA_*.log`, and a debug walk of the control `logs/debug_walk_control_scratch.json`.

## Readings, fixed before the runs

- **Control.** `walk1026.py control` from the known zero's M = 3 place (2.726476, 1.015603) with its M = 3 harmonics must converge to the stored M = 5 zero (`inputs/hier_M5_full_schur.log`: A 2.718579189,
  w/w_inf 0.999228404) within 1e-5 in A and in w. If not, the run stops there (`eval1026.py` exits 1).
- **Candidates.** Each started at its M = 3 zero with its M = 3 harmonics (`logs/f3probe.log`). PERSISTS: the walk converges (Newton step below 3e-6 in A and w/w_inf, |r_3|, |r_5| below 1e-6) to a zero not
  within 5e-3 of the known zero's M = 5 zero, with the M = 3 -> 5 shift (Euclidean norm in (A, w/w_inf)) smaller than the M = 1 -> 3 shift. FAILS: no converged solve is reached from it, or it converges to the
  known zero, or the shift is larger. UNDECIDED: otherwise (iteration cap; xi1 0.2 and 0.25 disagreeing). Primary radius xi1 0.2 (the control's), xi1 0.25 alongside (all four zeros).

## Files

| file | content |
|---|---|
| `common1026.sh`, `run1026.sh` | paths and the driver (the commands are in it) |
| `walk1026.py`, `eval1026.py`, `f3probe1026.py` | the outer-Newton walk, the readings' evaluator (selftest, mutations), the M = 3 harmonics probe |
| `inputs/` | the stored M = 5 selection log |
| `walks/`, `logs/`, `exits_1026.txt`, `memlog_1026.log` | one JSON per walk, each solve's and walk's log, exits, alert-only memory log |

## Results of the pre-registered run (12:58-13:03 UTC, `logs/eval_all.log`)

- Control, xi1 0.2: PASS, 7 solves, zero (2.718579192, 0.999228404), 3.1e-9 and 3.2e-10 from the stored one.
- xi1 0.2 (primary): minus FAILS (the Jacobian step in w gave |r_3| 2.0e-6 against the bar 1e-6, after two solves at 6.6e-8 and 1.8e-7), plus FAILS (the start solve gave |r_3| 1.8e-6, |r_5| 5.4e-8), newzero FAILS (the start solve's level 3 stays at |r_3| 15).
- xi1 0.25: the control's start solve fails (|r_3| 8.3e3), so the route is not validated there; minus walks 25 iterations (30 solves, all |r_3| < 3e-9) from (2.598600, 0.221757) to (2.22758, 0.09269), |r_1| 0.053, not converged: UNDECIDED; plus (|r_3| 8.8e2) and newzero (|r_3| 5.9e2) FAIL.
- Verdicts by the rule: minus UNDECIDED, plus FAILS, newzero FAILS.
- At the M = 3 zeros the M = 5 solves give F_5/F_1 of 0.114 (minus), 0.123 (plus), 0.181 (newzero) and F_3/F_1 of 0.292, 0.298, 0.433, against 0.0031 and 0.0549 at the known zero.

## Exploratory runs (13:04-13:09 UTC, `run1026x.sh`, `walks_explore/`, `logs_explore/`; not readings)

- xi1 0.2 with the bar at 1e-5: minus no converged zero (20 solves, heading to (2.5123, 0.0876), level 3 stops converging, |r_3| 0.27); plus converged in 30 solves to (2.583888, 0.141358) (|r_3| 2.2e-6, shift norm 0.272 against 0.0887: fails by the rule); newzero unchanged (level 3 at |r_3| 15).
- xi1 0.25, minus with the cap at 80: converged in 32 solves to (2.227529, 0.092574) (|r_3| 2.8e-10, |r_1| 5e-5, shift norm 0.393 against 0.0731: fails by the rule).
- `logs_explore/radius_check_*`: fixed-(A, w) solves at the two M = 5 zeros with the walks' final harmonics at other radii (minus zero at xi1 0.2 and 0.3, plus zero at 0.25 and 0.3): |r_1| 7.6e-6 to 1.2e-4, the zeros do not move with xi1.
