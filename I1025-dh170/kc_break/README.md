# I1025-dh170/kc_break: #1025 where the k_c-stable branch of lambda_1 breaks, D 18.4375, k_c 63 and k_c 55, lambda 1.62 to 1.80 at 0.01

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-22 02:59:17 UTC, before any run.

## Order (the coordinator's hc, 22 Nov, after the usage pause), quoted
"lambda_1's branch is k_c-stable through D 18.25 (k_c 55 minus k_c 63: 1.3e-4 at D 17.75, 9.4e-4 at 18.125, 1e-4 at 18.25; comments 7071508693, 7072529186, 7072669877). At D 18.5 it is not (k_c 55 has a complex pair near 1.684). Find where it breaks. Your state is D 18.4375. Scan both k_c there over lambda 1.62 to 1.80 at 0.01 (19 points each): k_c 63 on raw I1025-mac/d18/sol_l1kc63Wm1025_D18.437500.npy (its leap record line) and k_c 55 on raw I1025-mac/out/sol_l1kc55F1025_D18.437500.npy (its record line), each with the system check first, d18_hybsign.py, the noise test and the float64 sign. Run the two k_c side by side, 4 threads each, nice 10 (BelowNormal on Windows), 8 h caps. Window and reading go into the README first, raw I1025-dh170/kc_break. Reading, fixed now: the k_c 55 root's det-linear estimate within 0.01 of the k_c 63 root's means stable at D 18.4375; no k_c 55 root there, or one further off, means it breaks by D 18.4375. Report any ln|det| minimum without a change, with a dip fit. Post on #1025."

## Window
lambda 1.62, 1.63, ..., 1.80 (19 points) on each k_c's state at D 18.4375, plus a repeat check: lambda 1.71 is evaluated first and last in each scan (21 evaluations per lane; the two extra are controls, not part of the 19). Where the k_c 63 root should lie: the k_c 63 path of comment 7072529186 has 1.742506 at D 18.25 and 1.677209 at D 18.5; the straight line between them gives 1.6935 at D 18.4375, inside the window, in the bracket (1.69, 1.70) if it is straight.

