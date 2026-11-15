# I852-mac: Newton's contraction in the horizon data at D 240.1244

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/852

Code: hp/step_spread.py on wip/xf-852 (5904a658, on #850's wip/xf-850 d78c0a90, from main 4694993d), which adds
`--steps N`, several rels per run (`--rel 1e-90,1e-93,1e-96`) and `--mutate nostep`, on main 3c35f0c's hpkernel. One
process at nice 10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). State: I603-win2/chain/anm_pin3_D240.1244.npz
in #837's truth_system. Runs in `queue.sh` order, after I850-mac's queue.

In progress.

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
