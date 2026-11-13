# I623-win: the sigma-model's Delta(eta) at D = 4, k_c 23 and 39 (is it monotonic at large eta?)

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/623 (the coordinator's message `choptuik-large-d/2026-11-12/232500Z-coordinator-4cd7.md` and the commands in the issue's first comment). Worktree `choptuik-i623` at main ef1df85e, `solver/matter`, venv-t151 (Python 3.10, numpy 2.2.6, scipy 1.15.3). Pure Python, no hp kernel.

## Plan, written before the runs (the issue's acceptance)

- Seeds: the four converged k_c = 15 points of `data/sigdss_d4eta15.npz` (rows 0, 1, 2, 4 of `Z`: eta = inf, 10, 5, 2; Delta 0.46002147042605496, 0.4599633445382349, 0.45995609148619604, 0.4602767611524812, which are the issue's values), saved as `data/sigdss_sol_i623seed_D4.0000_eta{E}.npy`.
- Eight refines, one process each, `OPENBLAS_NUM_THREADS=1`, below-normal priority, from `solver/matter`:
  `python -u sigdss_run.py refine data/sigdss_sol_i623seed_D4.0000_eta{E}.npy --D 4 --eps {EPS} --kc_seed 15 --kc {KC} --kappa 0.5 --tag i623_kc{KC}_eta{E}`
  with (E, EPS) = (inf, 0), (10.0000, 0.1), (5.0000, 0.2), (2.0000, 0.5) and KC = 23 and 39. Each run's stdout goes to `logs/kc{KC}_eta{E}.log`; its record `data/sigdss_refine_i623_*.jsonl` and state `data/sigdss_sol_ref_i623_*.npy` are copied here from the worktree.
- Order: pilot KC 39 at eta = inf alone (if its first Newton step has not finished within 30 min, stop and report its log); then the four KC 23 runs, four at a time; then the other KC 39 runs.
- Pass: every run converges (`F` below 1e-10 in its record). Then the sign of Delta(5) - Delta(inf) at k_c 23 and at 39, and each difference against the change of the same quantity between the two resolutions. The question is answered if the sign is the same at both k_c and both differences exceed that change; otherwise it stays open and the summary says so. Reference: eta = inf at k_c 23 gave Delta = 0.4598654552 in `data/sigdss_log_d4eta_kc23_aborted.txt`, which the run must reproduce.
- With d_kc = Delta_kc(5) - Delta_kc(inf), "their change between the two resolutions" is read as c = |d_39 - d_23|, written here before the data are read: the question is answered if sign(d_23) = sign(d_39) and |d_23| > c and |d_39| > c. The table also gives d at k_c 15, 23 and 39 and the change of each Delta between resolutions, so any other reading can be checked.

## Summary

The question is **answered** by the issue's rule. All eight runs converge, and the sign of Delta(5) - Delta(inf) is **negative at both k_c**: -4.427e-5 at k_c 23 and -4.326e-5 at k_c 39 (-6.538e-5 at k_c 15). Both differences exceed their change between the two resolutions, c = |d_39 - d_23| = 1.008e-6, by factors of 44 (k_c 23) and 43 (k_c 39). So Delta(5) lies below Delta(inf) at every resolution, and the k_c 15 table's non-monotonicity (0.459956 at eta 5, 0.459963 at 10, 0.460021 at inf) is not a truncation artefact: it persists, with the same sign and about the same size, at k_c 39 where the constraint is 76 to 98 times smaller than at k_c 23.

## What ran

`run_623.py` (logs/run_623.log), BelowNormal, one thread each (`OPENBLAS_NUM_THREADS=1`), venv-t151 (Python 3.10, numpy 2.2.6, scipy 1.15.3), worktree `choptuik-i623` at main ef1df85e:

| run | start (UTC) | end | wall |
|---|---|---|---|
| pilot: k_c 39, eta inf | 2026-11-12 23:26:48 | 2026-11-13 00:19:43 | 3175 s (first Newton step done at 1423 s, inside the 30 min limit) |
| k_c 23, four runs | 23:51:01 | 00:02:12 to 00:02:37 | 671 to 696 s |
| k_c 39, eta 10, 5, 2 | 00:03:07 | 01:00:28 to 01:01:38 | 3441 to 3511 s |

The pilot ran alone for its first step (23:26 to 23:51), then beside the four k_c 23 runs (5 busy threads), then beside the three k_c 39 runs (4 busy threads); the pilot's working set peaked at 480 MB when last checked (23:50). The seeds are rows 0, 1, 2, 4 of `data/sigdss_d4eta15.npz` (eta = inf, 10, 5, 2; their Delta match the issue's). Each refine's record is `data/sigdss_refine_i623_kc{KC}_eta{E}.jsonl`, its state `data/sigdss_sol_ref_i623_*.npy`, its log `logs/kc{KC}_eta{E}.log`. `kc15_values.py` evaluates the seeds' F and constraint the way `refine` does (SigDSS at k_c 15, frozen with kappa 0.5, no Newton step), `table_623.py` makes the table below (`table_623.txt`).

