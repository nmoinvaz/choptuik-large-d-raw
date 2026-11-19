# I1025-mac: the l = 1 multiplet's DSS solution continued past D 10 (dss_ell), its growth rate at k_c 31-47, and delta = lambda_1 - lambda_0 (logs, records, states)

Machine: Mac (Apple silicon), helper session xfkappa, at most two processes at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025

Code: `solver/matter/ell_march.py`, `ell_refine.py`, `ell_leap.py` (new) and `ell_delta.py` (new) on branch
`wip/ell1-highD` of choptuik-large-d. The scripts write into the worktree's `solver/matter/data/`; the records
(`*.jsonl`) and states (`sol_*.npy`, DSSEll layout, NODES_STD) are copied to `out/` and not committed there.
Settings throughout: l = 1, kappa 0.7, u0 0.04, Ks 30. Seeds: #660's D = 10 states (raw I660-mac/out).

| file | what |
|---|---|
| `march_kc23_D10_12.log`, `out/march_l1kc23m1025.jsonl` | k_c 23 march D 10 -> 12 (seeds) |
| `march_kc23_D12_15.log` | its continuation: leaves the branch past D 13 (psi-constraint to 1.0), stopped |
| `march_kc31_D10_12_stopped.log`, `march_kc31_D10_15.log` | k_c 31 marches: the tangent predictor leaves the branch by D 10.3, stopped |
| `refine_a.sh`, `refine_a.log`, `out/l1kc{31,39,47}r1025.jsonl` | D 10.5-12 at k_c 31, 39, 47 with lambda |
| `leap_kc31_D12_15.log`, `out/l1kc31L1025.jsonl` | ell_leap at k_c 31, D 12 -> 14.25 (stops on the constraint bar 1e-3) |
| `refine_b.sh`, `refine_b.log`, `out/l1kc39L1025.jsonl` | D 12.5-14 at k_c 39 with lambda |
| `lane_c.sh`, `lane_c.log` | lambda at k_c 31 at D 13, 14; D 13.5, 14 at k_c 47; the k_c 47 leap pilot D 14 -> 15 |
| `delta_planted.log`, `delta_calib*.log`, `delta_table_*.log` | ell_delta.py planted (and its mutation), calib (windows and fits on lambda_0), table |
