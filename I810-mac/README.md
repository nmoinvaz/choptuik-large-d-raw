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
