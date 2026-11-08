# I164-mac: RT prototype re-solves on 32x85 to 32x97 at D = 54.996085 and 60.001952, two starts each, against hp

Machine: Apple M5 Mac, a subagent of the coordinator.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/164
Code: main b4d401f of nmoinvaz/choptuik-large-d (solver/rt/, #145's code, unchanged), worktree agent-a3f8a38336503b3e7;
the reading is section 11 of notes/RT_FORMULATION.md on branch wip/i164. python-flint 0.9.0.

Starts (raw commits 62b275a for D 60.0020, e613720 for D 54.9961):

- a: `I145-mac/cont/cont_32x101_<D>_32x101.npz`, the 32x101 continuation's state (Delta - Delta_hp = -1.27e-12 at
  D 60.001952, -2.1e-14 at 54.996085).
- b: `I145-mac/fol/fol_32x121_<D>_32x121.npz`, the 32x121 root re-solved from a (+3.5e-11 at D 60.001952, +8.5e-12 at
  54.996085).

Each is resampled to 32xN by `rt_run.py --start` (Chebyshev and Fourier interpolation of the double-double parts) and
solved there at the same D. The resampled starts have an f64 residual of 5e-14 to 1.2e-13 on 85, 91 and 95.

## Criteria, written before the main runs (not changed afterwards)

