# I1025-win2/kc95_d2225_high: high-lambda hybrid sign scan (0.46 to 0.82) of dh610's k_c 95 state at D 22.25

Machine win2 (Windows 11, 20 logical CPUs, 95.5 GB RAM; runner win2 claude-me2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 10:57 UTC, **before the scan of this folder** (the driver `kc95_highscan.sh` and its dry run, which stops before the scan, are here).

## Order (coordinator t5, hc, 25 Nov ~10:55 UTC), verbatim
"accepted: S at D 22.28125 (k_c 87) is a simple zero at -0.1976, by the registered test. Next on your free threads: a k_c 95 HIGH scan of dh610's accepted D 22.25 state (raw I1025-dh610/kc95_d2225, pinned by blob; kc95 check accepts, controls 1 1), lambda 0.46 to 0.82 by 0.04 plus the repeat of 0.62, 4 procs.
Register first: if S exists at k_c 95 but dives later in D than at k_c 87, it sits above F (0.434) here, one '+ to -' (by rank) somewhere in 0.46-0.82; if S is a k_c 87 feature, no change. winb tests the same at D 22.125. Raw kc95_d2225_high/, README first. Then the D 22.5 reading as planned."

## Registered readings (fixed before the scan)
Known at this state (k_c 95, D 22.25): sign - for lambda 0.02 to 0.40 (`../kc95_d2225_low/`, no change), `- to +` in (0.430, 0.435) (dh610's reading of F = lambda_1, det-linear 0.434264), sign + at 0.435 to 0.455 (dh610). So the sign is + just above F, and at 0.46 the scan starts in a + region.
- **(a) S exists at k_c 95 and dives later in D than at k_c 87: it sits above F here**: exactly one robust change `+ to -` (by rank: the next root above F, + below it and - above it) somewhere in (0.46, 0.82), and then the sign is - from it to 0.82; ln|det| dips toward a zero as in the k_c 87 profile of S (the registered test at D 22.28125: zero, a simple one, `- to +`, with a ln|det| profile of the form a + s l + q l^2 + ln|l - lS|; here the orientation by rank is `+ to -` because F lies below).
- **(b) S is a k_c 87 feature**: no robust change in (0.46, 0.82): sign + at every lambda from 0.46 to 0.82.
- Neither: a change `- to +`, two or more changes, or a non-robust point, are listed as read; a root above 0.82 is not covered by this scan.
How the scan is read: the sign at each lambda, every robust change by bracket, orientation as `read_lower.py` prints it, det-linear estimate and estimator range (a spread over estimator choices, not an enclosure); float64 signs differing from the hybrid sign, non-robust points and ln|det| minima without a sign change are listed as printed; ln|det| and its slope against lambda in `joint/ln_table.txt` (four decimals) over 0.02 to 0.82, joined with `../kc95_d2225_low/` and dh610's scan. A model comparison (zero against pole, as `../kc87_d2228125_fine/fit_zero_pole.py`) is made only if a change is found, after the reading.

## Inputs (pinned; the driver refuses any other)
dh610's k_c 95 state at D 22.25 (raw `I1025-dh610/kc95_d2225/sol_l1kc95dh610d2225_D22.2500.npy`, blob d709a8c0) and its record file (`l1kc95dh610d2225.jsonl`, blob e83e529e), fetched by `fetch_macm3.py --path=I1025-dh610/kc95_d2225 --tag=l1kc95dh610d2225` through `gh api` and checked against the listing; the k_c 95 check (d487e628, must accept; controls 1 1) and the k_c 87 check (6df5d960, must refuse); `d18_hybsign.py` e089207a, `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9, `pair2025.py` e692c61d. Code: worktree `D:/choptuik-i1025k79` at 48c36355, python 3.14 with multidouble 5.1.0 (`venv-md510`).

## Commands (`kc95_highscan.sh`, one driver started through `cim_start.ps1`)
1. Pins and selftests; the source fetch, state blob and record blob pinned, the k_c 95 check accepts (controls 1 1), the k_c 87 check refuses (dry run first).
2. Scan, now (the D 22.5 wide scan's last evaluation runs beside it; the 18.4 GB free-memory wait stays): four processes of one thread, caps 28800 s by the exact root pids: P1 0.62, 0.46, 0.74 | P2 0.62 (the repeat), 0.50, 0.78 | P3 0.54, 0.66, 0.82 | P4 0.58, 0.70 (11 evaluations: the order's ten lambdas and the repeat of 0.62), three rounds of about 1900 to 2500 s.
3. Reading: `read_lower.py` over 0.46 to 0.82, `repeat_check.py`, `pair2025.py` on the first records of P1 and P2, then `joint/` over 0.02 to 0.82.

## Acceptance (fixed before the run)
Source accepted with controls 1 1 and the k_c 87 check refusing it (dry run); every scan process prints "the record system"; the repeat of 0.62 on a second process agrees (1e-6); each robust change is reported by position and orientation with ln|det|'s shape beside it. No points beyond the order. A pin that differs, a selftest or control that does not read as written, or a scan process that fails stops the lane and I report it.

## Status
- 2026-11-25 10:57 UTC: folder and README (the registered readings) written; the dry run and the start follow.
- 2026-11-25 10:57 UTC: dry run passed (`dry_stdout.txt`, `exits_highscan.txt`, `selftest_exits.txt` = 0 1 1 0 0 1 0 0 0 1): dh610's state (blob d709a8c0) and record file (blob e83e529e) fetched and pinned, accepted by `kc95_syscheck_1025.py` (controls 1 1), refused by the k_c 87 check. The driver starts next.
