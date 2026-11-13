# I630-win: the sigma-model's Delta at eta = 20, D = 4, k_c 23 and 39 (is the rise toward eta = inf under way?)

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/630 (the coordinator's message `choptuik-large-d/2026-11-13/011329Z-coordinator-f7af.md`; follows #623, raw `I623-win/` at 9985be57). Worktree `choptuik-i623` (reused, main ef1df85e, `solver/matter`; the new tags `i630` collide with none of #623's files), venv-t151 (Python 3.10, numpy 2.2.6, scipy 1.15.3). Pure Python, no hp kernel.

## Plan, written before the runs (the issue's acceptance)

- `run_630.py` (BelowNormal, `OPENBLAS_NUM_THREADS=1`, one thread per process) runs, from `solver/matter`:
  1. `python -u sigdss_run.py cont i630 data/sigdss_sol_i623seed_D4.0000_eta10.0000.npy --par eps --start 0.1 --end 0.05 --targets 0.05 --D 4 --kc 15 --kappa 0.5` (the seed is #623's eta = 10 row of `data/sigdss_d4eta15.npz`);
  2. when it has landed on eps 0.05, the two refines at once, `python -u sigdss_run.py refine data/sigdss_sol_i630_D4.0000_eta20.0000.npy --D 4 --eps 0.05 --kc_seed 15 --kc {23,39} --kappa 0.5 --tag i630_kc{23,39}_eta20`.
  Logs go to `logs/`, the records `data/sigdss_i630.jsonl` and `data/sigdss_refine_i630_*.jsonl` and the states `data/sigdss_sol_*i630*.npy` are copied here from the worktree.
- Pass: the continuation lands on eps 0.05 and its F is in the record; both refines converge (F below 1e-10 in the record).
- Report, with #623's table values for eta = inf and 10 beside them: d = Delta(20) - Delta(inf) and e = Delta(20) - Delta(10) at k_c 23 and 39, and their changes between the two k_c, c_d = |d_39 - d_23| and c_e = |e_39 - e_23|. By #623's rule, written here before the data are read, the sign of a quantity is **resolved** when it has the same sign at k_c 23 and 39 and its magnitude at both k_c exceeds its change between them (c_d for d, c_e for e); otherwise it is **open**, and the summary says so. Reading, also written before the data: the rise toward eta = inf is under way at eta = 20 if e is resolved and positive (Delta(20) above Delta(10), so Delta has turned upward past its minimum near eta = 10); if e is resolved and negative, Delta(20) is still below Delta(10) and the minimum lies at larger eta; d is reported beside it.
- Checks: `table_630.py --selftest` (planted pairs, some that must stay open) and a `--shift` mutation of Delta(20) at k_c 39, as in #623.

## Summary

The continuation lands on eps 0.05 (F 6.97e-15 in its record) and both refines converge (F 1.54e-15 at k_c 23, 3.33e-12 at k_c 39). By the rule above both quantities are **resolved**, and **the rise toward eta = inf is already under way at eta = 20**.

| quantity | k_c 23 | k_c 39 | change between | magnitude / change |
|---|---|---|---|---|
| d = Delta(20) - Delta(inf) | -2.984e-5 | -2.957e-5 | 2.665e-7 | 112 and 111 |
| e = Delta(20) - Delta(10) | +1.760e-5 | +1.734e-5 | 2.568e-7 | 69 and 68 |

At both k_c the order is Delta(10) < Delta(5) < Delta(20) < Delta(inf): Delta(20) is above Delta(10), so Delta(eta) has turned upward past its lowest computed value at eta = 10, and it is still below Delta(inf) at eta = 20, so it approaches Delta(inf) from below. The minimum lies between eta = 5 and 20. At k_c 15 the order is different, Delta(5) < Delta(10) < Delta(20) < Delta(inf), the same k_c 15 versus higher-k_c change of Delta(5) and Delta(10) that #623 found.

## What ran

`run_630.py` (logs/run_630.log), BelowNormal, one thread per process (`OPENBLAS_NUM_THREADS=1`), venv-t151 (Python 3.10, numpy 2.2.6, scipy 1.15.3), worktree `choptuik-i623` at main ef1df85e:

| run | start (UTC) | end | wall |
|---|---|---|---|
| continuation, k_c 15, eps 0.1 to 0.05 | 2026-11-13 01:14:44 | 01:16:23 | 100 s |
| refine k_c 23, eta 20 | 01:16:23 | 01:26:36 | 612 s |
| refine k_c 39, eta 20 | 01:16:23 | 02:06:15 | 2992 s |

The continuation's one step landed on its target (`data/sigdss_i630.jsonl`: `target` true, eps 0.05, k_c 15, Delta 0.45998626346, F 6.967e-15, constraint 1.1235e-1). The refines started from its state `data/sigdss_sol_i630_D4.0000_eta20.0000.npy`. The eta = inf, 10 and 5 rows are #623's (`../I623-win`), read by `table_630.py` from its records. At most 2 busy threads.

## Results (`table_630.txt`)

continuation record: {'eps': 0.05, 'kc': 15, 'Delta': 0.45998626346043037, 'F': 6.9671316182425344e-15, 'par': 'eps', 'target': True} 

| eta | k_c | N | Delta | F | constraint |
|---|---|---|---|---|---|
| inf | 15 | 48 | 0.4600214704 | 5.88e-12 | 1.1761e-01 |
| inf | 23 | 72 | 0.4598654552 | 1.61e-15 | 1.5305e-02 |
| inf | 39 | 120 | 0.4598611019 | 3.67e-12 | 2.0111e-04 |
| 20.0000 | 15 | 48 | 0.4599862635 | 6.97e-15 | 1.1235e-01 |
| 20.0000 | 23 | 72 | 0.4598356152 | 1.54e-15 | 1.4694e-02 |
| 20.0000 | 39 | 120 | 0.4598315284 | 3.33e-12 | 1.8798e-04 |
| 10.0000 | 15 | 48 | 0.4599633445 | 6.27e-11 | 1.0702e-01 |
| 10.0000 | 23 | 72 | 0.4598180153 | 1.55e-15 | 1.4062e-02 |
| 10.0000 | 39 | 120 | 0.4598141853 | 3.32e-12 | 1.7514e-04 |
| 5.0000 | 15 | 48 | 0.4599560915 | 1.99e-14 | 9.6252e-02 |
| 5.0000 | 23 | 72 | 0.4598211881 | 1.67e-15 | 1.2754e-02 |
| 5.0000 | 39 | 120 | 0.4598178425 | 2.44e-12 | 1.5065e-04 |

both refines present and converged (F < 1e-10): True

| quantity | k_c 15 | k_c 23 | k_c 39 | change |d_39 - d_23| |
|---|---|---|---|---|
| d = Delta(20) - Delta(inf) | -3.521e-05 | -2.984e-05 | -2.957e-05 | 2.665e-07 |
| e = Delta(20) - Delta(10) | +2.292e-05 | +1.760e-05 | +1.734e-05 | 2.568e-07 |

d = Delta(20) - Delta(inf): RESOLVED: same sign -, magnitudes 2.984e-05 and 2.957e-05 both exceed c = 2.665e-07
e = Delta(20) - Delta(10): RESOLVED: same sign +, magnitudes 1.760e-05 and 1.734e-05 both exceed c = 2.568e-07
READING (README): e resolved positive: the rise toward eta = inf is under way at eta = 20 (Delta(20) above Delta(10))
order of Delta at k_c 23 (low to high): Delta(10) < Delta(5) < Delta(20) < Delta(inf)
order of Delta at k_c 39 (low to high): Delta(10) < Delta(5) < Delta(20) < Delta(inf)

The k_c 39 record's F (3.33e-12) is that of `refine`'s second pass, after the Runge-Kutta step counts are re-frozen; the first pass reached 3.5e-15 (`logs/kc39_eta20.log`). Both are far below 1e-10. The constraint falls by a factor of 78 from k_c 23 to 39 at eta = 20 (1.4694e-2 to 1.8798e-4).

## Controls

- **The rule can fail.** `table_630.py --selftest` runs it on six planted pairs (two resolved, four open), all as expected. Adding +1e-4 or +3e-5 to Delta(20) at k_c 39 turns both quantities to OPEN on the real data (`--shift`, `table_630_shift_plus1e-4.txt`: d's signs differ, and |e_23| = 1.76e-5 does not exceed the shifted change c = 9.97e-5).
- **Convergence in k_c.** Delta(20) moves by -1.506e-4 from k_c 15 to 23 and by -4.09e-6 from 23 to 39, in line with eta = inf (-1.560e-4, -4.35e-6) and eta = 10 (-1.453e-4, -3.83e-6) of #623. These are the code's own measures; no independent implementation of the solver was run.
- **Not run:** any k_c above 39, and an independent solver.

## Discrepancies

None with the text. Delta(20) - Delta(inf) is negative, as Delta(5) - Delta(inf) and Delta(10) - Delta(inf) were in #623, so Delta(5), Delta(10) and Delta(20) lie below Delta(inf) and only Delta(2) lies above it: this does not fit a decrease toward Delta(inf) from above (REVIEW_GHMG25.md row 31).

## Recommended tasks (for the coordinator)

1. **Locate the minimum of Delta(eta) between eta = 5 and 20.** What: add eta = 7 and eta = 14 (eps 0.142857 and 0.0714286), each a `cont` from the eta = 10 point to the new eps at k_c 15 (about 100 s) and the two refines (about 10 and 50 min), as here. Why: with eta = 5, 10 and 20 the minimum is bracketed, not located, and Delta(10) is the lowest computed. Acceptance: all runs converge with F below 1e-10; the eta of the smallest Delta among 5, 7, 10, 14, 20 is the same at k_c 23 and 39, or the summary says that it is not. Depends on #630.