## Results (`table_623.txt`)

| eta | k_c | N | Delta | F | constraint | solve s |
|---|---|---|---|---|---|---|
| inf | 15 | 48 | 0.4600214704 | 5.88e-12 | 1.1761e-01 | (seed) |
| inf | 23 | 72 | 0.4598654552 | 1.61e-15 | 1.5305e-02 | 671 |
| inf | 39 | 120 | 0.4598611019 | 3.67e-12 | 2.0111e-04 | 3172 |
| 10.0000 | 15 | 48 | 0.4599633445 | 6.27e-11 | 1.0702e-01 | (seed) |
| 10.0000 | 23 | 72 | 0.4598180153 | 1.55e-15 | 1.4062e-02 | 694 |
| 10.0000 | 39 | 120 | 0.4598141853 | 3.32e-12 | 1.7514e-04 | 3507 |
| 5.0000 | 15 | 48 | 0.4599560915 | 1.99e-14 | 9.6252e-02 | (seed) |
| 5.0000 | 23 | 72 | 0.4598211881 | 1.67e-15 | 1.2754e-02 | 695 |
| 5.0000 | 39 | 120 | 0.4598178425 | 2.44e-12 | 1.5065e-04 | 3495 |
| 2.0000 | 15 | 48 | 0.4602767612 | 2.40e-15 | 7.3747e-02 | (seed) |
| 2.0000 | 23 | 72 | 0.4601707267 | 1.53e-15 | 8.7763e-03 | 692 |
| 2.0000 | 39 | 120 | 0.4601686037 | 1.63e-12 | 8.9776e-05 | 3439 |

runs present: 8 of 8; every run converged (F < 1e-10): True
eta = inf at k_c 23: Delta 0.4598654552 against the Mac's 0.4598654552: difference +2.19e-11

| eta | Delta - Delta(inf) at k_c 15 | at k_c 23 | at k_c 39 | c = abs(d_39 - d_23) |
|---|---|---|---|---|
| 10.0000 | -5.813e-05 | -4.744e-05 | -4.692e-05 | 5.233e-07 |
| 5.0000 | -6.538e-05 | -4.427e-05 | -4.326e-05 | 1.008e-06 |
| 2.0000 | +2.553e-04 | +3.053e-04 | +3.075e-04 | 2.230e-06 |

change of each Delta between resolutions:
| eta | Delta_23 - Delta_15 | Delta_39 - Delta_23 |
|---|---|---|
| inf | -1.560e-04 | -4.353e-06 |
| 10.0000 | -1.453e-04 | -3.830e-06 |
| 5.0000 | -1.349e-04 | -3.346e-06 |
| 2.0000 | -1.060e-04 | -2.123e-06 |

VERDICT (rule on eta = 5): ANSWERED: same sign -, |d_23| 4.427e-05 and |d_39| 4.326e-05 both exceed c = 1.008e-06
sign of Delta(5) - Delta(inf): k_c 23 -, k_c 39 -
(outside the rule) Delta(5) - Delta(10) at k_c 15, 23, 39: -7.253e-06, +3.173e-06, +3.657e-06
(outside the rule) eta = 10.0000: same sign -, |d_23| 4.744e-05 and |d_39| 4.692e-05 both exceed c = 5.233e-07
(outside the rule) eta = 2.0000: same sign +, |d_23| 3.053e-04 and |d_39| 3.075e-04 both exceed c = 2.230e-06

