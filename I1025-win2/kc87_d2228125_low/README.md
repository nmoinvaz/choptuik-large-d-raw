# I1025-win2/kc87_d2228125_low: low-lambda hybrid sign scan of macm3's k_c 87 part b2 state at D 22.28125

Machine win2 (Windows 11, 20 logical CPUs, 95.5 GB RAM; runner win2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 05:50 UTC, before the scan of this folder (the driver `kc87_lowscan.sh` and its dry run, which stopped before the scan, are here).

## Order (coordinator t5, hc, 25 Nov ~05:10 UTC), verbatim
"queue after your current D 22.25 k_c 95 low scan (do not stop it): a low scan of macm3's k_c 87 part b2 state at D 22.28125 (raw I1025-macm3, part b2 states; pin by blob, the kc87 check must accept it, controls 1 1). Scan lambda -0.06, -0.04, -0.02, 0.0, 0.02, 0.04, 0.06, 0.08, 0.10 plus the repeat of 0.02, 4 procs.
If the code refuses lambda <= 0, scan 0.005 to 0.10 instead and say so. Reason: macm3's reading (ii) has lambda_1 diving from 0.47 at D 22.156 to about 0.11 at D 22.25, which would put lambda_1 = 0 near D 22.28-22.3; this scan tests that.
Report every robust change by position and orientation. Raw kc87_d2228125_low/, README first with the prediction: under (ii) a '- to +' root in (-0.05, 0.05); under (i) none."

## Prediction (the order's, fixed before the scan)
Under (ii), macm3's reading of lambda_1 diving to zero near D 22.28 to 22.3: **one `- to +` root in (-0.05, 0.05)**. Under (i): **no robust change** in the window. (macm3's k_c 87 reading at D 22.25, `I1025-macm3/kc87_leg_lambda/22.25_low/read_lower.txt`: hybrid signs 0.020- ... 0.100- 0.120+ ... 0.180+, one change `- to +` in (0.100, 0.120), det-linear 0.108387, range [0.100867, 0.108387].)
How the scan is read: the sign at each lambda, the robust changes by bracket, orientation as `read_lower.py` prints it, det-linear estimate and estimator range (a spread over estimator choices, not an enclosure). A point that is not noise-robust, a float64 sign differing from the hybrid sign and an ln|det| minimum without a sign change are listed as printed.
(`read_lower.py` prints a point as the lambda to three decimals followed by its sign, so `-0.060-` is lambda -0.060 with sign -.)

## Inputs (pinned; the driver refuses any other)
| item | where | pin |
|---|---|---|
| macm3's part b2 k_c 87 state at D 22.28125 | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.281250.npy` (committed 2026-11-24 16:38 -08:00), fetched by `fetch_macm3.py --path=I1025-macm3/kc87_leg2/b2 --tag=l1kc87Lmacm3b2` through `gh api`, checked against the listing | blob 3ce8bc2e |
| its record (the D 22.28125 row of `l1kc87Lmacm3b2.jsonl`: |F| 3.8769e-10, 2865 steps, constraint 7.406e-3, Delta 1.153577636116, h 0.03125, 1527 s) | same folder; the file's blob changes with every push of the leg (40d927af at the first fetch), so the row is pinned by the sha1 of its line | 0eb8d22e |
| k_c 87 check (must accept); k_c 95 check (must refuse) | `../kc95_leap/inputs/` | 6df5d960; d487e628 |
| `d18_hybsign.py` (xfkappa's, unmodified); `read_lower.py`; `d185_scan_read.py`; `d18c_read.py`; `repeat_check.py`; `pair2025.py` | `../kc95_d22/inputs/` | e089207a; 89309d3c; 7c9d400f; 1383470f; aaf598a9; e692c61d |
Code: worktree `D:/choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's), python 3.14 with multidouble 5.1.0 (`venv-md510`).

## Lambda <= 0
The code does not restrict the sign of lambda: `DSSEll.mode_matrix(z, lam)` sets `self.lam = lam` and `ell_ddm.DDEll.mode_matrix` takes `float(lam)` (the tangent term is skipped only at exactly 0). `read_lower.py` reads negative and zero lambdas correctly on planted scans (a change in (0.02, 0.04) and one in (-0.02, 0.0), both read as written; the brackets and det-linear estimates are the planted ones).
The decision rule stands as ordered: if a process with a lambda <= 0 stops with an exception, the lane stops, I say so, and I rerun 0.005 to 0.10. A zero mode at lambda = 0 (a trivial one, if the system's gauge leaves one) would show as a point that is not noise-robust or a sign that disagrees between the two noise seeds: it is listed, not hidden.

## Commands (`kc87_lowscan.sh`, one driver started through `cim_start.ps1`)
1. Pins and selftests (as `../kc95_d2225_low/README.md`).
2. Source: fetch, the state blob and the row hash pinned, `kc87_syscheck_1025.py` exit 0 on the state and record, `--mutate=F` and `--mutate=steps` exit 1 each, `kc95_syscheck_1025.py` exit 1 (refuses): done in the dry run (05:47 UTC).
3. Scan, after my other `d18_hybsign.py` scans have ended (the k_c 95 low scan of D 22.25, due ~07:15 UTC) and 18.4 GB are free: four processes of one thread, caps 28800 s by the exact root pids: P1 0.02, -0.04, 0.10 | P2 0.02 (the repeat), 0.04, -0.06 | P3 0.0, 0.06 | P4 -0.02, 0.08 (10 evaluations).
4. Reading: `read_lower.py` over -0.06 to 0.10, `repeat_check.py`, `pair2025.py` on the first records of P1 and P2.

## Acceptance (fixed before the run)
Source accepted with controls 1 1 and the k_c 95 check refusing it (dry run); every scan process prints "the record system"; the repeat of 0.02 on a second process agrees (1e-6); each robust change is reported by position and orientation; no points beyond the order. A pin that differs, a selftest or control that does not read as written, or a scan process that fails stops the lane and I report it.

## Status
- 2026-11-25 05:50 UTC: folder, driver and README written; the dry run accepted macm3's state (blob 3ce8bc2e, the row hash 0eb8d22e, controls 1 1, the k_c 95 check refuses) and stopped before the scan. The driver starts next and waits for the k_c 95 low scan's four processes to end.
