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
