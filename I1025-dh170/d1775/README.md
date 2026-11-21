# I1025-dh170/d1775: #1025 hybrid sign scan at D 17.75, k_c 63, lambda 1.70 to 1.95 at 0.01 (xfkappa's scan (A) of D 18)

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025 (the coordinator's hc, 21 Nov ~07:45 UTC; beside the #1057 reads, which keep priority).

## Why
At D 18 the dd signs read -, +, - at lambda 1.7529, 1.7887 and 1.8245 (win2b/win2, #1025 comment 7059272560): two sign changes, so two eigenvalues near lambda_1. winb's row B at D 17.75 sees one sign change near 1.865 with the orientation flipped
(plus below, minus above). The question: how many robust sign changes does the hybrid see across 1.70 to 1.95 at D 17.75, and where.

## Reading (the coordinator's, fixed before the run)
Count the robust sign changes and bracket each. Two changes mean the second eigenvalue is present at D 17.75 too. A sign change counts when both neighbouring grid points are noise-robust (p4_hybrid's 1e-15 noise test on blocks 0-11, 2 seeds, leaves the hybrid sign unchanged);
a change with a non-robust neighbour is listed, not counted. The float64 sign is printed beside each point and the points where it differs from the hybrid's are listed. `d1775_read.py` (planted test: two changes with their brackets and orientations, a non-robust neighbour not counted, one change, no change;
`--mutate` (non-robust counted) exit 1) prints it; the numbers quoted are from `d1775_scan_dh170.jsonl`.

## What runs
xfkappa's scan (A) (raw `I1025-mac/d18/lane_d18b.sh`, quoted in my `lane_d18b_xfkappa.sh`): `timeout 21600 nice -n 10 $PY -u $Q/d18_hybsign.py $STUB $ST 18 $L $SCAN` with L = 1.70, 1.71, ..., 1.90 (21 points), `d18_hybsign.py` blob e089207a (p4_hybrid's `sd()`: float64 blocks 0-11, dd block 12, the noise test, the float64 sign beside).
Here (`lane_d1775_dh170.sh`): `nice -n 10 /usr/bin/time -v python -u d18_hybsign.py I1025-win/out/l1kc63W1025.jsonl I1025-win/out/sol_l1kc63W1025_D17.750000.npy 17.75 1.70,1.71,...,1.95 d1775_scan_dh170.jsonl` (26 points; the record file is winb's, whose D 17.75 row is the stub: |F| 2.4283e-10, 2598 steps),
4 threads (OPENBLAS, OMP, MKL, VECLIB, RAYON = 4), `P4_WT_MATTER` = the worktree's `solver/matter`, an 8 h cap (28800 s) by exact pid.
Inputs (raw origin/main 53a490dc, blobs checked with `git hash-object --no-filters` against the tree ids, in `~/scratch1025d1775/`): winb's state `sol_l1kc63W1025_D17.750000.npy` de9fc3e5 (k_c 63), winb's `l1kc63W1025.jsonl` c33039df, and for the cross-check
`sol_l1kc63W1025_D18.000000.npy` 45e72c6a and xfkappa's `d18_stub_l1kc63W1025.jsonl` 2cfdb833. Code: worktree `~/Source/choptuik-large-d-1025p4` at 505d8399 (clean), python = the #1058 venv (hp 8179068d; numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, multidouble 5.1.0's package).

## Controls and stops (the script runs them first; each stops the lane)
1. Planted control: `ell_ddm.py selftest` must PASS and `ell_ddm.py selftest --mutate=slices` must FAIL (xfkappa's lane; 1800 s each).
2. Cross-check on known numbers: the hybrid at D 18, lambda 1.8, on xfkappa's inputs must give sign +1, noise-robust, float64 +1 and ln|det| -1925.0182289868 to 1e-6 (his `d18_hybsign.log`: "lam 1.8: hybrid +1 ln|det| -1925.0182289868 ... float64 +1 -1920.9910370828 (353 s)"). It can fail; a failure stops the scan.
3. The scan; if the 8 h cap is reached the points done are read as they are and the cap is reported.

## Resources
`/usr/bin/time -v` of the scan (user, system, CPU %, maximum RSS) in `d1775_scan.raw`; `watch_d1775.sh` samples every 30 s into `memlog_scan.log` (alert-only: ALERT lines in `alert_scan.log`; stops nothing) and raises the scan's nice to 19 while the #1057 lane reads a state (a user cannot lower nice again; `prio_scan.log`).
Reference timing: xfkappa's hybrid at lambda 1.8 took 353 s on the Mac (4 threads).

## Log
- 2026-11-21 07:49:48 UTC: folder, scripts and inputs prepared; the reading and controls are fixed above before any run.
- 2026-11-21 07:50:31 UTC: **lane started** 07:49:57 UTC (`lane_d1775_dh170.sh` bash pid 1080054; `watch_d1775.sh` pid 1080106). Pins checked; stage 1 the planted control: `ell_ddm.py selftest` PASS and `--mutate=slices` FAIL (as required, `ell_ddm_selftest.log`); stage 2 the cross-check at D 18, lambda 1.8 started 07:49:58.
- 2026-11-21 07:57:25 UTC: **the stage 2 cross-check FAILED its criterion as I wrote it** (`d18_crosscheck1_dh170_FAILED_criterion.log`, `.jsonl`; `exits_d1775_v1.txt`): the hybrid at D 18, lambda 1.8 on xfkappa's inputs gave sign +1 (his +1), noise-robust (both seeds +1), float64 +1 (his +1), the record system (|F| 2.6321e-10 against 2.6303e-10, 2552 steps), **ln|det| -1925.0179512680 against his -1925.0182289868: +2.78e-04, against my tolerance of 1e-6**, 444 s. The lane stopped, as written; the scan did not start. **Cause (the tolerance was mis-specified, not the data):** the hybrid's ln|det| carries float64 LAPACK noise: win2's dd determinant against the hybrid's at the three D 18 grid points differs by -4.7e-04, +8.8e-05 and +1.4e-04 (#1025 comment 7059272560), the same scale as the 2.8e-4 here, and the float64 full-matrix ln|det| differs by 0.67 between this machine (-1921.6636) and xfkappa's Mac (-1920.9910); only the SIGN of a determinant is the quantity this scan reads. I took 1e-6 from the P4 cross-check's lambda tolerance, which is a different quantity.
- 07:58 UTC: **revised cross-check, written before it runs (v2, `lane_d1775_dh170.sh`; v1 kept as `lane_d1775_dh170_v1.sh`):** the hybrid at D 18 at xfkappa's three grid points 1.752930001950494, 1.788704083622953 and 1.824478165295412 (his root record `ell_d18_hybrid_1025.jsonl` blob fbeaa7a1, `evals`) must give his signs -1, +1, -1, each noise-robust, with ln|det| within 1e-2 of his (a sanity bound an order above the 4.7e-4 scatter). This is stronger on the quantity that matters (three signs, one of them at a point where the float64 sign is known to be wrong, win2's table: float64 +1 at 1.824478) and it can fail; it is a change made after seeing a failure, so it is reported as one and the coordinator may overrule it. About 3 x 7.4 min. Then the scan as before (26 points at D 17.75).
