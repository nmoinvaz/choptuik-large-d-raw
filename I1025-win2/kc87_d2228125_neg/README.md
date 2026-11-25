# I1025-win2/kc87_d2228125_neg: negative-lambda hybrid sign scan of macm3's k_c 87 part b2 state at D 22.28125

Machine win2 (Windows 11, 20 logical CPUs, 95.5 GB RAM; runner win2 claude-me2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 08:46 UTC, before the scan of this folder (the driver `kc87_negscan.sh` and its dry run, which stops before the scan, are here).

## Order (coordinator t5, hc, 25 Nov ~08:55 UTC), verbatim
"yes, use the 4 free threads: D 22.28125 k_c 87 (same pinned state), lambda -0.08, -0.12, -0.16, -0.20, -0.26, -0.32, -0.40, -0.50 plus the repeat of -0.12, 4 procs. Register first: a '- to +' root somewhere below -0.06 if the dive accelerated (its slopes -2.0, -4.2, -5.5 per unit D were growing), none if it ended otherwise
(a pole of det crossing lambda = 0 instead of a zero). Report every robust change and ln|det|'s shape (a dip toward a zero, or a rise toward a pole)."

## Registered readings (fixed before the scan)
The previous scan of this state (`../kc87_d2228125_low/`) read hybrid sign + at all nine lambdas from -0.06 to 0.10 and ln|det| falling smoothly with slope -73.5 to -77.8 per unit lambda. The sign at 0.02 to 0.10 was - at D 22.25 (same leg, macm3). The two readings registered for lambda in [-0.50, -0.08]:
- **(a) the dive accelerated, the zero is below -0.06**: exactly one robust change `- to +` in (-0.50, -0.08) (sign - below it, + above it, the orientation macm3 reads at D 22.25), and ln|det| shows a **dip toward a zero** (it falls over the points just above the root, steeper than the -75 to -78 per unit lambda of the previous scan, and is lowest beside the change; a sign change with no dip would be a pole read as a sign flip and is listed as such).
- **(b) it ended otherwise (a pole of det crossing lambda = 0 instead of a zero)**: no robust change in the window (sign + at every lambda from -0.50 to -0.08), and ln|det| smooth or **rising toward a pole** (a rise, or a sharp maximum, at the lowest lambdas); a sign change with a ln|det| rise toward it (a sharp maximum) would be a pole inside the window and is reported as that.
- Neither: a root below -0.50 is not covered by this scan; the scan then reads (b)'s pattern (all +) and the README says the window ends at -0.50.
How the scan is read: the sign at each lambda, every robust change by bracket, orientation as `read_lower.py` prints it, det-linear estimate and estimator range (a spread over estimator choices, not an enclosure); float64 signs differing from the hybrid sign, non-robust points and ln|det| minima without a sign change are listed as printed; the ln|det| values are tabulated against lambda joined with the previous scan (-0.06 to 0.10) in `joint/`. (`read_lower.py` prints a lambda to three decimals followed by its sign, so `-0.080+` is lambda -0.080 with sign +.)

## Inputs (pinned; the driver refuses any other)
As `../kc87_d2228125_low/README.md`: macm3's part b2 k_c 87 state at D 22.28125 (raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.281250.npy`, blob 3ce8bc2e) and its record row (sha1 0eb8d22e), the k_c 87 check (6df5d960, must accept; controls 1 1) and the k_c 95 check (d487e628, must refuse), `d18_hybsign.py` e089207a, `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9, `pair2025.py` e692c61d. Code: worktree `D:/choptuik-i1025k79` at 48c36355, python 3.14 with multidouble 5.1.0 (`venv-md510`).

## Commands (`kc87_negscan.sh`, one driver started through `cim_start.ps1`)
1. Pins and selftests; the source fetch, state blob and row hash pinned, the k_c 87 check accepts (controls 1 1), the k_c 95 check refuses (as the previous driver; its dry run passes first).
2. Scan, now, beside the D 22.5 wide scan (8 threads; no wait for other `d18_hybsign.py` scans, the 18.4 GB free-memory wait stays): four processes of one thread, caps 28800 s by the exact root pids: P1 -0.12, -0.26, -0.50 | P2 -0.12 (the repeat), -0.20 | P3 -0.08, -0.32 | P4 -0.16, -0.40 (9 evaluations: the order's eight lambdas and the repeat of -0.12).
3. Reading: `read_lower.py` over -0.50 to -0.08 in this folder, `repeat_check.py`, `pair2025.py` on the first records of P1 and P2; then `joint/` holds copies of this folder's and the previous scan's rows (renamed so the reader sees both) and `read_lower.py` over -0.50 to 0.10 and a table of ln|det| by lambda.

## Acceptance (fixed before the run)
Source accepted with controls 1 1 and the k_c 95 check refusing it (dry run); every scan process prints "the record system"; the repeat of -0.12 on a second process agrees (1e-6); each robust change is reported by position and orientation, with ln|det|'s shape beside it. No points beyond the order. A pin that differs, a selftest or control that does not read as written, or a scan process that fails stops the lane and I report it.

## Status
- 2026-11-25 08:46 UTC: folder and README (the registered readings) written before the driver is run.
- 2026-11-25 08:47 UTC: dry run passed (`dry_stdout.txt`, `exits_negscan.txt`): pins and selftests (each mutation exit 1), macm3's state fetched (state blob 3ce8bc2e, the D row hash 0eb8d22e, record file blob 40d927af), accepted by `kc87_syscheck_1025.py` (controls 1 1), refused by the k_c 95 check; plan `scan_plan.txt`. The driver starts next.