## What runs
- `lane_kcbreak_dh170.sh 63` and `lane_kcbreak_dh170.sh 55`, side by side, each: pins (blob hashes, worktree), the planted control `ell_ddm.py selftest` (must PASS) and `--mutate=slices` (must FAIL), then `nice -n 10 /usr/bin/time -v python -u d18_hybsign.py REC STATE 18.4375 LAMS OUT` with 4 threads (OPENBLAS, OMP, MKL, VECLIB, RAYON = 4), an 8 h cap (28800 s) by exact pid, a sampler every 30 s into `memlog_kc63.log` / `memlog_kc55.log` (alert-only: ALERT lines in `alert_kc.log`, nothing stopped). `d18_hybsign.py` (blob e089207a, unmodified, the Mac's) is the hybrid sign: float64 blocks 0-11 and dd block 12, with p4_hybrid's 1e-15 noise test on blocks 0-11 (2 seeds) and the float64 sign beside each point. Its first line is the **system check**: the state's |F| and step count against the record line's (equal within 1%, or 1e-13, and the same steps), else exit 3 and the lane stops.
- `read_kcbreak.sh` after both lanes: `d18k2_read.py 18.4375 1.62 1.80 <k_c 55 scan> <k_c 63 scan>` (blob 52f31e53, the Mac's reader of comment 7072529186, with d185_scan_read 7c9d400f, d18c_read 1383470f, d18d_read 6b608903): the det-linear estimate of every robust change (xfkappa's formula, `changes()` of d185_scan_read), the comparison within 0.01, the dip fit of every ln|det| minimum without a change (model c + s (lam - lam_min) + ln|(lam - a)^2 + beta|, beta > 0 a complex pair, beta < 0 two real roots), the repeated points' agreement, the float64 summary.
- Inputs (git blobs checked against the raw repository's tree at origin/main 7d6e1e09, copies in `~/scratch1025kc/in/`): k_c 63 state `I1025-mac/d18/sol_l1kc63Wm1025_D18.437500.npy` 16a17e5f6c93ffc425c71e1e2d9a2cab42c4827d and its record file `l1kc63Wm1025.jsonl` 08f4dbf367edba55814e5cf989ccd32a9a5dbe67 (the D 18.4375 row, the leap record line: F 2.787105944303022e-10, 2471 steps, Delta 1.0545799755186647); k_c 55 state `I1025-mac/out/sol_l1kc55F1025_D18.437500.npy` 2b8864095ed78a4a9d7999d6f9bc26114e64ed65 and `l1kc55F1025.jsonl` 0fb77df8281d634e6ecf2d3b2038e3706df3c960 (the D 18.4375 row: F 2.70718927167557e-10, 2157 steps, Delta 1.0545448462957352). The script picks the row of its D itself.
- Code: worktree `~/Source/choptuik-large-d-1025p4` at 505d8399 (clean, checked), python the #1058 venv (numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, multidouble's package with `dd_logdet`), as the D 17.75 scan of this folder's sibling `d1775/`.

## Reading, fixed now (the coordinator's)
For the k_c 63 robust change in 1.62 to 1.80: if k_c 55 has a robust change whose det-linear estimate is within 0.01 of k_c 63's, the branch is **k_c-stable at D 18.4375**. If k_c 55 has no robust change in the window, or its nearest is further than 0.01, it **breaks by D 18.4375** (between D 18.25 and 18.4375). A change counts when both neighbouring grid points are noise-robust; a change touching a non-robust point gives no reading and the coordinator rules (the reader's rule). Each state reads its own signs and the signs are not compared. Any ln|det| minimum without a sign change, in either scan, is reported with its dip fit. The float64 sign is reported beside the hybrid's (information).

## Controls (each can fail)
1. Planted `ell_ddm.py selftest` PASS and `--mutate=slices` FAIL, run first in each lane (a failure stops the lane).
2. The system check of `d18_hybsign.py` against the record line (a failure stops the lane, exit 3).
3. The repeat check: lambda 1.71 first and last in each scan; the reader's merge compares repeated points (sign, noise, ln|det|); a disagreement is a STOP-level reading ("repeat disagrees; no reading").
4. The reader's planted selftest before the runs (`selftest_d18k2_read.log`: 5 of 5 cases PASS) and its two mutations (`--mutate=tol`, `--mutate=dip`: each exits 1, `selftest_d18k2_read_mutate_*.log`).
5. The environment is the one of the D 17.75 scans of `d1775/` (same worktree, venv and script blob), whose cross-check at D 18 against xfkappa's three signs passed on this machine; I do not repeat it.

## Predictions, registered before the runs
- system check passes in both lanes about 95%; the repeat check agrees in both (bit-identical ln|det| as win2b's, 0.0 difference) about 90%;
- every point noise-robust: k_c 63 about 80%, k_c 55 about 70%;
- k_c 63: exactly one robust change in 1.62 to 1.80 about 85%, in (1.69, 1.70) about 65%;
- the reading (the four outcomes are exclusive): stable about 40%; breaks with one k_c 55 change further than 0.01 about 20%; breaks with no k_c 55 change (a complex pair: a ln|det| minimum without a change) about 30%; no reading (a non-robust neighbour or other) about 10%;
- a ln|det| minimum without a change, if there is one: its dip fit reads a complex pair (beta > 0) about 70%;
- the float64 sign differs from the hybrid's at no more than 5 of 21 points in each lane about 70%;
- wall: 21 evaluations at 300 to 480 s, so 1.8 to 2.8 h per lane (about 65%), both inside the 8 h cap about 95%; max RSS below 2.5 GiB each about 90% (the D 17.75 scan peaked at 1.3 GiB).

## Log
- 2026-11-22 02:59:17 UTC: folder, scripts and inputs prepared; the window, the reading and the controls are fixed above before any run. Reader selftest 02:58 UTC: PASS, both mutations FAIL.