Notes on the table. The k_c 15 F and constraint are recomputed from the seeds, not read from the continuation's records. The record's F at k_c 39 (1.6e-12 to 3.7e-12) is that of `refine`'s second Newton pass, run after the Runge-Kutta step counts are re-frozen; the first pass reached 2e-15 to 4e-15 (`logs/kc39_*.log`, the last `jac` line), and both are far below the 1e-10 criterion.

## Controls

- **The verdict can fail.** `table_623.py --selftest` runs the rule on six planted (d_23, d_39) pairs, two that must be answered and four that must stay open (two sign changes, two where c exceeds a difference), and all six come out as expected. On the real data, adding +1e-4 to Delta(5) at k_c 39 (`--shift 1e-4`, `table_623_shift_plus1e-4.txt`) turns the verdict to OPEN (signs differ, d_39 = +5.674e-5), and so does +4.4e-5 (d_39 = +7.4e-7).
- **The reference run reproduces.** eta = inf at k_c 23 gives Delta = 0.45986545522 against the Mac's 0.4598654552 (`data/sigdss_log_d4eta_kc23_aborted.txt`): the difference, 2.2e-11, is below the digits the Mac's log prints. This is the same code on another machine and BLAS, not an independent method.
- **Convergence in k_c.** Delta(inf) moves by -1.560e-4 from k_c 15 to 23 and by -4.35e-6 from 23 to 39, and the constraint falls from 1.18e-1 to 1.53e-2 to 2.01e-4, so k_c 39 is well resolved by the code's own measures. This is the code's constraint, not an independent error estimate.
- **Not run:** an independent implementation of the sigma-model solver, and any k_c above 39.

## Beyond the rule (not part of the acceptance)

- Delta(10) - Delta(inf) is also negative at all three resolutions (-5.813e-5, -4.744e-5, -4.692e-5), and Delta(2) - Delta(inf) is positive (+2.553e-4, +3.053e-4, +3.075e-4). So at k_c 23 and 39 the order is Delta(10) < Delta(5) < Delta(inf) < Delta(2), a minimum of Delta(eta) near eta = 10 and not a monotone approach to Delta(inf).
- The order of Delta(5) and Delta(10) changes between k_c 15 and the higher resolutions: Delta(5) - Delta(10) is -7.253e-6 at k_c 15 and +3.173e-6, +3.657e-6 at k_c 23 and 39. At k_c 15 Delta(5) is the lowest of the eta computed, at k_c 23 and 39 Delta(10) is.
- The issue's "What" lists eta = 20, which these commands do not include: the k_c 15 file has no point at eps = 0.05 (its eps values are 0, 0.1, 0.2, 0.425, 0.5, 1.0, ...). Not run.

## Discrepancies

None with the text. The answer to the issue's question, that Delta(eta) is not monotone toward its eta = inf value, disagrees with the review's wording (notes/REVIEW_GHMG25.md section 6, R5, "decreases monotonically toward its eta = inf value") if that means approach from above: Delta(5) and Delta(10) lie below Delta(inf) at every resolution. Whether it contradicts the review is for the coordinator.

## Recommended tasks (for the coordinator)

1. **Locate the minimum of Delta(eta) at k_c 23 and 39 with eta = 20 added.** What: a continuation from the eps = 0.1 point to eps = 0.05 (`sigdss_run.py cont`, target 0.05 and one or two more such as 0.0667) at k_c 15, then refine to k_c 23 (about 11 min each) and 39 (about 58 min each) as here. Why: the issue names eta = 20, and the minimum near eta = 10 is not located, only bracketed by 5, 10 and inf. Acceptance: eta = 20 converges at both k_c with F < 1e-10, and the smallest Delta among eta = 5, 10, 20 is the same eta at both k_c. Depends on #623.
