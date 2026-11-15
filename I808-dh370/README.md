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