- Solver and options, as #145 at D 55-60: `rt_run.py --solver mp` (192 bits, N_t = 32) with `--tol 1e-12
  --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4`, and `--newton_tol 1e-38` at
  D = 54.996085, `--newton_tol 1e-36` at D = 60.001952.
- Convergence: a root counts when its record has ok true, that is Newton reached max|F| below newton_tol, or stalled
  within 1e6 of it (below 1e-32 at 54.996085, 1e-30 at 60.001952) under --patient. An unconverged solve may be
  restarted once from its saved last state with the same options (recorded here); if that does not converge either,
  the root counts as failing.
- Hp: the double-double rows of hp/data/delta_all.csv at D = 54.996085 (up10) and 60.001952 (up13), Delta_q0 +
  Delta_q1, err 2e-15 (check). Differences are taken in arb from the records' 30-digit Delta_str.
- Pass for a grid N at D 60 (the question of #164): `rt_grids.py roots/a101_32xN.jsonl roots/b121_32xN.jsonl
  --D 60.001952 --tol 1e-12` exits 0. That needs both roots converged, |Delta_RT - Delta_hp| < 1e-12 for both, and
  their spread |Delta_a - Delta_b| < 1e-12. The verdict of #164 is yes when at least one grid passes, no otherwise.
- The same check at D 54.996085 is reported beside it (outside the verdict).
- Main runs: N = 85, 91, 95 at both D from both starts, D 60.001952 first (12 solves, `run_main.sh`, two workers, one
  per start).
- Added grids, decided from the main runs' D 60 results only. Let E(N) be the larger of the two roots'
  |Delta_RT - Delta_hp| at D 60.001952, with E(101) = 2.33e-12 from #145. If min E over 85, 91, 95 is below 1e-11, or
  E is not monotone in N over 85, 91, 95, 101, then 87, 89, 93 and 97 are run at both D from both starts. If the
  smallest E is at 85, then 81 is run at D 60.001952 from both starts too.
- Time resolution: the grid with the smallest E is re-solved on 48xN at D 60.001952 from start a. If its Delta moves
  by 1e-13 or more against 32xN from the same start, N_t = 32 is reported as a limit.
- Controls, each must fire:
  - `rt_run.py --mutate=coef` at D 60.001952 on 32x91 from its unmutated root of start a: Delta moves by more than
    1e-6 and the run exits 1.
  - `rt_grids.py --mutate=shift` on the best grid's two roots at D 60.001952 (2 tol added to one Delta): exits 1.
  - `rt_roots.py --mutate=same` on one pair of roots: exits 1 (its planted check exits 0).
- Reported per grid and D: Delta_RT - Delta_hp for each root (the difference to hp's row), and the spread of the two
  roots (|Delta_a - Delta_b|, a lower bound on how far the grid leaves Delta undetermined, not an error bar).

## What ran

- `run_main.sh a|b "32x85 32x91 32x95"`, `main_a.stdout`, `main_b.stdout`, `roots/a101_32xN*`, `roots/b121_32xN*`:
  the main runs, 13:31-13:52 UTC. Every solve converged (4 to 7 Newton steps).
- The D 60 results gave min E = 6.4e-13 (32x95) and E(95) < E(101), so by the rule above `run_queue.sh a|b`
  (`queue_*.stdout`) runs 93, 97, 89 and 87 at both D from both starts, then 48x95 at D 60 from start a and the
  coefficient mutation on 32x91 (`controls/coef_32x91_mutcoef*`). The smallest E is not at 85, so 81 is not run.
- `run_extra.sh a|b` (`extra_*.stdout`), added after the D 60 results of 93 and 97 and outside the verdict: 32x99 at
  D 60 from both starts, and 32x95 at D 60 from two more starts, the start-b roots of 32x97 (`roots/c97_32x95*`) and
  32x93 (`roots/d93_32x95*`) resampled. Why: 95 is the only grid within 1e-12 at D 60, its neighbours lie on the other
  side of hp (93 at +2.4e-12 and +2.8e-12, 97 at +8e-14 and +1.1e-12), and 99 is the one odd N between 97 and 101 not
  run. The verdict stays the criterion's.
- `run_extra_a.sh` (`extra_a.stdout`): worker a's part of `run_extra.sh` (32x99 from start a, 32x95 from the 97
  root), started when worker a's queue ended, since its 48x95 solve took 26 min (12 Newton steps). `run_extra.sh a`
  was stopped while it was still waiting, before it ran anything.
- `run_checks.sh` (`checks.stdout`, `fit/`): rt_grids.py per grid (`verdict_32xN.log` at D 60, `table_32xN.log` at
  both D), rt_roots.py per pair of roots with its new pair test (`roots_32xN_<D>.log`, code at wip/i164 487de4a), the
  controls `--mutate=shift`, `--mutate=same` and `--mutate=mid`, and the time-resolution check `nt_check.py`. Two
  parts were redone. The first nt_check.py took 32x95's last record, at D 55, and failed (difference 1.45e-2, the
  "exit 1 nt" lines of `checks.stdout`); it now takes the record at the same D, and `fit/nt_48x95*.log` are its reruns.
  The c97 part reached the 97-start solve before it had finished; `run_checks_c97.sh` (`checks_c97.stdout`) redid it.

## Results (the reading is section 11 of notes/RT_FORMULATION.md on wip/i164)

- Verdict of #164: yes. 32x95 at D 60.001952: -6.38e-13 (start a), -5.85e-13 (start b), spread 5.3e-14,
  `fit/verdict_32x95.log` exit 0. No other grid of 85-97 passes. Outside the criteria: 32x99 at -3.45e-13 and
  -2.70e-13 (exit 0), and 32x95 from the 97 and 93 roots at -6.37e-13 and -6.39e-13.
- Delta_RT - Delta_hp at D 60.001952 (start a, start b): 85 -3.42e-11, -3.42e-11; 87 -5.24e-11, -5.24e-11; 89
  +2.58e-11, +2.51e-11; 91 -8.37e-12, -8.37e-12; 93 +2.35e-12, +2.81e-12; 95 -6.38e-13, -5.85e-13; 97 +8.4e-14,
  +1.08e-12. At D 54.996085 (both starts agree to 2e-14): 85 +1.89e-10, 87 -8.65e-11, 89 +2.88e-11, 91 -8.32e-12,
  93 +2.20e-12, 95 -5.46e-13, 97 +1.25e-13.
- The first prediction held on all five of its named results. The second held in sign and spread for 32x99, not in
  size (-2.7e-13 to -3.5e-13 against about -5e-14 to -1e-13).
- Pair test at D 60.001952: two distinct roots on 89, 93, 95, 97 and 99 (max|F(zm)| 1.8e-28 to 8.6e-25 against about
  2e-31 at the roots); hidden by the floor on 85, 87, 91, and on every grid at D 54.996085.
- Controls: coef on 32x91 at D 60 moved Delta by 1.31e-2, exit 1 (20 Newton steps, not converged); `--mutate=shift`
  exit 1; `--mutate=same` exit 1; `--mutate=mid` exit 1; 48x95 - 32x95 = +1.5e-16 (exit 0), with --tol 1e-17 exit 1.

## A prediction, written at 2026-11-08 14:02 UTC before the results it names (outside the criteria)

At D 60.001952 the sign of Delta_N - Delta_hp is (-1)^((N-1)/2) on 89, 91, 93, 95 and 97 (+, -, +, -, +), and at
54.996085 on 85, 91 and 95 (+, -, -). That is the sign of -T_{N+1}(0), the leading neglected Chebyshev term at
xi = 0, where the equations are divided by xi; it flips with each step of 2 in N. If the pattern is that, then before
their results: 87 at D 60 is negative, and at D 54.996085 87 is negative, 89 positive, 93 positive and 97 positive.
85 at D 60 (negative) already breaks it, and 99 and 101 at D 60 are expected to be set by the spread of their roots
(1e-12 at 97 and 101), not by this sign.

## A second prediction, written at 2026-11-08 14:06 UTC, before 32x99's results (outside the criteria)

The D 60.001952 roots of 85 to 97 fall into two families by N mod 4. For N = 3 mod 4 (87, 91, 95), the half grid
xi > 0 has an even number of points (N + 1)/2. Their errors are -5.24e-11, -8.37e-12 and -6.1e-13, falling about a
decade per step of 4 in N, and the two roots agree to 2.2e-15, 2.3e-15 and 5.4e-14. For N = 1 mod 4 (89, 93, 97, 101)
the errors are +2.5e-11, +2.6e-12, +8e-14 to +1.1e-12 and -1.3e-12 to -2.3e-12, and the roots spread by 7.1e-13,
4.6e-13, 1.0e-12 and 1.1e-12 (85 is the exception there, 1.0e-15). If that holds, 32x99 (3 mod 4) at D 60 is
negative and smaller than 95's 6e-13, about -5e-14 to -1e-13, with its two roots within 1e-13 of each other, so it
would hold 1e-12 too.
