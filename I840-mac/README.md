# I840-mac: step_spread in #837's truth_system at D 240.1, 245.6, 250.2 and 252.6

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/840

Code: hp/step_spread.py at main 0cfff3c4 (worktree wip/xf-840), unchanged, on main 3c35f0c's hpkernel. One process
at nice 10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). States: I603-win2/chain/anm_pin3_D*.npz, read in eight
parts with held values in eight parts and the stored plan (#837's truth_system, printed by each run as "truth read in
8 of 8 parts, held values eight parts, plan stored"). Each step took 360-900 s, each D 84-113 min.

Every number below is printed by a log of this folder or by `python3 tables.py` (output in `tables.md`), run from
this folder with numpy.

## Answer

The Δ step reads "not determined" at all four D under #827's 1e-3 bar. That bar is relative to the unperturbed step,
which at a true root is 5e-82 to 8e-49 in size, so any measurable response fails it. At D 240.1244 the response is
exactly quadratic in the move (p = 2.0000 over two decades), so it is Newton's own second-order term from a point
1e-65 off the root, not an undetermined step. From D 245.6 on, the 1e-65 move changes the smallest pivot by factors
0.66 to 226, so there the move is outside the Jacobian's own linear range, and the spread stops growing between 250.2
and 252.6.

## Acceptance

| criterion | verdict | number |
| --- | --- | --- |
| zero perturbation reproduces the unperturbed step exactly | pass | the repeat's eight parts and pivot the same at 4 of 4 D; `--ref` equal as a double at 240.1244 (−4.3765436014297066e-58, from I837-mac/step_D240_dz0.npz) and 252.6135 (+5.2645963792835124e-82, I837-mac/ss_D252.log); no stored step at 245.6 and 250.2 |
| the controls stay equal as a double | pass | centre and nodes 0-4, 6 of 6 at each D |
| the repeat check can fail | pass (fires) | `ss_D240_repeatctl`: the centre moved by 1e-65 gives the same dΔ to 10 digits but different eight parts: FAIL, exit 1 |
| the verdict's and bands' rules can fail | pass (fire) | `selftest` PASS; `--mutate=bar` FAIL (3 wrong); `--mutate=band` FAIL (2 wrong) |
| spread, verdict, spread / E and band per D | reported | table below; "not determined" and "below 1e-2" at every D |
| slope of log(spread) against D vs 1.44 | 1.568 | ratio 1.089 to #805's 1.44 over 4 points; log(E) at the same D 1.30; pairwise 1.91, 1.89, −0.36 |

## Per D (`sum.log`)

E = 2.2e-37 / p_min with #805's p_min (I830-mac/table805.json). The spread is the largest |dΔ(seed) − dΔ(unperturbed)|
over four random-sign seeds, exact from the eight parts: an estimator range over perturbations, not a statistical
error bar. The sd is the four seeds' sample standard deviation.

| D | state max\|F\| | unperturbed dΔ | smallest pivot = p_min | spread | seeds' sd | E | spread / E | band |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 240.1244 | 1.71e-66 | −4.3765e-58 | 7.306e-24 | 2.6732e-38 | 1.1392e-39 | 3.011e-14 | 8.878e-25 | below 1e-2 |
| 245.6366 | 5.02e-66 | +3.3839e-53 | 4.374e-27 | 1.0179e-33 | 1.3973e-34 | 5.029e-11 | 2.024e-23 | below 1e-2 |
| 250.1676 | 3.05e-61 | +7.6531e-49 | 1.069e-29 | 5.3618e-30 | 2.2544e-30 | 2.059e-08 | 2.605e-22 | below 1e-2 |
| 252.6135 | 5.55e-92 | +5.2646e-82 | 7.287e-31 | 2.2368e-30 | 1.0148e-30 | 3.019e-07 | 7.409e-24 | below 1e-2 |

The unperturbed smallest pivot equals #805's p_min at every D (the ratio prints 1.000000). In #830's float-held system
it did not at 245.6-252.6 (3.263e-27, 6.015e-29, 7.095e-29 against 4.374e-27, 1.069e-29, 7.287e-31).

Per seed, the dΔ and the smallest pivot (from `tables.md`):

| D | seed dΔ (1, 2, 3, 4) | signs | seed pivot / unperturbed pivot |
| --- | --- | --- | --- |
| 240.1244 | +2.420e-38, +2.673e-38, +2.403e-38, +2.409e-38 | all + | 1, 0.999, 1, 1 |
| 245.6366 | −1.018e-33, −9.941e-34, −6.941e-34, −7.706e-34 | all − | 0.659, 0.677, 0.891, 0.699 |
| 250.1676 | −5.992e-31, +3.674e-31, −5.362e-30, −4.433e-31 | mixed | 3.9, 6.2, 0.688, 4.69 |
| 252.6135 | −5.726e-31, +5.897e-31, −2.237e-30, −4.073e-31 | mixed | 173, 171, 72.7, 226 |

The move raises max|F| from the state's own value to 1.07e-28, 7.56e-28, 3.77e-27 and 8.97e-27: the horizon rows'
gain of about 1e37 to 1e39 per unit relative move.

## The power diagnostic (registered on the issue before it ran)

Seed 1 at rel 1e-65 (`ss_D240`), 1e-66 and 1e-67 (`pw_D240_r66`, `r67`), the same signs, at D 240.1244. Rule: both
p = log10(dev(rel) / dev(rel / 10)) in [1.8, 2.2] is quadratic, both in [0.8, 1.2] linear, otherwise neither.

| rel | dΔ | max\|dz\| | smallest pivot | max\|F\| |
| --- | --- | --- | --- | --- |
| 1e-65 | +2.420020e-38 | 7.5565e-38 | 7.305107e-24 | 1.0658e-28 |
| 1e-66 | +2.419916e-40 | 7.5564e-40 | 7.306078e-24 | 1.0658e-29 |
| 1e-67 | +2.419905e-42 | 7.5564e-42 | 7.306175e-24 | 1.0658e-30 |

p = 2.0000 at both decades: **quadratic**. dΔ / rel² is 2.42e92 and max|dz| / rel² 7.556e92 at all three, while the
residual is linear in rel. The step's largest component is this quadratic part, not the move's own −h (1.0e-65 at
rel 1e-65). The two are equal at rel 1.32e-93: at D 240.1 a Newton step from horizon data off by more than about
1e-93 relative is dominated by its second-order term. The `--ref` check passed in both runs.

The power was measured at D 240.1 only. At 245.6-252.6 the seeds move the pivot by factors 0.66 to 226, so a
quadratic reading there is not established (recommended task 1).

## The Delta control

The Delta block moved alone by rel 1e-65 (seed 1). Newton's step returns the move only if |dΔ| / move is 1.

| D | Delta move | dΔ after it | \|dΔ\| / move | max\|F\| after it |
| --- | --- | --- | --- | --- |
| 240.1244 | 1.6866e-65 | +1.1027e-49 | 6.538e+15 | 1.988e-34 |
| 245.6366 | 1.6857e-65 | −9.8677e-46 | 5.854e+19 | 1.319e-33 |
| 250.1676 | 1.6849e-65 | −1.7367e-42 | 1.031e+23 | 6.237e-33 |
| 252.6135 | 1.6845e-65 | −1.1274e-41 | 6.693e+23 | 1.442e-32 |

Not a check of step_spread (it prints the ratio only). Its power in the move is unmeasured (recommended task 2).

## Discrepancies

1. #827's verdict compares against the unperturbed dΔ. At a true root that is the image of a residual of 3e-61 ..
   6e-92, so "not determined" follows for any response above 1e-3 of it. At D 240.1 the response is the move's
   second-order term. The verdict does not decide the question at true roots, and the spread (absolute) is the usable
   number.
2. #808's bands were set for the float-held system (#830: spread / E 1.9e-2 .. 20.5). Here every ratio is 1e-22 ..
   1e-25, so "below 1e-2" holds by more than 20 orders and does not discriminate.
3. The fit over four D (1.568) mixes regimes. The first three D give 1.904, and 250.2 -> 252.6 gives −0.357, where the
   move changes the pivot by 73-226×. Neither 1.568 nor 1.904 is a clean rate against #805's 1.44.
4. At D 250.1676 the state's own max|F| is 3.05e-61, about five orders above D 240.1's and 245.6's (1.7e-66, 5.0e-66)
   and about 31 above 252.6's. The centre and node controls there leave max|F| at 3.0469e-61, unchanged by the 1e-65 move.

## Recommended tasks

1. **The horizon response's power at D 245.6-252.6.** What: step_spread with `--seeds 1 --controls 0 --repeat 0` at
   rel 1e-70, 1e-75 and 1e-80 at D 245.6366, 250.1676 and 252.6135 (and `--ref` at 252.6), with the smallest pivot
   per run. Why: at these D the 1e-65 move changes the pivot by 0.66-226×, so the spread there is not the quadratic
   term measured at 240.1, and the growth with D is not established. Acceptance (each can fail): at each D a rel where
   the seed's pivot is within 1% of the unperturbed one, and p in [1.8, 2.2] over two decades below it; then dΔ /
   rel² against D, fitted, against 1.44 and against twice 1.44. Estimate: about 15 min per run, 9 runs, 2.3 h at 3
   threads. Depends on #840.
2. **Newton's return from a pure Δ move.** What: add `--blocks NAME[,NAME]` to hp/step_spread.py so a run perturbs
   only the named blocks with the seeds; run the Delta block at rel 1e-65, 1e-66 and 1e-67 at D 240.1244 and 252.6135.
   Why: the Delta control's |dΔ| / move is 6.5e15 at 240.1 and 6.7e23 at 252.6, where an accurate Newton step gives 1.
   Acceptance: the power rule above (quadratic, linear or neither), with `--ref` passing; the new option's control:
   `--blocks centre` reproduces the centre control's dΔ as a double. Estimate: about 1.5 h. Depends on #840.
3. **Newton's contraction in the horizon data at D 240.1.** What: from seed 1's state at rel 1e-90, 1e-93 and 1e-96,
   take three Newton steps and record max|z − z_truth| / max|z_h| after each. Why: the step's quadratic part equals
   the move at rel 1.32e-93, which predicts that Newton contracts below about 1e-93 and not above; the chain's
   corrector meets horizon errors of unknown size. Acceptance: contraction (error falling each step) at 1e-96 and
   not at 1e-90, or the prediction fails as stated. Estimate: about 1 h. Depends on #840, and on recommended task 2's
   option if it is used to perturb only m_h and a_h.

## Files

| file | what |
| --- | --- |
| `ss_D240`, `ss_D245`, `ss_D250`, `ss_D252` `.log`, `.json` | unperturbed, repeat, horizon seeds 1-4 at 1e-65, controls (centre, nodes 0-4, Delta) |
| `ss_D240_repeatctl` | the repeat check's control (`--mutate repeat`): FAIL, as it must |
| `selftest*.log` | the verdict's and the bands' rules; `--mutate=bar` and `--mutate=band` fail |
| `pw_D240_r66`, `pw_D240_r67` | the power diagnostic, seed 1 at rel 1e-66 and 1e-67 |
| `sum.log`, `sum.json` | `step_spread.py sum` with I830-mac/table805.json |
| `tables.py`, `tables.md` | this README's per-seed, Delta-control, power and slope numbers |
| `run.sh`, `queue.sh`, `queue2.sh`, `*.done`, `queue*.log` | how the runs were made |
