# I633-win: the sigma-model's Delta at eta = 6 and 8.5, D = 4, k_c 23 and 39 (narrowing the minimum of Delta(eta))

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/633 (the coordinator's message `choptuik-large-d/2026-11-13/031223Z-coordinator-cd2b.md`; follows #631, raw `I631-win/` at 2d659f74, #630 `I630-win/` at 9c2cac04 and #623 `I623-win/` at 9985be57). Worktree `choptuik-i623` (reused, main ef1df85e, `solver/matter`; the new tags `i633a`, `i633b` collide with none of the earlier files), venv-t151 (Python 3.10, numpy 2.2.6, scipy 1.15.3). Pure Python, no hp kernel.

## Plan, written before the runs (the issue's acceptance)

- `run_633.py` (BelowNormal, `OPENBLAS_NUM_THREADS=1`, one thread per process, at most 4 busy) runs, from `solver/matter`, the two continuations at once and each one's two refines as soon as it has landed:
  1. `python -u sigdss_run.py cont i633a data/sigdss_sol_i623seed_D4.0000_eta5.0000.npy --par eps --start 0.2 --end 0.166666666667 --targets 0.166666666667 --D 4 --kc 15 --kappa 0.5` (eta = 6 from the eta = 5 seed);
  2. `python -u sigdss_run.py cont i633b data/sigdss_sol_i631a_D4.0000_eta7.0000.npy --par eps --start 0.142857142857 --end 0.117647058824 --targets 0.117647058824 --D 4 --kc 15 --kappa 0.5` (eta = 8.5 from #631's eta = 7 solution);
  3. `python -u sigdss_run.py refine data/sigdss_sol_i633{a,b}_D4.0000_eta{6.0000,8.5000}.npy --D 4 --eps {0.166666666667,0.117647058824} --kc_seed 15 --kc {23,39} --kappa 0.5 --tag i633_kc{23,39}_eta{6,8.5}`.
  Logs go to `logs/`; the records `data/sigdss_i633{a,b}.jsonl`, `data/sigdss_refine_i633_*.jsonl` and the states `data/sigdss_sol_*i633*.npy` are copied here from the worktree.
- Pass: both continuations land on their target eps with their F in the record, and all four refines converge (F below 1e-10 in the record).
- Table of Delta at eta = 5, 6, 7, 8.5, 10 for k_c 23 and 39 (the others, 14, 20 and inf, beside it), eta = 5, 10, inf from `../I623-win`, 7 and 14 from `../I631-win`, 20 from `../I630-win`.
- The bracket, by #623's rule as #631 fixed it, now on the ordered eta 5, 6, 7, 8.5, 10, 14, 20, inf: s_i = Delta(next) - Delta(eta_i) for each neighbouring pair is **resolved** when it has the same sign at k_c 23 and 39 and its magnitude at both exceeds its change c = |s_39 - s_23|, otherwise **open**; the minimum is **bracketed** between eta_{i-1} and eta_{i+1} when s_{i-1} < 0 and s_i > 0 are both resolved.
- The parabola, defined here before the data: at each k_c the three grid points with the smallest Delta among eta = 5, 6, 7, 8.5, 10 (they must be neighbours in eta; if they are not, that is reported and the three adjacent points around the smallest are used), Delta = a + b eta + c eta^2 through them, eta_min = -b/(2c) and Delta_min = a - b^2/(4c); eta_min must lie inside the span of the three points, otherwise it is flagged as an extrapolation. The change of eta_min and Delta_min between k_c 23 and 39 is reported as an estimate of the truncation, not a bound. As a sensitivity check outside the definition the same parabola is fitted in ln eta and in eps = 1/eta, and the spread of eta_min over the three variables is reported at each k_c.
- Checks: `table_633.py --selftest` (planted tables with a known bracket, and planted parabolas with a known vertex, including one whose vertex lies outside the span) and `--shift` mutations, as in #631.

## Summary

Both continuations land (F 2.79e-15 and 2.48e-15 in their records) and all four refines converge (F 1.4e-15 and 1.6e-15 at k_c 23, 2.9e-12 at k_c 39 in the records). **The bracket of the minimum narrows from (5, 10) to (6, 8.5), with Delta(7) the smallest at both k_c**: Delta falls into eta = 7 (s(6,7) = -1.317e-6, -1.432e-6) and rises out of it (s(7,8.5) = +1.821e-6, +1.697e-6), and every neighbouring difference is resolved by #623's rule.

| pair (a, b), s = Delta(b) - Delta(a) | k_c 23 | k_c 39 | change c | smaller magnitude / c | status |
|---|---|---|---|---|---|
| (5, 6) | -6.890e-6 | -7.047e-6 | 1.572e-7 | 44 | resolved, fall |
| (6, 7) | -1.317e-6 | -1.432e-6 | 1.149e-7 | 11 | resolved, fall |
| (7, 8.5) | +1.821e-6 | +1.697e-6 | 1.240e-7 | 14 | resolved, rise |
| (8.5, 10) | +3.213e-6 | +3.125e-6 | 8.830e-8 | 35 | resolved, rise |
| (10, 14) | +8.535e-6 | +8.389e-6 | 1.455e-7 | 58 | resolved, rise |
| (14, 20) | +9.065e-6 | +8.954e-6 | 1.112e-7 | 80 | resolved, rise |
| (20, inf) | +2.984e-5 | +2.957e-5 | 2.665e-7 | 111 | resolved, rise |

At both k_c the order is Delta(7) < Delta(6) < Delta(8.5) < Delta(10) < Delta(5) < Delta(14) < Delta(20) < Delta(inf).

**The parabola** through eta = 6, 7, 8.5 (the three smallest, neighbours in eta, at both k_c), in eta as defined in the plan:

| | k_c 23 | k_c 39 | change |
|---|---|---|---|
| eta_min | 7.1504 | 7.1983 | +0.0479 |
| Delta_min | 0.4598129584 | 0.4598093233 | -3.635e-6 |

Both vertices lie inside the span of the three points. The change between k_c 23 and 39 is an estimate of the truncation, not a bound. **The choice of the variable matters more than the k_c does**: in ln eta the vertex is at 7.0417 and 7.0891, in eps = 1/eta at 6.9380 and 6.9834, so the spread of eta_min over the three variables is 0.212 (k_c 23) and 0.215 (k_c 39), four times the change over k_c. A parabola through three points that span 6 to 8.5 gives eta_min = 7.0 to 7.2 and nothing finer; Delta_min is 2.3e-8 (k_c 23) and 4.0e-8 (k_c 39) below Delta(7), and its dependence on the variable is 2.1e-8 (k_c 23) and 4.0e-8 (k_c 39).

## What ran

`run_633.py` (logs/run_633.log), BelowNormal, one thread per process (`OPENBLAS_NUM_THREADS=1`), at most 4 busy threads, venv-t151 (Python 3.10, numpy 2.2.6, scipy 1.15.3), worktree `choptuik-i623` at main ef1df85e:

| run | start (UTC) | end | wall |
|---|---|---|---|
| continuation eta 6 (from eta 5), k_c 15 | 2026-11-13 03:13:36 | 03:15:26 | 110 s |
| continuation eta 8.5 (from #631's eta 7), k_c 15 | 03:13:36 | 03:15:26 | 110 s |
| refines k_c 23, eta 6 and 8.5 | 03:15:26 | 03:26:52 | 686 s each |
| refine k_c 39, eta 8.5 | 03:15:26 | 04:08:26 | 3180 s |
| refine k_c 39, eta 6 | 03:15:26 | 04:08:36 | 3190 s |

The two continuations landed on their targets (`data/sigdss_i633a.jsonl`, `data/sigdss_i633b.jsonl`: `target` true). The eta = 5, 10, inf rows are #623's (`../I623-win`), 7 and 14 are #631's, 20 is #630's, read by `table_633.py` from their records.

## Results (`table_633.txt`)

| eta | k_c | N | Delta | F | constraint |
|---|---|---|---|---|---|
| 5 | 15 | 48 | 0.4599560915 | 1.99e-14 | 9.6252e-02 |
| 5 | 23 | 72 | 0.4598211881 | 1.67e-15 | 1.2754e-02 |
| 5 | 39 | 120 | 0.4598178425 | 2.44e-12 | 1.5065e-04 |
| 6 | 15 | 48 | 0.4599526402 | 2.79e-15 | 9.9847e-02 |
| 6 | 23 | 72 | 0.4598142980 | 1.39e-15 | 1.3195e-02 |
| 6 | 39 | 120 | 0.4598107952 | 2.89e-12 | 1.5861e-04 |
| 7 | 15 | 48 | 0.4599538031 | 2.02e-14 | 1.0241e-01 |
| 7 | 23 | 72 | 0.4598129813 | 1.46e-15 | 1.3507e-02 |
| 7 | 39 | 120 | 0.4598093636 | 2.88e-12 | 1.6442e-04 |
| 8.5 | 15 | 48 | 0.4599582688 | 2.48e-15 | 1.0512e-01 |
| 8.5 | 23 | 72 | 0.4598148020 | 1.59e-15 | 1.3835e-02 |
| 8.5 | 39 | 120 | 0.4598110603 | 2.90e-12 | 1.7069e-04 |
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

continuations present: 2 of 2 (target landed: [True, True], F ['2.79e-15', '2.48e-15']); new refines present and converged (F < 1e-10): True

| neighbouring pair s = Delta(next) - Delta(first) | s at k_c 23 | s at k_c 39 | change c | status |
|---|---|---|---|---|
| (5, 6) | -6.890e-06 | -7.047e-06 | 1.572e-07 | RESOLVED fall |
| (6, 7) | -1.317e-06 | -1.432e-06 | 1.149e-07 | RESOLVED fall |
| (7, 8.5) | +1.821e-06 | +1.697e-06 | 1.240e-07 | RESOLVED rise |
| (8.5, 10) | +3.213e-06 | +3.125e-06 | 8.830e-08 | RESOLVED rise |
| (10, 14) | +8.535e-06 | +8.389e-06 | 1.455e-07 | RESOLVED rise |
| (14, 20) | +9.065e-06 | +8.954e-06 | 1.112e-07 | RESOLVED rise |
| (20, inf) | +2.984e-05 | +2.957e-05 | 2.665e-07 | RESOLVED rise |

eta of the smallest Delta: k_c 23 7, k_c 39 7
BRACKET: the minimum lies between eta = 6 and eta = 8.5 (Delta falls into eta = 7 and rises out of it, both resolved)
order of Delta at k_c 23 (low to high): Delta(7) < Delta(6) < Delta(8.5) < Delta(10) < Delta(5) < Delta(14) < Delta(20) < Delta(inf)
order of Delta at k_c 39 (low to high): Delta(7) < Delta(6) < Delta(8.5) < Delta(10) < Delta(5) < Delta(14) < Delta(20) < Delta(inf)

parabola through the three smallest of eta = 5, 6, 7, 8.5, 10 (primary variable eta):
| variable | k_c | points used | adjacent | eta_min | Delta_min | vertex inside span |
|---|---|---|---|---|---|---|
| eta | 23 | 6,7,8.5 | True | 7.1504 | 0.4598129584 | True |
| eta | 39 | 6,7,8.5 | True | 7.1983 | 0.4598093233 | True |
| ln eta | 23 | 6,7,8.5 | True | 7.0417 | 0.4598129795 | True |
| ln eta | 39 | 6,7,8.5 | True | 7.0891 | 0.4598093553 | True |
| eps = 1/eta | 23 | 6,7,8.5 | True | 6.9380 | 0.4598129770 | True |
| eps = 1/eta | 39 | 6,7,8.5 | True | 6.9834 | 0.4598093633 | True |

primary (eta): eta_min 7.1504 (k_c 23), 7.1983 (k_c 39), change +0.0479; Delta_min 0.4598129584, 0.4598093233, change -3.635e-06
spread of eta_min over the three variables at k_c 23: 6.9380 to 7.1504 (width 0.2124)
spread of eta_min over the three variables at k_c 39: 6.9834 to 7.1983 (width 0.2149)

The k_c 39 records' F (2.9e-12 at both new eta) is that of `refine`'s second pass, after the Runge-Kutta step counts are re-frozen; the first pass reached 3.2e-15 and 3.1e-15 (`logs/kc39_eta*.log`). The constraint falls by a factor of 83 (eta 6) and 81 (eta 8.5) from k_c 23 to 39.

## Controls

- **The bracket can fail.** `table_633.py --selftest` runs the bracket rule and the parabola on six planted cases (a clear minimum, a sign flip that must remove the bracket, exact parabolas in eta and in ln eta with known vertices, a vertex outside the span that must be flagged, and three smallest points that are not neighbours), all as expected; the ln eta case shows that the variable moves the vertex by 0.1 when the data are exact in the other variable. On the real data, adding +1e-6 to Delta(7) at k_c 39 (`--shift 7 1e-6`, `table_633_shift_eta7_plus1e-6.txt`) leaves (6,7) and (7,8.5) open and removes the bracket, and adding +1e-5 to Delta(6) (`table_633_shift_eta6_plus1e-5.txt`) changes the three smallest points to 7, 8.5, 10 and the vertex to 5.97, which the table flags as outside their span.
- **Convergence in k_c.** Delta(6) moves by -1.383e-4 and Delta(8.5) by -1.435e-4 from k_c 15 to 23, and by -3.50e-6 and -3.74e-6 from 23 to 39, in line with the other eta (#623, #630, #631). These are the code's own measures; no independent solver was run.
- **Not run:** any k_c above 39, an independent solver, and the parabola with more than three points (a fit over five points would add a model choice that the plan did not fix).

## Discrepancies

None with the text. The parabola's eta_min of 7.15 and 7.20 at k_c 23 and 39 lies at the grid point eta = 7 within 0.2, and Delta(7) is already within 4.0e-8 of the parabola's minimum at both k_c.

## Recommended tasks (for the coordinator)

None needed for the question. If a tighter location is wanted, eta = 6.5 and 7.5 would test the parabola's vertex directly (about 1.1 h on 4 threads), but the minimum is already known to within about 0.3 in eta (the parabola's vertex over its three variables and both k_c, 6.94 to 7.20), and its depth below Delta(7) is 2e-8 to 4e-8, about two orders of magnitude below the k_c 23 to 39 change of any Delta (3.3e-6 to 4.4e-6).
