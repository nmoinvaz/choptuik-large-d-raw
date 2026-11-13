# I631-win: the sigma-model's Delta at eta = 7 and 14, D = 4, k_c 23 and 39 (where is the minimum of Delta(eta)?)

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/631 (the coordinator's message `choptuik-large-d/2026-11-13/020958Z-coordinator-76ac.md`; follows #630, raw `I630-win/` at 9c2cac04, and #623, `I623-win/` at 9985be57). Worktree `choptuik-i623` (reused, main ef1df85e, `solver/matter`; the new tags `i631a`, `i631b` collide with none of the earlier files), venv-t151 (Python 3.10, numpy 2.2.6, scipy 1.15.3). Pure Python, no hp kernel.

## Plan, written before the runs (the issue's acceptance)

- `run_631.py` (BelowNormal, `OPENBLAS_NUM_THREADS=1`, one thread per process, at most 4 busy) runs, from `solver/matter`, the two continuations at once and each one's two refines as soon as it has landed:
  1. `python -u sigdss_run.py cont i631a data/sigdss_sol_i623seed_D4.0000_eta5.0000.npy --par eps --start 0.2 --end 0.142857142857 --targets 0.142857142857 --D 4 --kc 15 --kappa 0.5` (eta = 7 from the eta = 5 seed);
  2. `python -u sigdss_run.py cont i631b data/sigdss_sol_i623seed_D4.0000_eta10.0000.npy --par eps --start 0.1 --end 0.0714285714286 --targets 0.0714285714286 --D 4 --kc 15 --kappa 0.5` (eta = 14 from the eta = 10 seed);
  3. `python -u sigdss_run.py refine data/sigdss_sol_i631{a,b}_D4.0000_eta{7,14}.0000.npy --D 4 --eps {0.142857142857,0.0714285714286} --kc_seed 15 --kc {23,39} --kappa 0.5 --tag i631_kc{23,39}_eta{7,14}`.
  Logs go to `logs/`; the records `data/sigdss_i631{a,b}.jsonl`, `data/sigdss_refine_i631_*.jsonl` and the states `data/sigdss_sol_*i631*.npy` are copied here from the worktree.
- Pass: both continuations land on their target eps with their F in the record, and all four refines converge (F below 1e-10 in the record).
- Table of Delta at eta = 5, 7, 10, 14, 20 and inf for k_c 23 and 39 (eta = 5, 10, inf from `../I623-win`, eta = 20 from `../I630-win`).
- The bracket of the minimum, by #623's rule applied to the neighbouring differences, written here before the data are read. Order the eta increasingly, 5, 7, 10, 14, 20, inf, and let s_i = Delta(next eta) - Delta(eta_i) for each neighbouring pair, at k_c 23 and 39. A difference s is **resolved** when it has the same sign at both k_c and its magnitude at both exceeds its change between them, c = |s_39 - s_23|; otherwise **open**. The minimum is **bracketed** between eta_{i-1} and eta_{i+1} when s_{i-1} < 0 and s_i > 0 are both resolved (Delta falls into eta_i and rises out of it). If no eta_i has both resolved, the summary names the open differences and the bracket is the widest interval that the resolved ones allow. The eta of the smallest Delta at each k_c is reported too.
- Checks: `table_631.py --selftest` (planted tables with a known bracket and one that must stay open) and a `--shift` mutation of one Delta at k_c 39, as in #623 and #630.

## Summary

Both continuations land and all four refines converge (F below 1e-10). **The minimum of Delta(eta) is bracketed between eta = 5 and eta = 10, at eta = 7**: Delta(7) is the smallest of the six values at k_c 23 and at k_c 39, Delta falls into eta = 7 (s(5,7) = -8.2e-6, -8.5e-6) and rises out of it (s(7,10) = +5.0e-6, +4.8e-6), and every neighbouring difference is resolved by #623's rule, with magnitudes 23 to 112 times their change between the two k_c.

| pair (a, b), s = Delta(b) - Delta(a) | k_c 23 | k_c 39 | change c | smaller magnitude / c |
|---|---|---|---|---|
| (5, 7) | -8.207e-6 | -8.479e-6 | 2.720e-7 | 30 |
| (7, 10) | +5.034e-6 | +4.822e-6 | 2.123e-7 | 23 |
| (10, 14) | +8.535e-6 | +8.389e-6 | 1.455e-7 | 58 |
| (14, 20) | +9.065e-6 | +8.954e-6 | 1.112e-7 | 80 |
| (20, inf) | +2.984e-5 | +2.957e-5 | 2.665e-7 | 111 |

At both k_c the order is Delta(7) < Delta(10) < Delta(5) < Delta(14) < Delta(20) < Delta(inf). At k_c 15 it is Delta(7) < Delta(5) < Delta(10) < Delta(14) < Delta(20) < Delta(inf), so the minimum is at eta = 7 there too, and the swap of Delta(5) and Delta(10) between k_c 15 and the higher k_c (#623) is a small shift of the minimum, which lies between 5 and 10, and not a change of shape. The bracket is the resolution of the grid, (5, 10); it is not a located minimum (no run between 5 and 7 or 7 and 10).

## What ran

`run_631.py` (logs/run_631.log), BelowNormal, one thread per process (`OPENBLAS_NUM_THREADS=1`), at most 4 busy threads, venv-t151 (Python 3.10, numpy 2.2.6, scipy 1.15.3), worktree `choptuik-i623` at main ef1df85e:

| run | start (UTC) | end | wall |
|---|---|---|---|
| continuation eta 7 (from eta 5), k_c 15 | 2026-11-13 02:11:26 | 02:13:21 | 115 s |
| continuation eta 14 (from eta 10), k_c 15 | 02:11:26 | 02:13:26 | 120 s |
| refine eta 7, k_c 23 | 02:13:21 | 02:24:58 | 696 s |
| refine eta 14, k_c 23 | 02:13:26 | 02:24:58 | 691 s |
| refine eta 7, k_c 39 | 02:13:21 | 03:09:12 | 3350 s |
| refine eta 14, k_c 39 | 02:13:26 | 03:09:12 | 3345 s |

The two continuations landed on their targets (`data/sigdss_i631a.jsonl`, `data/sigdss_i631b.jsonl`: `target` true, F 2.02e-14 and 2.63e-15). The eta = 5, 10, inf rows are #623's (`../I623-win`), eta = 20 is #630's (`../I630-win`), read by `table_631.py` from their records.

## Results (`table_631.txt`)

| eta | k_c | N | Delta | F | constraint |
|---|---|---|---|---|---|
| 5 | 15 | 48 | 0.4599560915 | 1.99e-14 | 9.6252e-02 |
| 5 | 23 | 72 | 0.4598211881 | 1.67e-15 | 1.2754e-02 |
| 5 | 39 | 120 | 0.4598178425 | 2.44e-12 | 1.5065e-04 |
| 7 | 15 | 48 | 0.4599538031 | 2.02e-14 | 1.0241e-01 |
| 7 | 23 | 72 | 0.4598129813 | 1.46e-15 | 1.3507e-02 |
| 7 | 39 | 120 | 0.4598093636 | 2.88e-12 | 1.6442e-04 |
| 10 | 15 | 48 | 0.4599633445 | 6.27e-11 | 1.0702e-01 |
| 10 | 23 | 72 | 0.4598180153 | 1.55e-15 | 1.4062e-02 |
| 10 | 39 | 120 | 0.4598141853 | 3.32e-12 | 1.7514e-04 |
| 14 | 15 | 48 | 0.4599749118 | 2.63e-15 | 1.1007e-01 |
| 14 | 23 | 72 | 0.4598265501 | 1.62e-15 | 1.4425e-02 |
| 14 | 39 | 120 | 0.4598225746 | 2.85e-12 | 1.8243e-04 |
| 20 | 15 | 48 | 0.4599862635 | 6.97e-15 | 1.1235e-01 |
| 20 | 23 | 72 | 0.4598356152 | 1.54e-15 | 1.4694e-02 |
| 20 | 39 | 120 | 0.4598315284 | 3.33e-12 | 1.8798e-04 |
| inf | 15 | 48 | 0.4600214704 | 5.88e-12 | 1.1761e-01 |
| inf | 23 | 72 | 0.4598654552 | 1.61e-15 | 1.5305e-02 |
| inf | 39 | 120 | 0.4598611019 | 3.67e-12 | 2.0111e-04 |

continuations present: 2 of 2 (target landed: [True, True], F ['2.02e-14', '2.63e-15']); new refines present and converged (F < 1e-10): True

| neighbouring pair s = Delta(next) - Delta(first) | s at k_c 23 | s at k_c 39 | change c | status |
|---|---|---|---|---|
| (5, 7) | -8.207e-06 | -8.479e-06 | 2.720e-07 | RESOLVED fall |
| (7, 10) | +5.034e-06 | +4.822e-06 | 2.123e-07 | RESOLVED rise |
| (10, 14) | +8.535e-06 | +8.389e-06 | 1.455e-07 | RESOLVED rise |
| (14, 20) | +9.065e-06 | +8.954e-06 | 1.112e-07 | RESOLVED rise |
| (20, inf) | +2.984e-05 | +2.957e-05 | 2.665e-07 | RESOLVED rise |

eta of the smallest Delta: k_c 23 7, k_c 39 7
BRACKET: the minimum lies between eta = 5 and eta = 10 (Delta falls into eta = 7 and rises out of it, both resolved)
order of Delta at k_c 23 (low to high): Delta(7) < Delta(10) < Delta(5) < Delta(14) < Delta(20) < Delta(inf)
order of Delta at k_c 39 (low to high): Delta(7) < Delta(10) < Delta(5) < Delta(14) < Delta(20) < Delta(inf)

The k_c 39 records' F (2.9e-12 at both new eta) is that of `refine`'s second pass, after the Runge-Kutta step counts are re-frozen; the first pass reached 3.0e-15 and 3.3e-15 (`logs/kc39_eta*.log`). The constraint falls by a factor of 82 (eta 7) and 79 (eta 14) from k_c 23 to 39.

## Controls

- **The bracket can fail.** `table_631.py --selftest` runs the rule on four planted tables (a clear minimum at 10, two where the neighbouring differences are not separated or change sign between the resolutions, and a monotone rise), all as expected. On the real data, adding +1e-5 to Delta(7) at k_c 39 (`--shift 7 1e-5`, `table_631_shift_eta7_plus1e-5.txt`) removes the bracket: s(5,7) and s(7,10) both become OPEN and the smallest Delta at k_c 39 moves to eta = 10. The rule brackets a local minimum, so shifting Delta(14) by -2e-5 at k_c 39 leaves the bracket (5, 10) and moves only the line "eta of the smallest Delta" to 14; the real data have one minimum.
- **Convergence in k_c.** Delta(7) moves by -1.41e-4 and Delta(14) by -1.48e-4 from k_c 15 to 23, and by -3.62e-6 and -3.98e-6 from 23 to 39, in line with eta = 5, 10, 20 and inf (#623, #630). These are the code's own measures; no independent solver was run.
- **Not run:** any k_c above 39, an independent solver, and any eta between 5 and 10 other than 7.

## Discrepancies

None with the text. The k_c 15 table in matter/SIGMA_DSS.md has Delta(5) below Delta(10); with eta = 7 added, k_c 15 has its minimum at eta = 7 too, so that table is consistent with a minimum between 5 and 10.

## Recommended tasks (for the coordinator)

1. **Narrow the bracket to (6, 8.5) or locate the minimum to a few percent.** What: eta = 6 and 8.5 (eps 0.1666667 and 0.1176471) from the eta = 5 and 10 seeds, the continuations and refines as here (about 1.1 h on 4 threads). Why: the minimum is at the 5, 10 resolution of the grid, and Delta differences between neighbouring eta are 5e-6 to 9e-6, 20 to 80 times the resolution change, so a finer grid is resolvable. Acceptance: all runs converge with F below 1e-10; the bracket rule applied to the neighbouring differences names an interval narrower than (5, 10) at both k_c, or the summary says which differences are open. Depends on #631.
