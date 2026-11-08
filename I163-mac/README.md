# I163-mac: RT prototype with horizon Taylor rows (--horizon K): planted checks, pilots, the acceptance at D 50.01 on 32x121 and 32x123, and the pair test at D 60.00 on 32x93-99

Machine: the Apple M5 Mac (`mac`), shared with #189's agent. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/163

Code: worktree `agent-aed8a75ee3273b565` of the main repository, branch `wip/i163` (each driver prints its commit). The
solver is #145's (`rt_run.py --solver mp`, 192 bits) with the new option `--horizon K` of `solver/rt/rt_model.py`:
the collocated rows of Omega_2,3,4^+ at the K points next to xi = -1 are replaced by the Taylor coefficients of orders
1..K of the same residuals at xi = -1. `--horizon 0` (the default) is the collocation of #105, #145 and #164,
bit-identical. `--mutate=norows` runs a command with the rows dropped (K = 0).

## Layout

- `run_one.sh OUTDIR TAG START GRID K [opts]`: one solve with #145's options (`--tol 1e-12 --max_products 250
  --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4`; Newton's target 1e-40 below D 54, 1e-38 at 54.996085,
  1e-36 at 60.001952), the state resampled to GRID and solved at its own D.
- `checks/`: the symbolic and planted checks of `solver/rt/rt_horizon.py` and their controls.
- `pilot/`: pilots at D = 54.996085 on 32x121, before the criteria below.
- `run_queue.sh QUEUE`: runs the lines of a queue file with `run_one.sh`; `run_py.sh LOG script.py ...` runs one
  diagnostic into a log; `run_checks.sh` the checks of `checks/`.
- `diag/`: diagnostics outside the acceptance.

## Pilots (D = 54.996085, 32x121), before the criteria

- `pilot/p7.stdout`, `pilot/p30.stdout` (21:21 UTC, code a99b2f5): K = 7 and K = 30 from #145's 32x101 continuation
  state, resampled in f64 by `resample_to`. K = 30: GMRES reached only 6.1e-3 in 250 products at the first Newton step
  (the f64 LU does not precondition rows of order 30), stopped by hand. K = 7: the resampled start has max|F| = 1.9e-11
  (the rows amplify the f64 rounding of the resampling), the first step reaches 2.4e-15, then Newton moves by 1e-7 to
  6.5e-5 per step with max|F| between 1e-9 and 8e-8 for six steps; stopped by hand.
- Diagnostics (`diag/`, 21:35 UTC, `rt_resample_res.py`, exact resampling in arb). The D = 50.007491 roots of #145 on
  32x121 (fol, -2.9e-12 from hp) and 32x101 (cont, +3.3e-15) keep max|F| = 8.2e-31 and 3.4e-31 when resampled to
  121, 141 and 181 points: both are roots of every finer xi grid to the double-double floor. The 32x121 root also
  satisfies the K = 7 rows on 32x121 and 32x123 to 5.9e-29 and 4.9e-29.
- Prediction written before the second pilot (21:41 UTC): with the start resampled exactly (`--resample_mp`), K = 7 on
  32x121 at D = 54.996085 converges from #145's 32x101 state to a root within 1e-13 of that state's Delta (-2.1e-14
  from hp), and from #145's 32x121 root (+8.5e-12) to a root within 1e-13 of +8.5e-12. That is, the rows keep both
  roots and do not decide between them.
- Second pilot (21:41 UTC, code 8167b24): from #145's 32x121 root (+8.5e-12) the K = 7 system starts at max|F| =
  7.1e-29 and converges in one Newton step (max|dz| 1.8e-20) to +8.54e-12 from hp (`pilot/p7b.*`, exit 1 against
  1e-12). From #145's 32x101 state resampled exactly it starts at 3.4e-29 (`pilot/p7r.*`).

## Criteria (written 21:45 UTC, before the main runs; not to be changed)

K = 7 throughout: lambda_2 = 5.68 at D = 50.007491 and 5.94 at 60.001952, so the rows of orders 6 and 7 lie above
Re lambda_2 for every harmonic. K = 30, which would also pass lambda_4 (26 to 31), is out of reach of the f64-LU
preconditioner (pilot). Every start is resampled exactly (`--resample_mp`). A root counts when its record has ok true.
hp is the double-double row of `hp/data/delta_all.csv` (err 2e-15).

1. **Acceptance (#163), D = 50.007491, 32x121, K = 7.** Start a: #145's 32x101 continuation state
   (`I145-mac/cont/cont_32x101_D50.0075_32x101.npz`, +3.3e-15 from hp). Start b: #145's 32x141 root
   (`I145-mac/fol/fol_32x141_D50.0075_32x141.npz`, -4.1e-11). Pass: both converge, |Delta_a - Delta_b| < 1e-18, and
   both |Delta - Delta_hp| < 1e-14 (`rt_grids.py --tol 1e-14 --tol_ab 1e-18` exits 0).
2. **The control (#163).** The same two commands with `--mutate=norows`. It fires when at least one root misses hp by
   more than 1e-12 (`rt_grids.py --tol 1e-12` exits 1). The acceptance holds when 1 passes and 2 fires.
3. **The other family (coordinator), 32x123, N = 3 mod 4.** 1 and 2 on 32x123 with the same starts and rules,
   reported by family.
4. **Pair test (coordinator), D = 60.001952, 32x93, 95, 97, 99, K = 7.** Starts a and b of #164 (#145's 32x101
   continuation state and its 32x121 root at that D). `rt_roots.py` on each pair with the rows, and on #164's pairs
   without them (`I164-mac/roots/a101_32xN_D60.0020_32xN.npz` and `b121_...`): max|z2 - z1|, max|B(e, e)|/max|e| and
   the verdict (two roots, or hidden by the floor). The rows remove a pair when its verdict changes from two roots to
   hidden by the floor.
5. **Predictions, from the diagnostics above.** (P1) Criterion 1 fails: start a lands within 1e-13 of +3.3e-15 from
   hp and start b within 1e-13 of +4.5e-12, the root #145's 32x121 re-solve found from the same start without rows,
   since the rows keep the collocation's analytic roots. (P2) In criterion 4 the rows change max|z2 - z1| by less than
   a factor 10 on every grid. The issue's premise predicts the opposite of both: one root per grid within 1e-14 of hp.

## Results (after the runs; the criteria above are unchanged)

The write-up is section 13 of notes/RT_FORMULATION.md (branch wip/i163). Verdicts, from `fit/`:

| criterion | result | verdict |
|---|---|---|
| 1, 32x121 K = 7 | a -1.86e-12, b -1.97e-12 from hp, a - b +1.12e-13 (`fit/acc_32x121.log`, exit 1) | fails |
| 2, 32x121 no rows | a -2.89e-12, b -2.90e-12 (`fit/acc_32x121_norows.log`, exit 1) | control fires |
| 3, 32x123 K = 7 | a -4.29e-12, b -4.14e-12, a - b -1.43e-13 (exit 1) | fails |
| 3, 32x123 no rows | a -5.74e-12, b -5.73e-12 (exit 1) | control fires |
| 4, pairs at D 60 | 93 removed (4.65e-14 -> 2.2e-16, hidden); 95 7.7e-15 -> 5.2e-14; 97 7.0e-14 -> 8.0e-14; 99 4.9e-15 -> 5.7e-14 (`fit/pair_*.log`) | the rows remove 1 of 4 pairs |
| P1 | start a jumped to -1.86e-12 | fails |
| P2 | factors 210 (93, the other way), 6.7, 1.1, 11.7 | fails on 93 and 99 |

The acceptance of #163 fails. Every main solve converged (final max|F| at most 6.4e-43 at D 50, 7.7e-40 at D 60).

Further folders:

- `acc/`: the D 50.007491 solves (queues A, B). `pair/`: the D 60.001952 solves (queues C, D).
- `fit/`: `rt_grids.py` and `rt_roots.py` verdicts (`run_verdicts.sh`), with the controls `fit/*mutate*`.
- `checks/`: `rt_horizon.py symbolic` (exit 0; `--mutate=a4` exit 1), `exponents`, `planted` (exit 0;
  `--mutate=taylor` exit 1).
- `diag/` (outside the criteria): `rt_resample_res.py` (roots on finer grids, control `--mutate=perturb` exit 1),
  `rt_pair_fine.py` (J along pair differences on finer grids, control `--mutate=f64` exit 1), `rt_constraint.py`,
  `rt_branch_cheb.py` (branch coefficients, `--planted` exit 0), `rt_sigma.py` (bounds on the smallest gain;
  `sigma_*.log` are the first, inverse-iteration version at code 2862224, of which only the first solve is used;
  `sigma2_*` and `sigma3_*` the bound version, planted exit 0 and its `--mutate=shift` exit 1), `again_*` (Newton from
  a stored root on its own grid: one step of 1-3e-24, no jump), `exponents_crossings.log` (lambda_2 = 4 at D 21.5, 5
  between 33 and 34).
