# I852-mac: Newton's contraction in the horizon data at D 240.1244

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/852

Code: hp/step_spread.py on wip/xf-852 (5904a658, on #850's wip/xf-850 d78c0a90, from main 4694993d), which adds
`--steps N`, several rels per run (`--rel 1e-90,1e-93,1e-96`) and `--mutate nostep`, on main 3c35f0c's hpkernel. One
process at nice 10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). State: I603-win2/chain/anm_pin3_D240.1244.npz
in #837's truth_system. Runs in `queue.sh` order, after I850-mac's queue.

## Answer

Newton does not contract the m_h, a_h move step by step at any of the three rels, so the prediction (contraction at
1e-96, none at 1e-90) fails. At every rel the first step multiplies the move by 9.306e3 plus #840's quadratic part,
which shows at 1e-90 (excess 7.5556e92 per rel², against #840's 7.5565e92). The second step brings max|z_k − u_k| /
max|z_h| to 1.2972e-99 .. 2.7269e-99 at every rel, the iteration's own floor, where the unperturbed path's step also
settles (2.3719e-98 at k 2, 1.1622e-99 at k 3, below all three rels from k 2 on).

So Newton removes the move in two steps at every rel. What stops a contraction at the first step is the start: the
stored truth is 3.2085e-57 of |z_h| from the root it converges to. At a point whose own step is d0, Newton's map has
derivative −J⁻¹F''(·, d0), which turns the move into a first-order change of the step. That gain vanishes at an exact
root, and the centre block's is at the floor (e_1 2.9742e-99 from e_0 9.9987e-91).

## The measure (changed before the run, agreed with the coordinator)

The issue asks for max|z − z_truth| / max|z_h| after each step. The stored truth is itself one Newton step of max|dz|
3.2088e-57 from the root (#840), so after a step that distance reads about 3e-57 at every rel, whatever the perturbation
does. The contraction is read instead from max|z_k − u_k| / max|z_h|, where u_k is the unperturbed path's k-th iterate
(Newton from the stored truth, the same number of steps). That is the perturbation's own error, which does not see the
truth's. max|z_k − z_truth| / max|z_h| is recorded as asked, and so is the unperturbed path's own step
max|u_k − u_(k−1)| / max|z_h|, to show whether it settles below the perturbations' scales (1e-90 .. 1e-96).

## Criteria (posted on the issue before the runs)

| # | criterion | fails when |
| --- | --- | --- |
| C1 | `--ref` passes in every run (−4.3765436014297066e-58, #840) | the unperturbed step changes |
| C2 | the control `--mutate nostep` (z_k left at z_(k−1)) reads "does NOT contract" at rel 1e-96 | it reads "contracts" |
| C3 | the centre block at rel 1e-90 (where Newton returns the move, #840 at D 252.6) reads "contracts" | a positive control that does not contract stops the reading of the main run |
| C4 | the prediction: max\|z_k − u_k\| / max\|z_h\|, from max\|move\| / max\|z_h\| at k = 0, falls at each of three steps at rel 1e-96 and does not at 1e-90 | contraction at 1e-90, or none at 1e-96 |
| C5 | the unperturbed path's step max\|u_k − u_(k−1)\| / max\|z_h\| per k, against 1e-90 .. 1e-96 | (reported; where it does not settle below them, the reading of C4 is qualified) |

## Results

| # | verdict | numbers (`tables.md`, from `tables.py`) |
| --- | --- | --- |
| C1 | pass | `--ref` equal in 3 of 3 runs (−4.3765436014297066e-58) |
| C2 | pass | `ctl_nostep_D240`: e_k 1.0000e-96 at k 0, 1, 2, "does NOT contract" |
| C3 | pass | `ctl_centre_D240` at rel 1e-90: e_k 9.9987e-91, 2.9742e-99, 2.5172e-99, "contracts" |
| C4 | FAIL | "does NOT contract" at all three rels; gain e_1 / e_0 1.0062e4 (1e-90), 9.3068e3 (1e-93), 9.3060e3 (1e-96) |
| C5 | reported | the unperturbed step 3.2085e-57, 2.3719e-98, 1.1622e-99 at k 1, 2, 3: below 1e-90, 1e-93 and 1e-96 from k 2 on |

| rel | e_0 | e_1 | e_2 | e_3 | gain e_1 / e_0 |
| --- | --- | --- | --- | --- | --- |
| 1e-90 | 1.0000e-90 | 1.0062e-86 | 1.7251e-99 | 2.7269e-99 | 1.0062e+04 |
| 1e-93 | 1.0000e-93 | 9.3068e-90 | 2.0136e-99 | 1.7348e-99 | 9.3068e+03 |
| 1e-96 | 1.0000e-96 | 9.3060e-93 | 1.2972e-99 | 1.8359e-99 | 9.3060e+03 |

e_k = max|z_k − u_k| / max|z_h|, e_0 = move / max|z_h|, max|z_h| 1.000111062.

### Notes

- The measure: max|z_k − z_truth| / max|z_h| reads 3.2085e-57 after every step at every rel (`steps_D240.log`), the
  truth's own distance from the root, as expected before the run. It says nothing about the move.
- The excess, (gain(1e-90) − gain(1e-96)) / 1e-90 = 7.5556e92, is a difference of max norms, not a fit by component.
  It agrees with #840's max|dz| / rel² 7.5565e92 at rel 1e-65..1e-67 to four digits (`I840-mac/tables.md`).
- At k 2 and 3, e_k is 1.2972e-99 .. 2.7269e-99 and does not fall. The unperturbed path's own step at k 3 is
  1.1622e-99, and max|F| stays at 4.5e-94 .. 1.7e-93 at the last iterates (`steps_D240.log`). That is the octo-double
  floor of the plain step, so a reading that asks e_k to fall at each of three steps cannot pass once e_k reaches it.
- The derivative −J⁻¹F''(·, d0) is Newton's map differentiated by hand (the step is −J⁻¹F, and d0 = −J⁻¹F at the
  start); it is not checked here beyond the gain's independence of rel.

## Discrepancies

- The issue's prediction (contraction at 1e-96, not at 1e-90) fails. It assumed a start at the root; the stored truth
  is 3.2085e-57 of |z_h| away, and the gain it gives (9.306e3) does not depend on rel.
- C4 as written (falls at each of three steps) is not well posed past k 2, where e_k is at the iteration's floor. That
  is a fault of the criterion, posted by this runner before the run, not of the code.

## Recommended tasks

1. **A re-converged truth at D 240.1244.** What: store u_2 (two plain Newton steps from #837's truth; max|F| before
   step 3 5.4062e-94, against 1.7135e-66 at the truth) in eight parts as a state beside anm_pin3_D240.1244.npz, with
   #837's held values and plan. Why: the stored truth is 3.2085e-57 of |z_h| from its root, and that offset makes the
   first step's response to the horizon move linear with gain 9.306e3 (#852), and may add a cross term to the linear
   return of a Δ move (#857). Acceptance: the new state's own plain step max|dz| / max|z_h| at most 1e-97 and max|F|
   at most 1e-92, read back through `truth_system`; fails otherwise. Depends on #852, #837.
2. **#852 from the re-converged root.** What: `step_spread.py --steps 2` with m_h, a_h at rel 1e-90, 1e-93, 1e-96 from
   task 1's state. Why: it tests the issue's prediction without the start's offset. Acceptance, read at the first step:
   gain e_1 / e_0 below 1 at 1e-96 and above 1 at 1e-90, and at 1e-90 gain / rel within 10% of 7.5556e92 (#840's
   quadratic part); fails otherwise. Depends on task 1.
