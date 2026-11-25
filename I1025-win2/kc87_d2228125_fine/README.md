# I1025-win2/kc87_d2228125_fine: fine lambda scan (-0.19, -0.18, -0.17) of macm3's k_c 87 part b2 state at D 22.28125

Machine win2 (Windows 11, 20 logical CPUs, 95.5 GB RAM; runner win2 claude-me2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 09:52 UTC, before the scan of this folder (the driver `kc87_finescan.sh` and its dry run, which stops before the scan, are here).

## Order (coordinator t5, hc, 25 Nov ~09:50 UTC), verbatim
"yes, run -0.19, -0.18, -0.17 on the 3 free threads, with the registration as you wrote it (zero: ln|det| plunges toward the bracket centre; pole: it rises). Name the k_c 87 roots by branch from now: this one is S (macm3's make_branches: S steep from above, F flat = lambda_1)."
(In reply to my report of the negative-lambda scan's round 2, `../kc87_d2228125_neg/`: hybrid sign + at -0.08, -0.12, -0.16 and - at -0.20, -0.26, -0.32, -0.40: a robust change `- to +` in (-0.20, -0.16), the orientation macm3 reads at D 22.25 for the root at 0.108387 (branch S). ln|det| rose toward more negative lambda throughout, -2402.32 at -0.16 and -2401.89 at -0.20, the slope across that pair -10.8 per unit lambda against -62 on one side and -134 on the other; float64 ln|det| -2404.88 against the hybrid -2401.89 at -0.20 only.)

## Registered readings (fixed before the scan)
Question: what is the feature in (-0.20, -0.16): a zero of det M (the S root) or a pole of det M? Reference for ln|det| in the bracket: the straight line between the two measured points, -2402.32 at -0.16 and -2401.89 at -0.20, which gives about -2402.2 (-0.17), -2402.1 (-0.18) and -2402.0 (-0.19); the smooth trend on the right (-0.08 to -0.16) continues at about -62 per unit lambda and the trend on the left (-0.26 to -0.40) at about -85 to -90.
- **Zero (the S root)**: the hybrid sign changes `- to +` between two of the points (or at a bracket end), and ln|det| **plunges toward the bracket centre**: the two or three points nearest the change lie several units (more than 1) below the reference line, lowest beside the change (|det| -> 0 at a zero; ln|det| ~ ln|lambda - lambda_S|).
- **Pole**: the sign changes `- to +` and ln|det| **rises** toward the bracket centre: the points nearest the change lie above the reference line, highest beside the change (|det| -> infinity).
- Neither (a smooth continuation, the sign change between -0.20 and -0.19 or between -0.17 and -0.16 with no plunge or rise): listed as such, the feature narrower than 0.01.
The sign change is read by position to the 0.01 grid (the bracket of two neighbouring points, with `read_lower.py`'s det-linear estimate and estimator range, a spread over estimator choices, not an enclosure), orientation as printed, float64 signs differing from the hybrid sign and the float64 ln|det| beside the hybrid one listed (at -0.20 they differ by 3.0). `joint/` joins this scan with `../kc87_d2228125_low/` (-0.06 to 0.10) and `../kc87_d2228125_neg/` (-0.50 to -0.08) in one reading and a table of ln|det| and its slope against lambda.

## Inputs (pinned; the driver refuses any other)
As `../kc87_d2228125_low/README.md`: macm3's part b2 k_c 87 state at D 22.28125 (raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.281250.npy`, blob 3ce8bc2e) and its record row (sha1 0eb8d22e), the k_c 87 check (6df5d960, must accept; controls 1 1) and the k_c 95 check (d487e628, must refuse), `d18_hybsign.py` e089207a, `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9, `pair2025.py` e692c61d. Code: worktree `D:/choptuik-i1025k79` at 48c36355, python 3.14 with multidouble 5.1.0 (`venv-md510`).

## Commands (`kc87_finescan.sh`, one driver started through `cim_start.ps1`)
1. Pins and selftests; the source fetch, state blob and row hash pinned, the k_c 87 check accepts (controls 1 1), the k_c 95 check refuses (dry run first, 09:50 UTC).
2. Scan, now: three processes of one thread, caps 28800 s by the exact root pids: P1 -0.19 | P2 -0.18 | P3 -0.17 (no repeat is ordered), beside the D 22.5 wide scan and the last evaluation (-0.50) of the negative-lambda scan (8 threads of mine).
3. Reading: `read_lower.py` over -0.19 to -0.17 in this folder, then `joint/` (this scan, `../kc87_d2228125_neg/` and `../kc87_d2228125_low/`, rows as of the end of this scan) over -0.50 to 0.10 and the ln|det| table.

## Acceptance (fixed before the run)
Source accepted with controls 1 1 and the k_c 95 check refusing it (dry run); every scan process prints "the record system"; each robust change is reported by position and orientation with ln|det|'s shape beside it, and the S branch named. No points beyond the order. A pin that differs, a selftest or control that does not read as written, or a scan process that fails stops the lane and I report it.

## Status
- 2026-11-25 09:52 UTC: folder and README (the registered readings) written; the dry run passed (`dry_stdout.txt`, `exits_finescan.txt`). The driver starts next.
- 2026-11-25 09:51 UTC: the scan started by itself (the driver run through `cim_start.ps1`): three processes, root pids 47228, 41384, 35408, caps 28800 s (17:51 UTC at the latest); about 1800 to 2500 s per evaluation: the three points ~10:25 UTC.
