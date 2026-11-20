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
| `l0_validate_D8.71.log` | the l = 0 check: dss_ell at D 8.71 against the stored lambda_0 (scan_ne6, gamma_rust) |
| `lane_de.sh`, `lane_de.log` | lanes D, E: ell_leap --fold at k_c 47 from D 14 (stopped at D 17 with its step at the 1/64 floor, set by rounding-floor singular values), and lambda at k_c 47 on its half-integer states |
| `leap_kc47_fold.log`, `out/l1kc47F1025.jsonl`, `out/sol_l1kc47F1025_D*.npy` | the k_c 47 fold run: records with J's singular values, the bordered matrix's and \|J^+ dF/dn\|, and every state |
| `lam_kc47_fold.log`, `out/l1kc47Fr1025.jsonl`, `out/sol_l1kc47Fr1025_D*.npy` | lambda at k_c 47, D 14.5-17.5 |
| `fold_planted.log`, `fold_table_D15.6.log` | ell_delta.py fold: planted D* and its mutation; the real records' table (its sigma is rounding-floor junk, not quoted) |
| `lane_f.sh`, `lane_f.log`, `leap_kc47_fold2.log` | lanes F-H: k_c 47 D 17 -> 17.5 at h 0.125 with the fixed step rule; k_c 55 starts at D 17, 17.5 (`refine_kc55_start.log`, `out/l1kc55Fs1025.jsonl`); the k_c 55 fold run to D 20 (`leap_kc55_fold.log`, `out/l1kc55F1025.jsonl`); k_c 55 at D 14.5-16.5 for the k_c bar (`refine_kc55_bar.log`, `out/l1kc55Fb1025.jsonl`); lambda at k_c 55, D 18-20 (`lam_kc55_fold.log`, `out/l1kc55Fr1025.jsonl`) |
| `steep_planted.log`, `kcneed_planted.log`, `leak_M5.log` | ell_delta.py steep (the k_c test of the steepening) and kcneed (the k_c a lambda error needs), planted and mutated; leak (harmonic leakage at the M = 3 zeros) |
| `eigs_planted.log`, `eigs_check_kc47_D17.5.log`, `eigs_check_eps_kc47_D17.5.log` | ell_eigs.py planted and its mutation; the state checks at k_c 47, D 17.5 (differencing step 1e-7 fails check (a) on roundoff, 1e-6 passes) |
| `lane_i.sh`, `lane_i_stopped.log`, `lane_i2.sh`, `lane_i2.log` | lane I (stopped while waiting; its D 17 and 17.5 eigenvalue jobs moved to winb, I1025-win) and lane I2: lambda at k_c 55 plus ell_eigs at D 18-20 (`out/ell_eigs_1025.jsonl`) |
| `post_D17.5_kc55.log` | the numbers of the D 17.5 correction post |
