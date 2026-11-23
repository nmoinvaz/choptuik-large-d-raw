# I1025-dh610/reconv_d1975: re-convergence on Linux of dh170's and macm3's k_c 87 D 19.75 states (ell_refine.py at k_c 87 to 87), where the two states differ (ell_cond.py), and, if they come together, their signs at lambda_1 1.32, 1.33, 1.34

Machine dh610 (Fedora 45, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 06:32:57 UTC, before any run of this folder.

## Order (coordinator t5, the #1025 comment posted 07:00 UTC 23 Nov and hc), in part
First report the D 19.75 k_c 95 scan if it has ended (it had not at the time of writing: round 2 was running). Then the re-convergence test on Linux, two `systemd-run --user` units at the same time, 8 threads each, nice 10, in solver/matter with
both states copied into data/ under their tags and checked by blob: (1) `ell_refine.py l1kc87dh170d1975 87 l1kc87linRe 87 1 19.75 2.1120935738 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma` (dh170's state 352107a8, record
6078a0b4); (2) the same with src l1kc87macm3d1975 (macm3's 5825f5d0, 84f75a48) and tag l1kc87macRe. k_c equals k_c_src, so there is no regrid, only 16 more LM Jacobians. Then (3) `solver/matter/ell_cond.py` from branch wip/ell-cond (ee2c1dbd;
fetch it into a worktree, no changes) on (linRe, macRe) and on each start state against its own re-converged state: `STATE_A STATE_B 87 1 19.75 --kappa 0.7 --Ks 30 --u0 0.04 --out f.json`, plus its control `--mutate=plant` once (must exit 0 with
PASS; a failing control stops the work). (4) Only if |dz| between linRe and macRe is below 1e-7: `d18_hybsign.py` on both at 1.32, 1.33, 1.34. Report |F| before and after for each, the ell_cond lines, and the signs. Memory alerts only.

**Written before the run (the coordinator's):** more LM iterations lower |F| and pull the states together, roots within 0.002 in (1.32, 1.33); if |F| stays above 3e-10 the stopping point is the method's floor.

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs; the lanes refuse any other blob)
| item | source | blob |
|---|---|---|
| dh170's k_c 87 D 19.75 state (Linux; |F| 3.987605893965491e-10, 3124 steps, Delta 1.0860022726137006) | I1025-dh170/kc87_d1975/ at raw 9f63ed51 | 352107a8 |
| its record | same | 6078a0b4 |
| macm3's k_c 87 D 19.75 state (macOS; |F| 3.980170323712351e-10, 3124 steps, Delta 1.086003680648846) | I1025-macm3/kc87_d1975/ at raw 03c79c79 | 5825f5d0 |
| its record | same | 84f75a48 |
| my k_c 87 check; the scanner (xfkappa's, unmodified) | I1025-dh610/kc95_d1975/in/ | 6df5d960; e089207a |
| for the comparison: macm3's scan of its own state (rows 1.32, 1.33, 1.34), dh170's partial round 1 (1.32, 1.33), my Linux scan of macm3's state (`../cross_macm3_d1975/`, raw d8d1ee40) | `in/ref_*` | 702717f3; 0336f50f; 92b2a612 |
Code: **re-convergence** in `~/Source/choptuik-large-d-1025g/solver/matter` at 48c36355 (the code that made both states; `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's; `ell_refine.py` blob 631e5801). **ell_cond:** worktree
`~/Source/choptuik-large-d-1025h` at ee2c1dbd (branch wip/ell-cond, no changes; `ell_cond.py` blob 1bb7b995). That branch's `dss_ell.py` (a41da9a7) differs from the 1025g one (5d28c19e) only in `mode_matrix_c` and `svd_robust`, which `ell_cond.py` does not use,
and its `ell_refine.py` (0121ad81) in the missing `gelss` fallback of the `lstsq`; `ell_cond.py` prints |F(A)| at each start state, which must equal the record's |F| (a check of the same residual). **Scan** (step 4): `~/Source/choptuik-large-d-1025f` at 505d8399 (clean).
Python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble avx2).

## Commands (systemd user units under `systemd-inhibit`)
1. **Re-convergence**, two units at the same time (`lane_reconv_refine.sh lin|mac` via `start_refine_lin.sh` = unit i1025y and `start_refine_mac.sh` = unit i1025z): in `solver/matter` of 1025g, 8 threads each, nice 10, cap 21600 s (a time cap only), the commands of the order (above). Each lane checks the pins, copies the state into `data/` under its tag (dh170's is already there from `../kc95_d1975`; checked by blob), refuses to start with less than 8 GiB free, samples RSS and CPU every minute, and on exit 0 copies the result into `in/` (`in_blobs_reconv_lin.txt`, `in_blobs_reconv_mac.txt`). Outputs `lin/`, `mac/`.
2. **After** (`lane_reconv_after.sh` via `start_after.sh` = unit i1025aa, started at once and waiting for both `DONE.txt`): (info) `kc87_syscheck_1025.py` on both re-converged states with its two controls; (3) `ell_cond.py` control `--mutate=plant` on (linRe, macRe) once (exit 0 and "plant check: PASS", else the lane stops), then at the same time (linRe, macRe), (dh170's start state, linRe), (macm3's start state, macRe), 6 threads each, nice 10, `--kappa 0.7 --Ks 30 --u0 0.04 --out` into `cond/`; (4) if the `dz` of `cond/f_lin_mac.json` is below 1e-7: `d18_hybsign.py` on both re-converged states at 1.32, 1.33, 1.34, 6 processes of 1 thread, nice 10 (`scan/`); else `STEP4.txt` says it was not run.

## Acceptance (fixed before the run)
- Each re-convergence exits 0 (the cap is a stop). |F| before is the record's (and the k_c 87 check's value on this machine: dh170's 3.9876058940e-10, macm3's 3.9889482683e-10); |F| after is the new record's.
- The ell_cond control exits 0 with PASS; a failing control stops the work and I report it; no bar is loosened. `ell_cond.py` at each start state prints |F(A)| equal to the record's |F| to 4 digits (information; a mismatch is reported).
- Step 4 runs only if |dz| (linRe, macRe) is below 1e-7; then each of the 6 processes prints the record system and the signs are read as in `../cross_macm3_d1975` (hybrid sign, noise signs, float64 sign, ln|det|), the root read by position as the root near lambda_1's line, bracket (1.32, 1.33) as in the coordinator's reading.
- Reported: |F| before and after for each; the ell_cond lines (the singular values, |dz|, the components of dz along the smallest right singular vectors, the part outside them, Delta's entry, |J dz| against |F(B) - F(A)|); the signs if step 4 runs. Reading of the coordinator's line: **lowered |F| and a smaller |dz| support it; |F| staying above 3e-10 is the method's floor.**

## Predictions, registered before the run (information)
- The records' |F| at D 19.5 for k_c 79, 87, 95 are 3.512e-10, 3.523e-10, 3.534e-10 (three regrids, three k_c), and at D 19.25 3.11e-10, at D 19.75 3.98e-10 and 3.99e-10 (two builds): a smooth function of D and not of k_c or build. I expect that this is a floor of the method: |F| after within 5% of |F| before for both states about 80%, so the stopping point is the floor and |F| stays above 3e-10 (about 90%).
- |dz| between linRe and macRe stays above 1e-6 (about 80%), so step 4 is not run (about 85%); if it is run, the signs at 1.33 are the same for both, whichever they are (about 60%).
- The two ell_refine runs exit 0 (about 90%) in 1500 to 4500 s each (about 65%; the Jacobian count is what costs, 16 more as the order says, and I have no timing of one at this k_c with no regrid).
- ell_cond: the control passes (90%); |F(A)| equals the record's (85%); most of |dz| of the start-to-own-re-converged pairs and of the (linRe, macRe) pair lies along the few smallest right singular vectors, with a large Delta entry (about 65%).

## Status
- 2026-11-23 06:32:57 UTC: folder, inputs, lanes and the reading prepared before any run. The D 19.75 k_c 95 scan of `../kc95_d1975` has not ended (round 2 of two); both ell_refine units start now, so 16 + 4 = 20 threads at most until it ends.

## Result (2026-11-23, read 07:57 UTC; every number below is printed by `summarize_reconv.py` into `summary.txt`, from `in/*.jsonl`, `in/*.npy` and `cond/f_*.json`)

Everything ran as ordered and exited 0: the two ell_refine runs (lin 3748 s, mac 3652 s wall, side by side), the k_c 87 checks (information) on both re-converged states (ACCEPTED, and each control `--mutate=F`, `--mutate=steps` exits 1; `syscheck_*.txt`), the ell_cond control (`--mutate=plant`: exit 0, "plant check: PASS (v_min component 1.000000e-06, others max 2.4e-18, outside 2.8e-16)"), and the three ell_cond runs. No memory alert (`MEMALERT.txt` absent). **Step 4 was not run:** |dz| between linRe and macRe is 1.2693e-06, not below 1e-7 (`STEP4.txt`).

Re-converged states (`in/sol_l1kc87linRe_D19.7500.npy` blob 4988a55c, `in/l1kc87linRe.jsonl` 6735329b; `in/sol_l1kc87macRe_D19.7500.npy` a81f02dc, `in/l1kc87macRe.jsonl` 19f8e9ce). The k_c 87 roots are not yet physical.

```
| state | record norm F before | norm F of the first evaluation in ell_refine (F_start) | record norm F after | steps | Delta before | Delta after | seconds |
|---|---|---|---|---|---|---|---|
| dh170 start -> linRe | 3.9876058940e-10 | 3.9876058940e-10 | 3.9854188111e-10 | 3124 -> 3124 | 1.086002272614 | 1.086002272507 | 3746 |
| macm3 start -> macRe | 3.9801703237e-10 | 3.9904831991e-10 | 3.9851106831e-10 | 3124 -> 3124 | 1.086003680649 | 1.086002609309 | 3650 |

| pair (A, B) | norm F(A) | norm F(B) at A's freeze | smallest 8 singular values of J(A) | norm dz | Delta entry of dz | part of dz outside the 8 | largest component along one of the 8 | norm J dz | norm F(B)-F(A) | norm J dz / norm dz |
|---|---|---|---|---|---|---|---|---|---|---|
| (linRe, macRe) | 3.9855e-10 | 3.9850e-10 | 2.79e-16, 3.47e-16, 4.82e-16, 5.53e-16, 6.03e-16, 6.04e-16, 6.79e-16, 6.95e-16 | 1.2693e-06 | +3.3680e-07 | 1.2693e-06 (1.000) | 2.91e-12 (2.3e-06) | 1.0542e-12 | 1.6177e-12 | 8.31e-07 |
| (dh170 start, linRe) | 3.9858e-10 | 3.9855e-10 | 2.33e-16, 2.88e-16, 3.73e-16, 4.18e-16, 5.24e-16, 5.77e-16, 6.03e-16, 6.67e-16 | 4.0279e-10 | -1.0678e-10 | 4.0279e-10 (1.000) | 1.69e-17 (4.2e-08) | 1.1599e-12 | 1.0681e-12 | 2.88e-03 |
| (macm3 start, macRe) | 3.9886e-10 | 3.9850e-10 | 2.93e-16, 3.09e-16, 4.06e-16, 4.38e-16, 4.91e-16, 5.06e-16, 6.56e-16, 7.29e-16 | 7.0747e-06 | -1.0713e-06 | 7.0747e-06 (1.000) | 1.66e-12 (2.3e-07) | 1.3279e-11 | 1.2899e-11 | 1.88e-06 |
| planted control | 3.9854e-10 | 3.9861e-10 | 2.89e-16, 2.97e-16, 3.21e-16, 5.33e-16, 6.01e-16, 7.24e-16, 7.38e-16, 7.57e-16 | 1.0000e-06 | +1.1002e-12 | 2.7834e-16 (0.000) | 1.00e-06 (1.0e+00) | 9.1419e-16 | 6.6236e-13 | 9.14e-10 |

smax(J) 12.191154, n 5695, condition (linRe, macRe) 4.371e+16

| pair | norm dz (L2, Delta included) | Delta entry |
|---|---|---|
| (dh170d1975, macm3d1975) | 7.9032e-06 | +1.4080e-06 |
| (linRe, macRe) | 1.2693e-06 | +3.3680e-07 |
| (dh170d1975, linRe) | 4.0279e-10 | -1.0678e-10 |
| (macm3d1975, macRe) | 7.0747e-06 | -1.0713e-06 |
| (dh170d1975, macRe) | 1.2689e-06 | +3.3670e-07 |
| (macm3d1975, linRe) | 7.9034e-06 | -1.4081e-06 |
```

- **|F| after:** 3.9854e-10 (linRe) and 3.9851e-10 (macRe), both above 3e-10. dh170's |F| fell by 0.055% (3.98761e-10 to 3.98542e-10). macm3's record |F| rose by 0.12% (3.98017e-10 to 3.98511e-10) and fell by 0.13% from ell_refine's own first evaluation of its state (F_start 3.99048e-10). The same state gets different |F| from different evaluations (linRe: 3.98542e-10 the record, 3.98340e-10 the k_c 87 check, 3.98546e-10 ell_cond; macm3's start state: 3.98017e-10 the record, 3.99048e-10 ell_refine's F_start, 3.98895e-10 the k_c 87 check on this machine, 3.9886e-10 ell_cond), a spread of 0.05% to 0.26%, which is as large as the changes. I did not find the cause of that spread; this is not tested here.
- **ell_cond |F(A)| against the record (information):** not equal to 4 digits at the start states: dh170's start 3.9858e-10 against 3.9876e-10, macm3's start 3.9886e-10 against 3.9802e-10 (the k_c 87 check's value on this machine is 3.9889e-10); linRe 3.9855e-10 against 3.9854e-10.
- **The pull:** the distance between the two start states is 7.9032e-06; after, 1.2693e-06 (6.2 times smaller). dh170's state moved 4.0e-10 (nothing); macm3's moved 7.0747e-06, nearly all of the way to dh170's. The remaining 1.27e-06 is 0.0000 along the 8 smallest right singular vectors (largest component 2.9e-12), whole outside them, in all three pairs; the planted control reads 1.000 along v_0 with the same code. The smallest singular values are 2.3e-16 to 7.6e-16 against sigma_max 12.19 (condition about 4e16): eight of them are below eps * sigma_max = 2.7e-15.
- **Gain along dz:** |J dz| / |dz| is 8.3e-07 for (linRe, macRe), 1.9e-06 for (macm3 start, macRe) and 2.9e-03 for (dh170 start, linRe). The linearization holds for the two pairs with |F(B) - F(A)| about 1e-11 and 1e-12 (|J dz| 1.328e-11 against 1.290e-11 and 1.160e-12 against 1.068e-12); for (linRe, macRe) |J dz| is 1.054e-12 against |F(B) - F(A)| 1.618e-12. So a difference of 1.27e-06 between the two states changes |F| by about 1e-12, 0.3% of |F|: the stopping rule has no signal there. ell_refine's `--tol 1e-12` is a bar on |F| itself (`lm`: `nF < tol`), never reached at 4e-10, so each run stopped by another rule of `lm` (3 successive steps that each reduce |F| by less than half, no decrease, or the 12 + 4 Jacobian cap); ell_refine runs it quiet, so the log does not say which.
- **Delta's share of |dz|:** 27% for (linRe, macRe), 15% for (macm3 start, macRe), 27% for (dh170 start, linRe).
- **Not measured:** the roots. Step 4 would measure them on (linRe, macRe); it is not run (the order's bar is |dz| below 1e-7).

### Predictions against outcomes (registered before the run, above)

| prediction | outcome |
|---|---|
| F after within 5% of F before for both (80%) | yes (-0.055%; +0.12% or -0.13% by the record or by F_start) |
| norm F stays above 3e-10 (90%) | yes, 3.985e-10 for both |
| dz between linRe and macRe above 1e-6 in norm (80%), step 4 not run (85%) | yes (1.2693e-06), not run |
| both ell_refine runs exit 0 (90%), 1500 to 4500 s each (65%) | yes, 3748 s and 3652 s |
| ell_cond control passes (90%) | yes |
| ell_cond's norm F(A) equals the record's (85%) | no (3.9858e-10 against 3.9876e-10; 3.9886e-10 against 3.9802e-10) |
| most of dz along the few smallest right singular vectors (65%) | no: 0.000 along the 8, 1.000 outside, in all three pairs |

The coordinator's reading ("more LM iterations lower |F| and pull the states together, roots within 0.002 in (1.32, 1.33); |F| above 3e-10 is the method's floor"): |F| was not lowered beyond the spread between its evaluations; the states were pulled together, 7.9e-06 to 1.27e-06, by macm3's state moving; the roots were not measured; |F| stays above 3e-10, which that reading calls the method's floor.
