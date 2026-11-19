# I1027-dh610: M = 7 at the two low-omega M = 5 zeros of #1026: do their harmonics decay?

Machine: dh610 (Fedora, i7-12700, 20 threads, 62 GB), beside #1003's K 49 run (5 procs). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1027 (#1026's recommendation 2; coordinator's order of
2026-11-19 ~13:10 UTC). Code: `hier_nb.py` of `~/Source/cl-995` (fc7dee4d), venv `~/Source/venv-i1026` (numba 0.68.1), `INNER_NB_RTOL=1e-13`, 2 procs per solve, nice 10.

## Route

`walk1027.py` is #1026's outer Newton over complete fixed-(A, w) solves (walk1026.py) at M = 7, with the M = 7 flags of `proof/B_tail_M7.md` (`--pretune --fixA --schur --predict --floor --h3=1e-4`, xi1 0.15 the matching
radius of the known M = 7 zero), F_7 started at zero, and the perturbed-repeat protocol of #976/#977/#1002 for solves above the bar. One solve takes about 80 s. `logs/probe_m7_control_single_solve.log` is
one solve at the known M = 5 zero with F_7 = 0 (|F7/F5| 0.0574, |r_3| 2.4e-5 above the 1e-6 bar, which the repeats address).

## Readings, fixed before the runs

- **Control.** The known zero, started at its M = 5 zero (2.718579189, 0.999228403) with F_7 = 0, must converge to (2.71924, 1.000025) within 3e-4 in A and in w/w_inf (the stored zero is +-1e-5 over several
  solves, one walk's noise is about 3e-4: |r_1| scatters by about 1 over a Jacobian whose smallest singular value is 3e3), with |F7/F5| at its first solve within 5% of 0.0574. If not, the run stops.
- **Low-omega zeros** z2275 = (2.227529, 0.092574) and z2584 = (2.583888, 0.141358): |F7/F5| and |F5/F3| from the first solve (fixed A, w at the M = 5 zero) and, when the walk converges, at the M = 7 zero, and
  the M 5 -> 7 shift (Euclidean norm in (A, w/w_inf)). CONVERGES: |F7/F5| <= 0.2 and the walk converges to a zero with a M 5 -> 7 shift smaller than the M 3 -> 5 one, taken as the smaller of the two pairings
  (nearest M = 3 zero: 0.1113 for z2275, 0.0817 for z2584; the walk's origin in #1026: 0.3929 and 0.2719). DOES NOT: |F7/F5| >= 0.3, or no M = 7 zero near it (the start or a Jacobian solve fails, or no step
  lowers |r_1|). UNDECIDED otherwise (the ratio between 0.2 and 0.3, an iteration cap, or the shift not smaller).
- Primary radius xi1 0.15 (the control's); 0.2 and 0.25 are exploration (the control is not validated there).

## Files

| file | content |
|---|---|
| `common1027.sh`, `run1027.sh` | paths and the driver (the commands are in it) |
| `walk1027.py`, `eval1027.py` | the M = 7 walk, the readings' evaluator (selftest, mutations) |
| `walks/`, `logs/`, `exits_1027.txt`, `memlog_1027.log` | one JSON per walk, each attempt's and walk's log, exits, alert-only memory log |

## Results, 2026-11-19 (13:15-14:31 UTC; `logs/eval_all.log`, `eval_all.txt`)

- Control PASS (`logs/walk_control_xi0.15.log`): 4 solves (each with one perturbed repeat), M = 7 zero (2.719236, 1.000024), 3.8e-6 and 6.8e-7 from the stored (2.71924, 1.000025); |F7/F5| 0.0573 (stored 0.0574).
- xi1 0.15 (primary): both low-omega zeros DOES NOT (no M = 7 zero near it: the start solves stay at |r_3| 60 and 1.3e4).
- xi1 0.25 (exploration, the control is not validated there): z2275 -> M = 7 zero (2.233308, 0.065740), z2584 -> (2.573290, 0.100532), converged with |r_3| about 1e-9. |F7/F5| 0.676 and 0.634 at those zeros (0.650 and 0.568 at the M = 5 zeros), |F5/F3| 0.587 and 0.555, M 5 -> 7 shift 0.027 and 0.042. DOES NOT (|F7/F5| >= 0.3).
- xi1 0.2: start solves not converged (|r_3| 10 and 2.6e-6), ratios 0.620/0.575 and 0.570/0.507 at the M = 5 zeros.
- `logs/radius_check_*`: the xi1 0.25 walks' best points solved again at xi1 0.2 and 0.3: |r_1| 0.03 to 0.28 against Jacobian singular values of 270 to 5e3, |F7/F5| and |F5/F3| equal to four digits at the three radii (0.6759/0.5868 and 0.6339/0.5553). `radius_check1027.py`.
- Evaluator controls: `logs/eval_selftest.log` PASS; `logs/eval_mutate_shift.log` makes the control FAIL (exit 1); `logs/eval_mutate_ratio.log` turns the two converged walks UNDECIDED (the walks without an M = 7 zero stay DOES NOT).
