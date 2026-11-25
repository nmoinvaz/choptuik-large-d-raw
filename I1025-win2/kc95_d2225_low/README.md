# I1025-win2/kc95_d2225_low: low-lambda hybrid sign scan of dh610's k_c 95 state at D 22.25

Machine win2 (Windows 11, 20 logical CPUs, 95.5 GB RAM; runner win2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 04:40 UTC, before the scan of this folder (the driver `kc95_lowscan.sh` and its dry run, which stopped before the scan, are here).

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
- 2026-11-25 04:40 UTC: folder, driver and README written; the dry run (`dry_stdout.txt`, `exits_lowscan.txt`) accepted dh610's state (blob d709a8c0, record file blob e83e529e; controls 1 1; the k_c 87 check refuses) and stopped before the scan. The driver starts next and waits for the D 22.0 scan's four processes to end (~05:01 UTC).
