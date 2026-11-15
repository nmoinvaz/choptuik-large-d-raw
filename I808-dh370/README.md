# I808-dh370: Delta at fixed D under the d6 and d10 held values and under a new plan, at #603's states

Machine dh370 (Fedora 45, i7-8700, 12 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/808.

Scripts (written by the coordinator): `run808.sh` (the jobs), `table808.py` (the table, the control and the verdicts,
with the rule fixed before the runs in its docstring). Code: worktree `choptuik-large-d-808` at main 0209d4d2
(`anm_run.py --held_from`), venv-i800 (main's kernel at ccc520e1 plus ks_w_from, off by default).

Each job polishes one of #603's states at its own D (`--steps 0`, #603's flags, `--qd_it 20`, `--save_base 1`):
- d6, d10: the held values of #608's chain of that fit (its last state, I608-dh610/chain_d6 at 243.1312 and chain_d10
  at 242.1312), carried to D by the fit, on #603's plan;
- plan: #603's own held values on a new plan (`--keep_plan 0`).

States: D 240.1244 (the control, against data/delta_fits.csv) and 250.8381, 251.8859, 252.6135, 253.5301, where
#603's departure from track C's series is near its envelope 2.2e-37/p_min. Pilot first: 253.5301 d10 (the hardest) and
240.1244 d6, 6 threads each; then the other 13 jobs, 3 at a time at 4 threads.

Why the design changed from the issue's text: anm_run holds the held values relative to the base, so `--held_fit` of
another degree alone changes nothing at fixed D. `--held_from` gives the other chain's values instead. #608's chains
use other plans (21 segments against #603's 61), so delta_fits.csv's differences carry a plan change too, and the plan
arm measures that part alone.

## Results (dh370, 2026-11-15)

What ran. Unit `i808` (`run808.sh pilot`, 12 threads at nice 10), 02:01:28 to 02:59:04 UTC: both pilot jobs refused every
trial of step 0 (6 trials each in 57 min, lam 1 to 1/32) and were stopped on the coordinator's order, their logs kept as
`s240.1244_d6_pilot.log` and `s253.5301_d10_pilot.log` (`i808_journal.log`):

| pilot job | held shift | first step \|dz\| | trial max\|F\|, lam 1 to 1/32 |
|---|---|---|---|
| s240.1244_d6 (the control) | at most 6.67e-7 | 8.72e-7 | 6.2e39, 7.0e37, 9.8e35, 1.5e34, 2.3e32, 3.6e30 |
| s253.5301_d10 | at most 7.56e-6 | 9.08e-6 | 6.1e50, 2.4e48, 1.0e46, 6.0e43, 5.4e41, 6.9e39 |

By the coordinator's analysis (not re-derived here) a held shift of 1e-6 moves a_h and the horizon series multiplies it by
the mass mode's gain (about 1e37 at D 240), so every first full step of the held arm lands at 1e39 to 1e50 and the arm
cannot work at fixed D. So the control (delta(d6) = +3.4486e-11 against `data/delta_fits.csv`) was not measured and
the held arm has no job. Then unit `i808plan` (the plan arm only: `run808.sh job` at the five states, 4 threads each,
three at a time, then `table808.py` into `table808_plan.txt`), 02:59:20 to 06:24:25 UTC. Exits (`exits_808.txt`): all five
jobs exit 0, none converged, and the table exits 2 (the held arm missing, as expected).

| job | start to end (UTC) | steps | final max\|F\| | first correction's dDelta | step 0's trials |
|---|---|---|---|---|---|
| s240.1244_plan | 02:59 to 05:39 | 16 | 3.4e-25, no trial accepted at step 15 | +2.610e-16 | lam 1 accepted |
| s250.8381_plan | 02:59 to 05:10 | 2 | 5.8e-23, no trial accepted at step 1 | +2.210e-09 | lam 1/16 after 4 |
| s251.8859_plan | 02:59 to 04:48 | 2 | 4.1e-24, no trial accepted at step 1 | +9.060e-11 | lam 1/2 after 1 |
| s252.6135_plan | 04:49 to 06:24 | 2 | 2.5e-20, no trial accepted at step 1 | +2.930e-09 | lam 1/8 after 3 |
| s253.5301_plan | 05:11 to 06:11 | 1 | 5.2e-36, the start's, no trial accepted at step 0 | none | all 9 refused, lam 1 to 1/256 |

`table808_plan.txt` gives the first dDelta (the first step's undamped correction, the linear response), the steps and the
final max|F| above, and: held, Delta(d6) - Delta(d10): incomplete; plan, delta(plan): incomplete; exit 2. No polish saved a
base, so no delta(plan) = Delta(polished) - Delta(#603) exists, and neither the registered bands nor the control apply.
The control check `--mutate=swap` was not run, since no converged control exists to swap.

What the logs show. At 250.8381, 251.8859 and 252.6135 step 0 was accepted at a lam below 1 and raised max|F| from the
start's 3.62e-36, 3.10e-36 and 2.68e-36 to 5.8e-23, 4.1e-24 and 2.5e-20. At step 1 their lam 1 trial then reached max|F|
7.15e-31, 2.08e-31 and 3.08e-36, far below that, and was refused each time because the raw simplified correction
|dz_t| was not below |dz| (2.56e-9 against 3.33e-18 at 252.6135). The smaller trials of 252.6135's step 1 gave max|F|
from 1.2e-20 to 5.9e27. At 240.1244 `|dz|` halved per step from step 1 to step 9 (9.9e-27 to 1.9e-29), as #800's t0
did for its first three steps before it sped up, and here it did not speed up. At 253.5301 step 0's first correction
has |dz| 1.004e-07 and the nine trials' max|F| runs from 9.94e36 (lam 1) to 1.19e24 (lam 1/256), so the polish never
left the start's 5.2e-36.

run808.sh and run808b.sh as placed call bash $0 after a cd, so run them by absolute path; plandrop was relaunched that way at 06:28:53 UTC.

## Results, plandrop (dh370, 2026-11-15)

What ran. Unit `i808drop`, `bash /home/nathan/Source/choptuik-large-d-raw/I808-dh370/run808b.sh plandrop` (worktree
choptuik-large-d-808b at bd4ada6c, venv-i800), the five states with `--keep_plan 0 --od_full_drop 1e-6`, three at a time at
4 threads, nice 10. The first launch at 06:28:14 UTC ran no job (relative `$0` after the cd, `plandrop_nolaunch_run.log`,
`table808_plandrop_nolaunch.txt`); the run is the relaunch at 06:28:53 UTC (`i808drop_journal.log`, `exits_808.txt`). One
polish ran past 4 h, so I stopped the unit at 10:29:27 UTC (`exits_808.txt`); run808b.sh's own table step then did not run, and
`table808_plandrop.txt` is the same `table808.py ... --plan_tag=plandrop` run by hand at 10:29:36 UTC. Exit 2, as expected: the
held arm has no jobs.

| job | start to end (UTC) | steps | final max\|F\| | first dDelta | Delta - Delta(#603) |
|---|---|---|---|---|---|
| s240.1244_plandrop | 06:28 to 09:07 | 16, no trial accepted at step 15 | 3.4e-25 (start 6.1e-36) | +2.610e-16 | none |
| s250.8381_plandrop | 06:28 to 10:29 | 17 done, 18th under way, stopped at 4 h | 7.17e-50 | +2.210e-09 | none |
| s251.8859_plandrop | 06:28 to 08:02 | 13, converged | 2.1e-64 | +9.060e-11 | +9.05849e-11 |
| s252.6135_plandrop | 08:02 to 09:56 | 3, no trial accepted at step 2 | 3.1e-36 (start 2.7e-36) | +2.930e-09 | none |
| s253.5301_plandrop | 09:07 to 10:12 | 1, no trial accepted at step 0 | 5.2e-36, the start's | none | none |

`table808_plandrop.txt`: plan, delta(plan): incomplete. Only 251.8859 converged, so no band of the registered rule applies
and the control (the held arm at 240.1244) was not measured. The base of 251.8859 is `s251.8859_plandrop/base_pin3_D251.8859.npz`;
the other four saved none.

What the logs show.
- The full-step rule did what it was made for at 250.8381, 251.8859 and 252.6135: after a damped step 0 raised max|F| to
  5.8e-23, 4.1e-24 and 2.5e-20, step 1's lam 1 trial fell to 7.2e-31, 2.1e-31 and 3.1e-36 and was accepted by the drop that
  the own test had refused in the plan arm. At 251.8859 this repeated at steps 3 and 5, and |dz| fell from 5.7e-20 (step 6)
  to 3.7e-70 (step 11).
- 250.8381 went through 7 cycles (steps 0 to 13) of an even step at lam 1/16 to 1 that raised max|F| to between 6e-23 and
  8e-22 and an odd step at lam 1 that dropped it to between 3e-37 and 7e-31; the even steps' dDelta fell 2.21e-9, 2.06e-9,
  1.56e-9, 1.17e-9, 1.02e-9, 5.1e-10, 2.6e-10. From step 13 on, max|F| went 2.9e-37, 1.7e-32, 1.4e-49, 7.2e-50 and |dz|
  2.1e-15, 5.5e-24, 2.3e-27, 1.2e-27, with lam 1/2 at step 16 and |dz| halving per step, as 240.1244's did, so convergence
  to 1e-60 needed tens of further steps at about 6 min each. The sum of
  lam x dDelta over its accepted steps (from the log's 3-digit values) is +2.21e-9, the first dDelta; it is not a converged
  delta, and the registered rule does not use it.
- 252.6135 at step 2 and 253.5301 at step 0 refused all 9 trials (lam 1 to 1/256): from a start at 3e-36 and 5e-36 there is
  nothing for the drop rule to accept. At 253.5301 the first correction has |dz| 1.004e-07 and the trials' max|F| is
  9.9e36 at lam 1 and 1.2e24 at lam 1/256, falling about 27 times per halving.
- 240.1244 (the control's state) stopped at step 15 with lam 1 at 1.5e-26 against 3.4e-25, a 22-fold drop, short of 1e-6.

First dDelta over E (not a registered quantity): 240.1244 8.7e-3, 250.8381 3.1e-2, 251.8859 3.9e-4, 252.6135 9.7e-3. Where a
delta exists, it agrees with the first dDelta (251.8859 +9.05849e-11 against +9.060e-11).
