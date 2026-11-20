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
| `march_kc23_D12_15.log`, `out/march_l1kc23n1025.jsonl` | its continuation: leaves the branch past D 13 (psi-constraint to 1.0), stopped |
| `march_kc31_D10_12_stopped.log`, `march_kc31_D10_15.log`, `out/march_l1kc31m1025.jsonl` | k_c 31 marches: the tangent predictor leaves the branch by D 10.3, stopped |
| `refine_a.sh`, `refine_a.log`, `out/l1kc{31,39,47}r1025.jsonl` | D 10.5-12 at k_c 31, 39, 47 with lambda |
| `leap_kc31_D12_15.log`, `out/l1kc31L1025.jsonl` | ell_leap at k_c 31, D 12 -> 14.25 (stops on the constraint bar 1e-3) |
| `refine_b.sh`, `refine_b.log`, `out/l1kc39L1025.jsonl` | D 12.5-14 at k_c 39 with lambda |
| `lane_c.sh`, `lane_c.log`, `out/l1kc31Lr1025.jsonl`, `out/l1kc47L1025.jsonl` | lambda at k_c 31 at D 13, 14; D 13.5, 14 at k_c 47; the k_c 47 leap pilot D 14 -> 15 |
| `delta_planted.log`, `delta_calib*.log`, `delta_table_*.log` | ell_delta.py planted (and its mutation), calib (windows and fits on lambda_0), table |
| `l0_validate_D8.71.log` | the l = 0 check: dss_ell at D 8.71 against the stored lambda_0 (scan_ne6, gamma_rust) |
| `lane_de.sh`, `lane_de.log` | lanes D, E: ell_leap --fold at k_c 47 from D 14 (stopped at D 17 with its step at the 1/64 floor, set by rounding-floor singular values), and lambda at k_c 47 on its half-integer states |
| `leap_kc47_fold.log`, `out/l1kc47F1025.jsonl`, `out/sol_l1kc47F1025_D*.npy` | the k_c 47 fold run: records with J's singular values, the bordered matrix's and \|J^+ dF/dn\|, and every state |
| `lam_kc47_fold.log`, `out/l1kc47Fr1025.jsonl`, `out/sol_l1kc47Fr1025_D*.npy` | lambda at k_c 47, D 14.5-17.5 |
| `fold_planted.log`, `fold_table_D15.6.log` | ell_delta.py fold: planted D* and its mutation; the real records' table (its sigma is rounding-floor junk, not quoted) |
| `lane_f.sh`, `lane_f.log`, `leap_kc47_fold2.log` | lanes F-H: k_c 47 D 17 -> 17.5 at h 0.125 with the fixed step rule; k_c 55 starts at D 17, 17.5 (`refine_kc55_start.log`, `out/l1kc55Fs1025.jsonl`); the k_c 55 fold run to D 20 (`leap_kc55_fold.log`, `out/l1kc55F1025.jsonl`); k_c 55 at D 14.5-16.5 for the k_c bar (`refine_kc55_bar.log`, `out/l1kc55Fb1025.jsonl`); lambda at k_c 55, D 18-20 (`lam_kc55_fold.log`, `out/l1kc55Fr1025.jsonl`) |
| `steep_planted.log`, `kcneed_planted.log`, `leak_M5.log` | ell_delta.py steep (the k_c test of the steepening) and kcneed (the k_c a lambda error needs), planted and mutated; leak (harmonic leakage at the M = 3 zeros) |
| `eigs_planted.log`, `eigs_check_kc47_D17.5.log`, `eigs_check_eps_kc47_D17.5.log` | ell_eigs.py planted and its mutation; the state checks at k_c 47, D 17.5 (differencing step 1e-7 fails check (a) on roundoff, 1e-6 passes) |
| `lane_i.sh`, `lane_i_stopped.log`, `lane_i2.sh`, `lane_i2.log` | lane I (stopped while waiting; its D 17 and 17.5 eigenvalue jobs moved to winb, I1025-win) and lane I2: lambda at k_c 55 plus ell_eigs at D 18-20, stopped at 03:20 UTC 2026-11-20 during its D 18 refine (which ran on), since the scans are invalid (`eigs_control.log`) |
| `post_D17_numbers.log`, `post_D17.5_kc55.log` | the numbers of the D 17 post and of the D 17.5 correction post |
| `eigs_control.log`, `mfloor.py`, `mscale.py` | why winb's D 17.5 scans saturated A_0's rank: M's conditioning at k_c 31, D 13 (1e12-1e14 at every lambda, small directions turning with lambda; a fixed equilibration gains about 30x) |
| `eigs_planted_ill_before.log` | ell_eigs.py planted_ill on the code before any fix: fails (rcond 1e-17 cases, and spurious values in an empty circle) |
| `kink_criteria.log` | what separates an avoided crossing from a k_c error at D 16.5 (the steep stretch over D 16.5-17), written before lane J's results |
| `lane_j.sh`, `lane_j.log`, `lane_j_a.log`, `lane_j_b.log` | lane J: lambda at k_c 55 at D 18.5-19.5 (J-a); after the leap, k_c 63 at D 16.5 and k_c 55, 47 at D 16.25, 16.75 (J-b; `out/l1kc63Fb1025.jsonl`, `out/l1kc{47,55}{Fq,Fp}1025.jsonl`) |
| `detscan.py`, `detscan_kc55_D18.log` | sign and log\|det\| of M on 12 real lambda at k_c 55, D 18: every M finite, the sign flips 5 times over 1.77-1.96, so lambda_55(18) = 1.7662 is not established |
| `signtest.py`, `signtest.log` | is sign(det M) resolved? LU(Q M) times sign(det Q) for 3 random orthogonal Q against LU(M); planted control (agrees at a 1e-13 floor, disagrees at 1e-19), then k_c 55 at D 18 (1.80 agrees, 1.84 not) and D 17 (2.00, 2.05 agree) |
| `floormap.py`, `floorblocks.py`, `colnorm.py`, `floormap.log`, `colnorm.log` | where M's floor singular directions sit in the state layout (field, coefficient index), and whether they turn with lambda |
| `lane_j_note.log` | J-a stopped by hand at 03:45 UTC (its lambda steps would read noise) |
| `eigs_planted_lift.log` | ell_eigs.py with the floor lift: planted OK, planted --mutate=beyn BAD, planted_ill (no lift) BAD, planted_ill --lift OK, --lift --mutate=nolift BAD |
| `lift_criteria.log` | the pass criteria for the lift on real states (C1 established roots, C2 reference independence, C3 resolved sign), written before lane K |
| `lane_k.sh`, `lane_k.log`, `lane_k_a.log`, `lane_k_b.log`, `lane_k_note.log` | lane K: ell_lam.py (lambda_1 with the lift) at k_c 55 D 16.5, 17, 17.5, 18, k_c 63 D 17, and lane J-b's D 16.25, 16.75 items (`out/ell_lam_lift_1025.jsonl`); stopped at 04:50 UTC after C1 failed at k_c 55, D 17 |
| `lift_offset_prediction.log`, `lane_a.sh`, `lane_a.log` | test (a): the lift's root shift at k_c 55, D 17 against the reference's distance (0.01, 0.001), with the prediction written first (`out/ell_lam_offset_1025.jsonl`) |
| `post_D18.5_numbers.log` | the numbers of the D 18.5 post |
| `svdtrack.py`, `svdtrack_criteria.log`, `svdtrack_control_note.log`, `svddiag.py`, `lane_s.sh`, `lane_s.log` | lane S: does lambda_1's zero at k_c 55, D 17 sit in a regular singular value of M (a V out of the floor) or inside the floor? SVD track with planted and D 13 k_c 31 controls and the criteria written first (`out/svdtrack_1025.jsonl`). The D 13 control misread (the V's chain breaks at avoided crossings with regular pairs), so the D 17 track did not run; cause and planted crossing case in `svdtrack_control_note.log`; then lambda at k_c 47 at D 16.25 and 16.75 (`out/l1kc47{Fq,Fp}1025.jsonl`; k_c 55 there runs on win2b, I1025-win2b) |
| `svdiso.py`, `svdiso_criteria.log`, `svdiso_planted.log`, `svdiso_control_note.log`, `lane_iso.sh`, `lane_iso.log` | lane ISO: the isolation test (is lambda_1's V isolated near the root, and does a sigma-fit there return the det root?), criteria and planted written first; D 13 k_c 31 control and its shift mutation, then k_c 55 D 17 (`out/svdiso_1025.jsonl`). The D 13 control failed: M's small singular values form a ladder of pairs (neighbour ratios 1.8-4.2), so lambda_1's V is never isolated, and its zero is carried by the ladder's bottom member (`svdiso_control_note.log`); D 17 did not run |
| `out/sol_l1kc55F1025_D*.npy`, `out/l1kc55F1025.jsonl` | the k_c 55 leap's states and records, D 17 to 19.625 (it stopped at its psi-constraint bar 1e-2 at 08:19 UTC 2026-11-20; `leap_kc55_fold.log`); kept for a fixed root finder |
| `lane_t_prediction.log`, `lane_t.sh`, `lane_t_a.log`, `lane_t_b.log` | lane T: lambda at k_c 71 at D 17 (from winb's k_c 63 state) and at k_c 63 at D 16, each with its signtest; the coordinator's prediction written first (`out/l1kc71Fm1025.jsonl`, `out/l1kc63Fm1025.jsonl`) |
| `svd_fallback_check.log`, `lane_t_b2.sh`, `lane_t_b2.log` | lane T-b's first refine stopped on numpy's gesdd failing to converge on a finite k_c 63 Jacobian (macOS Accelerate); diagnosis, the gesvd fallback's check with its control (wip/ell1-highD bb3fae9b), and T-b's rerun |
| `post_summary_numbers.log` | the numbers of the #1025 summary post (ell_delta collect and table at the raw commit it names, the lift shifts, T1, the leap's rows) |
| `dd_e1e2_criteria.log`, `lane_dd.sh`, `lane_dd.log` | route (c), first experiment: is the large-D sign failure the LU's rounding (E1, a double-double banded LU of the double M over exact variants) or M's entries (E2, 1e-16 to 1e-14 relative noise, all blocks and per block)? Control D 13, k_c 31; then k_c 55, D 17.5; criteria and the coordinator's reading rule written first (`out/ell_dd_sens_1025.jsonl`) |
| `dd_checkAB_criteria.log`, `lane_ddA.sh`, `lane_ddA.log` | route (c): checks A (the double-double mode matrix against float64 blocks 0-11, its horizon series against the x-ODE in mpmath) and B (dd det signs and the dd root at D 13), with the development findings and bars written first (`out/ell_ddm_checks_1025.jsonl`) |
| `dd_e1e2b_criteria.log`, `lane_dd2.sh`, `lane_dd2.log` | E1/E2 repeated inside the noise window at k_c 55, D 17.5 (the first run, `lane_dd.log`, had no power: float64 resolved the sign at its lambda too); a float64 sign scan picks the lambda first (`out/ell_dd_scan_1025.jsonl`) |
| `dd_signtest_D17.5_criteria.log`, `lane_dd17.sh`, `lane_dd17.log` | route (c) milestone 4: the double-double M's det sign at k_c 55, D 17.5 at six lambda where float64's sign flips erratically, with entry noise 1e-24-1e-16 and the hionly control; criteria first (`out/ell_ddm_D17.5_1025.jsonl`) |
