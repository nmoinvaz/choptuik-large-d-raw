# I1025-win2/kc95_d2225_low: low-lambda hybrid sign scan of dh610's k_c 95 state at D 22.25

Machine win2 (Windows 11, 20 logical CPUs, 95.5 GB RAM; runner win2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 04:33 UTC, before the scan of this folder (the driver `kc95_lowscan.sh` and its dry run, which stopped before the scan, are here).

## Order (coordinator t5, hc, 25 Nov ~04:30 UTC), verbatim
"next after your D 22.0 reading (~05:01): a low-lambda scan of dh610's k_c 95 state at D 22.25 (raw I1025-dh610/kc95_d2225, tag l1kc95dh610d2225; pin by blob; kc95 check accepts it, controls 1 1). Scan lambda 0.02 to 0.18 by 0.02 plus the repeat of 0.10, and 0.20 to 0.40 by 0.04, 4 procs.
Report every robust change by position and orientation. Reason: at k_c 87 a second root appeared at D 22.25 near lambda 0.11 ('- to +', macm3); at k_c 95 the lambda_1 root at 0.434 still reads '- to +', so either k_c 95 has no second root there yet or it sits elsewhere.
That decides whether the new mode is physical or a resolution effect. Raw kc95_d2225_low/, README first."

## Inputs (pinned by `git hash-object --no-filters`; the driver refuses any other blob)
| item | where | blob |
|---|---|---|
| dh610's k_c 95 state at D 22.25 | raw `I1025-dh610/kc95_d2225/sol_l1kc95dh610d2225_D22.2500.npy`, fetched by `fetch_macm3.py --path=I1025-dh610/kc95_d2225 --tag=l1kc95dh610d2225` through `gh api` and checked against the listing | d709a8c0 |
| its record file (one record, from dh610's regrid; the lane's `in_blobs_regrid.txt` names both) | same folder, `l1kc95dh610d2225.jsonl` | e83e529e |
| k_c 95 check; k_c 87 check (must refuse the k_c 95 state) | `../kc95_leap/inputs/` | d487e628; 6df5d960 |
| `d18_hybsign.py` (xfkappa's, unmodified; its first line is the record-system check, exit 3 if not); `read_lower.py`; `d185_scan_read.py`; `d18c_read.py`; `repeat_check.py`; `pair2025.py` | `../kc95_d22/inputs/` | e089207a; 89309d3c; 7c9d400f; 1383470f; aaf598a9; e692c61d |
Code: worktree `D:/choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's), python 3.14 with multidouble 5.1.0 (`venv-md510`).

## Commands (`kc95_lowscan.sh`, one driver started through `cim_start.ps1`)
1. Pins and selftests (`read_lower.py` 0 with `--mutate=shift` and `--mutate=round2` exit 1; `repeat_check.py` 0; `pair2025.py` 0 with `--break` 1; the k_c 95 and k_c 87 checks `--selftest` 0; `fetch_macm3.py --selftest` 0 and `--mutate` 1).
2. Source: fetch, blob pins, `kc95_syscheck_1025.py` exit 0 on dh610's state and record, `--mutate=F` and `--mutate=steps` exit 1 each, `kc87_syscheck_1025.py` exit 1 (refuses).
3. Scan, after my other `d18_hybsign.py` scans have ended and 18.4 GB are free (a wait; nothing is stopped for memory): `d18_hybsign.py in/l1kc95dh610d2225.jsonl in/sol_l1kc95dh610d2225_D22.2500.npy 22.25 <lambdas> scan_D22.25_pN.jsonl`, four processes of one thread, caps 28800 s by the exact root pids:
   P1 0.10, 0.14, 0.24, 0.36 | P2 0.10 (the repeat), 0.06, 0.20, 0.32 | P3 0.12, 0.08, 0.04, 0.28 | P4 0.16, 0.18, 0.02, 0.40 (16 evaluations: 0.02 to 0.18 by 0.02 is 9, the repeat of 0.10 is 1, 0.20 to 0.40 by 0.04 is 6).
4. Reading: `read_lower.py` over 0.02 to 0.40 (every robust change by position: bracket, det-linear, estimator range, and orientation), `repeat_check.py` on the merged rows, `pair2025.py` on the first records of P1 and P2.

## Acceptance (fixed before the run)
Source accepted with controls 1 1 and the k_c 87 check refusing it (done in the dry run, 04:32 UTC); every scan process prints "the record system"; the repeat of 0.10 on a second process agrees (1e-6); each robust change is reported by position and orientation, with the estimator range named as a spread over estimator choices and not an enclosure;
float64 signs that differ from the hybrid sign, non-robust points and ln|det| local minima without a sign change are listed as the reader prints them. No widening or extra points beyond the order. A pin that differs, a selftest or control that does not read as written, or a scan process that fails stops the lane and I report it.

## Status
- 2026-11-25 04:33 UTC: folder, driver and README written; the dry run (`dry_stdout.txt`, `exits_lowscan.txt`) accepted dh610's state (blob d709a8c0, record file blob e83e529e; controls 1 1; the k_c 87 check refuses) and stopped before the scan. The driver starts next and waits for the D 22.0 scan's four processes to end (~05:01 UTC).
- 2026-11-25 04:58 UTC: scan started by itself (four processes, root pids 21932, 43052, 40308, 41540, caps 28800 s). 07:17 UTC: scan done (four processes exit 0 in 8303 to 8356 s; four evaluations each, about 2000 to 2160 s per evaluation; every process printed the record system: |F| 3.97422e-10 against the record's 3.97378e-10, steps 3128 = 3128).

## Result (D 22.25, k_c 95, dh610's state; `read_lower.txt`, `summary_lowscan.txt`)
Hybrid signs, 15 distinct lambdas: 0.02 -, 0.04 -, 0.06 -, 0.08 -, 0.10 -, 0.12 -, 0.14 -, 0.16 -, 0.18 -, 0.20 -, 0.24 -, 0.28 -, 0.32 -, 0.36 -, 0.40 -. Not noise-robust: none. **The float64 sign differs from the hybrid sign nowhere.** The repeat of 0.10 on a second process agrees bit for bit (ln|det| -2726.8585936241; `read_lower.py`, `repeat_check.py` and `pair2025.py` pass).
**Robust changes: 0.** No ln|det| local minimum without a sign change. End signs - at 0.020 and - at 0.400. ln|det| falls monotonically over the window: -2719.670 at 0.02 to -2755.294 at 0.40, with the slope d ln|det|/d lambda -89.6 per unit lambda at 0.02 to 0.04, slowly steepening (-91.9 at 0.18 to 0.20, -97.9 at 0.32 to 0.36) to -106.6 at 0.36 to 0.40; no dip.
Against the other readings at this D (raw): dh610's k_c 95 reading of lambda_1 (`I1025-dh610/kc95_d2225/read_lower.txt`: 0.430 -, 0.435 +, one change `- to +` in (0.430, 0.435), det-linear 0.434264): the sign is - at 0.400 here and - at 0.430 there, so the two scans join without a gap in the sign pattern. macm3's k_c 87 reading at this D (`I1025-macm3/kc87_leg_lambda/22.25_low/read_lower.txt` and `22.25_wide/read_lower.txt`): - for 0.02 to 0.10, one change `- to +` in (0.100, 0.120) (det-linear 0.108387, range [0.100867, 0.108387]), + for 0.12 to 0.44, then `+ to -` in (0.440, 0.445) (det-linear 0.442516).
So in 0.02 to 0.40 the k_c 95 determinant keeps the sign it has at the lowest lambda (-), and k_c 87 has one more sign change in the same window (at 0.108); the orientation of the lambda_1 root follows from that count: `+ to -` at k_c 87 (after the extra root) and `- to +` at k_c 95 (no extra root). **At k_c 95 there is no second root in (0.02, 0.40) at D 22.25.** Not covered: lambda below 0.02 (and negative lambda) at k_c 95; a root there would not change the signs read here, because the sign at 0.02 is - for both k_c.
