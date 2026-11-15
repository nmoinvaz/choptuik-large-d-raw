# I810-mac: the l = 1 table's k_c truncation at D = 7, 8, 9 (k_c 23 against 31 and 39), and the psi-constraint

Machine: the coordinator's Mac (Apple M5), agent xfkappa, one process at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/810
Code: `solver/matter/ell_refine.py` and `dss_ell.py` of choptuik-large-d, branch wip/xf-810. Sources: the table's
states `solver/matter/data/sol_l1_kc23r_D{7,8,9}.0000.npy` and their records `data/l1_kc23r.jsonl`; #660's D = 10
rerun state `I660-mac/out/sol_l1kc23hi660_D10.0000.npy`. The scripts write into the worktree's `solver/matter/data/`;
the files are copied here and not committed to choptuik-large-d.

| file | what |
|---|---|
| `queue1.sh`, `queue1.log`, `out/l1kc{23,31,39}s810.jsonl` and states | `ell_refine.py` from the table's k_c 23 states at D = 7, 8, 9 (kappa 0.7, u0 0.04, Ks 30, tol 1e-13): k_c 23 -> 23, 31, 39 |
| `dirs.log` | `ell_constraint_dirs.py` on #660's D = 10 rerun state (k_c 23): the psi-constraint along the Jacobian's four weakest directions and the strongest (the control), straight moves (test 1) and Newton re-converged (test 2, `--resolve`) |
| `queue2.sh`, `queue2.log` (truncated, see its note), `out/l1kc{23,31,39}d{4,5}s810.jsonl` and states | the extension to D = 4 and 5, each row's own settings (kappa 0.5, u0 0.01, Ks 16, tol 1e-13): D = 5 from the row's state at k_c 23, 31, 39; D = 4 lambda from the stored k_c 23, 31, 39 states |

## Results

Changes of Delta and lambda with k_c from each row's state (tol 1e-13; bars 1e-6 and 3e-6 on the change from the row's
k_c to the next, falling at the one after; D = 6 from ELL.md's own check, D = 10 from #660):

| D | row's k_c | Delta | 23 -> 31 | 31 -> 39 | lambda | 23 -> 31 | 31 -> 39 | psi-constraint 23 / 31 / 39 | verdict |
|---|---|---|---|---|---|---|---|---|---|
| 4 | Delta 39, lambda 23 | 0.459861102 | -4.26e-6 | -9.8e-8 | 8.410420009 | **-2.55e-4** | -6.5e-6 | 1.5e-2 / 1.7e-3 / 2.0e-4 | Delta converged; **lambda not** (k_c 39: 8.410158049) |
| 5 | 23 | 0.7833438998 | -9.0e-9 | +6.8e-10 | 4.640173544 | -5.5e-7 | -5.5e-9 | 3.2e-4 / 1.5e-5 / 6.8e-7 | both converged |
| 6 | 23 | 0.9115280871 | +6.8e-8 | - | 3.765554784 | -2.6e-7 | - | 1.7e-5 / 2.9e-7 / - | both within the bar (k_c 39 not run) |
| 7 | 23 | 0.9639878012 | +1.68e-7 | +4.5e-8 | 3.381429353 | -5.6e-7 | -1.5e-7 | 2.1e-5 / 1.4e-7 / 4.3e-8 | both converged |
| 8 | 23 | 0.9837904662 | +3.56e-7 | +9.7e-8 | 3.162528663 | -8.4e-7 | -2.3e-7 | 2.2e-6 / 2.2e-7 / 8.7e-8 | both converged |
| 9 | 23 | 0.9882045993 | -5.73e-7 | -1.50e-7 | 3.018537415 | +2.57e-6 | +6.7e-7 | 2.4e-6 / 3.0e-7 / 1.2e-7 | both converged (lambda at 0.86 of its bar) |
| 10 (#660, not in the table) | 23 | 0.9849793417 | -2.65e-6 | -7.0e-7 | 2.914965959 | -1.34e-5 | -3.5e-6 | 8.2e-5 / 1.6e-6 / 2.4e-7 | not converged |

Re-solves at the row's own k_c reproduce the stored rows: Delta within 3e-13, lambda within 5e-9, and the
psi-constraint to 5 digits or better. |dDelta/dF| is 59, 357, 1.7e4, 8.2e4, 3.8e5 at D = 4, 5, 7, 8, 9 (1.4e6 at D = 10).
Settings: the D = 4 and 5 rows were solved with kappa 0.5, u0 0.01, Ks 16, not the kappa 0.7, u0 0.04, Ks 30 that
ELL.md states for the table (the residual of each stored state matches only under its own settings).

The psi-constraint, stored against rerun. (a) The table's states give back their stored constraint (recomputed from the state: exactly; after a re-solve: to 5
digits or better). (b) #660's
march: on its D = 10 rerun state (k_c 23) the Jacobian has four near-null directions (singular values 2.4e-12 twice,
1.4e-11 twice, against 5.5). Test 1, straight moves along them that change the constraint by 1e-5, raised |F| to
4e-10 to 2e-8 and failed its criterion. Test 2, the same moves followed by Newton (tol 1e-13), lands at states with
|F| about 6e-14, 3e-4 to 3e-3 from the start, with the constraint moved by 1.0e-5 to 3.1e-5 and Delta by under 7e-10.
The control, the strongest direction, returns to the start (7e-11 away, constraint within 1.5e-11). So the converged
states at k_c 23 near D = 10 form a family along those directions. The equations fix Delta to about 1e-9 across it but
not the constraint, and the stored and rerun marches converged to different members of it.
