# I660-mac: the l = 1 multiplet's k_c 23 march past D = 9 and its D = 10 solution, checked against k_c 31

Machine: the coordinator's Mac (Apple M5), agent xfkappa, one process at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/660
Code: `solver/matter/ell_march.py`, `ell_refine.py` (which records |dDelta/dF| since #660) and `dss_ell.py` of
choptuik-large-d, branch wip/xf-660. Originals: `solver/matter/data/march_l1kc23hi.jsonl`, the D = 10 row of
`data/ell_gamma.jsonl`, `logs/t31_super.log`. The scripts write into the worktree's `solver/matter/data/`; the files
are copied here and not committed to choptuik-large-d.

| file | what |
|---|---|
| `queue1.sh`, `queue1.log` | the k_c 23 march from D = 9 to 10 (t31_super.log's command), then `ell_refine.py` at D = 10: k_c 23 -> 23 and 23 -> 31 |
| `queue2.sh`, `queue2.log` | diagnostics after the bar failed: k_c 23, 31 and 39 re-solved from the same state with tol 1e-13 |
| `out/march_l1kc23hi660.*`, `out/sol_l1kc23hi660_D10.0000.npy` | the reproduced march and its D = 10 state |
| `out/l1kc23r660.jsonl`, `out/l1kc31r660.jsonl` | the refines of queue 1 (Delta, F, psi-constraint, dDelta_dF, lambda) and their states |
| `out/l1kc23t660.jsonl`, `out/l1kc31t660.jsonl`, `out/l1kc39t660.jsonl` | the refines of queue 2 and their states |

## Bars (posted on the issue before the run) and results

Reproduction: Delta_23(10) = 0.9849793400857 against the stored 0.9849793397201 (3.7e-10, bar 1e-9: PASS), |F| 1.7e-13;
lambda_23 = 2.9149659647 against 2.9149659546 (1.0e-8, bar 1e-7: PASS). The march's Delta agrees with the stored march
to 3e-9 at every point from D 9.05 to 10, with the same steps. Its psi-constraint does not: 1.4e-5 stored at D = 10
against 8.2e-5 rerun (equal at D 9.05 and 9.125, up to 6x apart after), so at k_c 23 near D = 10 the constraint follows
run-to-run differences that Delta does not.

Convergence in k_c at D = 10 (bar |Delta_31 - Delta_23| <= 1e-6, |lambda_31 - lambda_23| <= 3e-6, |F_31| <= 1e-10,
|dDelta/dF| |F| <= 1e-7 at both):

| k_c | tol | Delta | lambda | abs(F) | dDelta/dF | dDelta/dF x F | psi-constraint |
|---|---|---|---|---|---|---|---|
| 23 | 1e-11 | 0.9849793400857 | 2.9149659647 | 1.7e-13 | 1.42e6 | 2.3e-7 | 8.2e-5 |
| 31 | 1e-11 | 0.9849768422842 | 2.9149546341 | 4.4e-12 | 1.42e6 | 6.2e-6 | 1.6e-6 |
| 23 | 1e-13 | 0.9849793416667 | 2.9149659590 | 6.0e-14 | 1.42e6 | 8.6e-8 | 8.2e-5 |
| 31 | 1e-13 | 0.9849766910596 | 2.9149526051 | 1.8e-12 | 1.42e6 | 2.6e-6 | 1.6e-6 |
| 39 | 1e-13 | 0.9849759887273 | 2.9149491218 | 2.3e-12 | 1.42e6 | 3.3e-6 | 2.4e-7 |

**The bar fails.** k_c 23 -> 31 moves Delta by -2.5e-6 (tol 1e-11) or -2.65e-6 (tol 1e-13), and lambda by -1.13e-5 or
-1.34e-5. The residual criterion fails at both k_c (2.3e-7 and 6.2e-6). The diagnostics locate the cause in the
truncation, not the residual. The two k_c 31 solves differ by 1.5e-7 in Delta and 2.0e-6 in lambda, far less than the
norm bound |dDelta/dF| |F| (2.6e-6 to 6.2e-6), which is pessimistic here. The changes fall with k_c: 31 -> 39 moves
Delta by -7.0e-7 and lambda by -3.5e-6, about 0.26 of the 23 -> 31 change, and the psi-constraint falls 8.2e-5 ->
1.6e-6 -> 2.4e-7. So the k_c 23 solution at D = 10 is not converged in k_c at the accuracy of ELL.md's table (Delta
~1e-6, lambda ~1e-6 relative), and even k_c 39 against 31 misses the lambda bar (3.5e-6 against 3e-6).
