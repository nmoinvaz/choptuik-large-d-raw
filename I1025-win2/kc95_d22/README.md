# I1025-win2/kc95_d22: macm3's k_c 87 leg state at D 22.0 regridded to k_c 95, then a hybrid sign scan around lambda_1

Machine win2 (Windows 11, 20 logical CPUs, 95.5 GB RAM; runner win2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-24 17:44 UTC, before any regrid or scan of this folder
(the drivers `kc95_regrid.sh` and `kc95_scan.sh` and the tools in `inputs/` are here; the dry runs are in `dry21875/`). The D 22.5 point is the same drivers in `../kc95_d225/`.

## Order (coordinator t5, hc, 24 Nov ~17:25 UTC), verbatim
"STOP THE FAR SCOUT NOW by exact pid ... (done at 17:27 UTC, see ../kc79_leap/README.md)
2. CANCEL THE QUEUED k_c 95 LEAP (same reason: an h 0.0625 path; at h 0.03125 a k_c 95 leg would take ~35 h to D 21.75). Instead, from tag g's end (19:20), k_c 95 REGRIDS at chosen D from macm3's k_c 87 leg states, which are at h 0.03125 from D 21.8125 on:
first D 22.0, then D 22.5, each as soon as macm3 pushes that state (raw I1025-macm3/kc87_leg2/b/, tag l1kc87Lmacm3b). Each: pin by blob, kc87_syscheck accepts it (controls 1 1); ell_refine.py <tag> 87 <new tag> 95 1 <D> <lambda_0 from its record>
--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma, 4 threads BelowNormal, 6 h cap; kc95_syscheck_1025.py accepts the result (controls 1 1, kc87 check refuses); then d18_hybsign.py with 4 processes on lambda = (macm3's k_c 87 root at that D + 0.003)
rounded to 0.005, +-0.01 by 0.005, plus a repeat of the centre (prediction: k_c 87 root + 0.003, bar 0.005). Raw kc95_d22/ and kc95_d225/ in your folder, README first. dh610 does the same at D 21.75 now.
Two new Opus sessions of mine run on this machine since 17:21 (desktop-pc/t24 and t25, 6 threads each): leave their processes alone, as they leave yours."

## Inputs (pinned by `git hash-object --no-filters`; the drivers refuse any other blob)
| item | where | blob |
|---|---|---|
| macm3's k_c 87 state and record at D 22.0 | raw `I1025-macm3/kc87_leg2/b/` (`sol_l1kc87Lmacm3b_D22.000000.npy`, `l1kc87Lmacm3b.jsonl`), fetched by `fetch_macm3.py` through `gh api` and checked against the listing's blob; the blobs are recorded in `in/fetched.txt` | recorded at the fetch |
| k_c 87 check (dh610's; the source's acceptance); k_c 95 check (the result's acceptance) | `../kc95_leap/inputs/` | 6df5d960; d487e628 |
| `d18_hybsign.py` (xfkappa's, unmodified; its first line is the record-system check); `read_lower.py` (dh170's); `repeat_check.py`; `leg_read.py`; `d185_scan_read.py`; `d18c_read.py` | copies of `I1025-dh610/kc95_d2175/in/` in `inputs/` | e089207a; 89309d3c; aaf598a9; 5cae2639; 7c9d400f; 1383470f |
| `pair2025.py` (my repeat gate, from `../kc79_d2025/`); `centre.py` (the scan centre from macm3's `roots87.txt`) | `inputs/` | e692c61d; the file's own selftest |
Code for the regrid and the scan: worktree `D:/choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's; `ell_refine.py` 631e5801; `ell_delta.py` fde699f5), python 3.14 with multidouble 5.1.0 (`venv-md510`).

## Commands
1. `kc95_regrid.sh 22.0 l1kc95win2d22 kc95_d22` (one driver, own session through `cim_start.ps1`, BelowNormal): pins and selftests (the k_c 87 and k_c 95 checks `--selftest` 0; `fetch_macm3.py --selftest` 0 and `--mutate` 1); waits for macm3's D 22.0 state and record row;
   `kc87_syscheck_1025.py` accepts the source (controls `--mutate=F` and `--mutate=steps` exit 1 each); the state goes into the worktree's `data/` under the name `ell_refine.py` reads; waits for the tag g leap's end (all8.done, 19:19:49 UTC at its cap) and for any other regrid of mine;
   in `solver/matter`, 4 threads, cap 21600 s by the exact root pid, no retry:

       python -u ell_refine.py l1kc87Lmacm3b 87 l1kc95win2d22 95 1 22.0 <lambda_0 = ell_delta.lam0_at(22.0)> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma

   Accepted only when `kc95_syscheck_1025.py` exits 0 on the result, `--mutate=F` and `--mutate=steps` exit 1 each, and `kc87_syscheck_1025.py` on the result exits 1 (refuses). `regrid_accepted.txt` or `regrid_refused.txt` says which.
2. `kc95_scan.sh 22.0 l1kc95win2d22 kc95_d22`: waits for `regrid_accepted.txt` and for macm3's k_c 87 root at D 22.0 in raw `I1025-macm3/kc87_leg_lambda/roots87.txt` (read with `gh api`); centre = (root + 0.003) rounded to 0.005 (`centre.py`; selftest 0, `--mutate` 1);
   the six evaluations centre-0.01, -0.005, centre, +0.005, +0.01 and the repeat of the centre on FOUR processes of one thread (P1 centre, centre+0.01 | P2 the repeat, centre-0.01 | P3 centre-0.005 | P4 centre+0.005), caps 28800 s by exact pids,
   after my other `d18_hybsign.py` scans have ended and 18.4 GB are free (a wait, not a stop; nothing is stopped for memory); then `read_lower.py` on the folder over centre +-0.01, `repeat_check.py`, `pair2025.py` (P1 and P2 first records, the same lambda), and
   `leg_read.py read` against the prediction root + 0.003 (bar 0.005).

## Acceptance (fixed before the run)
Source accepted with controls 1 1; the regrid exits 0 inside 21600 s; the result accepted by `kc95_syscheck_1025.py` with controls 1 1 and refused by the k_c 87 check; every scan process prints "the record system" (else it exits 3); the repeat of the centre agrees with the centre
(`pair2025.py` 1e-6); a robust sign change found by `read_lower.py` is reported by position as read (a bracket, with the estimator range named as a spread over estimator choices, not an enclosure). No robust change in the window: reported as read, no widening.
A pin that differs, a selftest or control that does not read as written, a source not accepted, a regrid not accepted or over the cap, or a scan process that fails stops the lane and I report it.

## Status
- 2026-11-24 17:44 UTC: folder, drivers, inputs and README written; dry runs of both drivers (`dry21875/`, on macm3's D 21.875 state) first, then the lane for D 22.0 waits for macm3's state and tag g's end.
- 2026-11-24 17:50 UTC: the coordinator (hc): "macm3 scans every multiple of 0.125 while its leap runs, so D 22.0 and 22.5 are both scanned; no skip. If a root has not appeared 3 h after macm3 pushed that state, tell me rather than wait the 12 h." Both lanes' drivers are running and wait (D 22.0 and D 22.5);
  an alert watcher reports at 3 h after the fetch of macm3's state if its root is not in `roots87.txt`.
- 2026-11-24 17:55 UTC: the coordinator (hc): "yes, hold the k_c 95 regrids until the #1078 build on t25 ends (its rustc is near its expected peak, ~35 GB); start them when committed memory is back below ~80 GB. Your tag g leap continues to its cap. Report any allocation failure at once."
  The regrid drivers (D 22.0 and D 22.5; they were waiting for macm3's states, nothing computed) were killed by exact pid after command-line checks (the wrapper trees 22088 and 40384, then the leftover bash 45868, 34240, 41444, 34364 and fetch pythons 30364, 39700; one first
  attempt of mine failed on a PowerShell parse error and killed nothing) and restarted with a commit gate in `kc95_regrid.sh`: after tag g's end and no other regrid of mine, it waits until committed memory (`\Memory\Committed Bytes`) is below 80 GB (a wait; nothing is stopped; the gate's threshold was tried on planted values 98.0 and 80.0
  hold, 79.9 and 70 go). The scan drivers are unchanged (their 18.4 GB free-memory gate).

## D 22.0 from macm3's part b2 (the coordinator's hc, 25 Nov ~01:40 UTC; written 2026-11-25 01:40 UTC before any regrid or scan of this lane; dry run of the regrid driver on this source 01:42 UTC, `dry22b2/`)
Order (verbatim): "ruling: k_c 95 at D 21.875 = 0.598590 by position, +0.002113 above k_c 87 (D 21.75's step was -0.000991). Next, same procedure: k_c 95 at D 22.0 from macm3's part b2 state (raw I1025-macm3/kc87_leg2/b2/, tag l1kc87Lmacm3b2, D 22.0; its k_c 87 root 0.544982), folder kc95_d22/ (reuse its drivers), no memory gate needed now.
Prediction: 0.544982 + 0.0005 (bar 0.005; the two steps so far straddle zero). Then hold the D 22.5 lane until b2 reaches 22.5."
- Source: macm3's part b2 D 22.0 state (`I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.000000.npy`, blob 84bc8e08, committed 2026-11-24 13:00 -08:00) and record (`l1kc87Lmacm3b2.jsonl`, the D 22.0 row: |F| 4.0460e-10, 2874 steps, constraint 6.319e-3, Delta 1.145631292134, h 0.03125, 1150 s). The fetch tool takes the leg by `--path=I1025-macm3/kc87_leg2/b2 --tag=l1kc87Lmacm3b2` (the drivers: `SRC_TAG` and `SRC_PATH`).
- Root: macm3's reading of that state (`I1025-macm3/kc87_leg_lambda/22.0/read_lower.txt`: robust change (0.540, 0.545), - to +, det-linear 0.544982, range [0.544963, 0.544982], a spread over estimator choices; `roots87.txt` row `22.0 0.544982`), the same number the order names. The scan driver reads it from `roots87.txt`.
- Centre: the prediction is root + 0.0005 = 0.545482 (bar 0.005); my reading of "same procedure" is the centre ON THE PREDICTION, rounded to 0.005: 0.545, evaluations 0.535, 0.540, 0.545, 0.550, 0.555 and the repeat of 0.545 on its own process (P1 0.545, 0.555 | P2 0.545 repeat, 0.535 | P3 0.540 | P4 0.550), four processes of one thread. (The previous point's centre was root + 0.003 rounded; its window would here be 0.540 to 0.560; this window 0.535 to 0.555 holds the prediction 0.5455 and 0.550 as well.)
  `centre.py` takes `--offset=0.0005` (selftest 0; the new planted cases call it; `--mutate` exits 1 on them; the scan driver passes `CENTRE_OFFSET`).
- Regrid: `ell_refine.py l1kc87Lmacm3b2 87 l1kc95win2d22 95 1 22.0 <lambda_0 = ell_delta.lam0_at(22.0)> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, 4 threads, BelowNormal, cap 21600 s, `COMMIT_GATE_GB=off` (no memory gate, as ordered); accepted only by `kc95_syscheck_1025.py` (controls 1 1; the k_c 87 check refuses it). The scan driver follows by itself (18.4 GB free).
- The D 22.5 lane (`../kc95_d225/`) is held until part b2 reaches D 22.5 (b2's newest state at this writing: D 22.3125).
- Earlier in this folder: the first D 22.0 plan (from part b, which stopped at the D 22.0 step) was retargeted to `../kc95_d21875/`; its drivers never fetched anything.
- 2026-11-25 01:43 UTC: both drivers started through `cim_start.ps1` (`SRC_TAG=l1kc87Lmacm3b2 SRC_PATH=I1025-macm3/kc87_leg2/b2 COMMIT_GATE_GB=off`; scan `ROOT_OVERRIDE=0.544982 ROOT_SOURCE=macm3-22.0-read_lower.txt-and-order CENTRE_OFFSET=0.0005`). Source fetched (state blob 84bc8e08, record file blob 8e5cbee9 with 11 rows) and accepted (selftest 0, controls 1 1). The regrid started at 01:43:10 UTC, root pid 40000, cap 21600 s (07:43 UTC at the latest), committed memory 62.4 GB.
- 2026-11-25 01:50 UTC: the coordinator (hc): "your reading is right: centre 0.545, window 0.535-0.555 plus the repeat. Read the orientation as well as the position, and say if it differs from macm3's '- to +' at this D." The plan stands. The reading will give the position (bracket, det-linear, estimator range) and the orientation of the robust change against macm3's k_c 87 orientation at D 22.0 (`- to +`, bracket (0.540, 0.545)).
- 2026-11-25 03:51 UTC: **regrid ACCEPTED** (D 22.0, from part b2). `ell_refine.py` exit 0 in 7668 s (01:43:10 to 03:50:58 UTC, root pid 40000, worker 25784, about 15,500 CPU s; committed memory 62 to 66 GB, no allocation failure). Result (state blob daae6b2e, record blob 85e66736, one record): |F| 4.1701e-10, F_start 3.642e-5, 3139 steps (k_c 87 source: 2874, ratio 1.0922), psi-constraint 3.910e-3 (source 6.319e-3), Delta 1.145617390443 (k_c 95 minus k_c 87: -1.3902e-5).
  `kc95_syscheck_1025.py` exit 0 (state |F| and `freeze_from` steps equal the record's); controls `--mutate=F` exit 1 (state |F| 4.170126e-10 not within 1% of the record's 6.255188e-10) and `--mutate=steps` exit 1 (3139 against 3140); `kc87_syscheck_1025.py` on the result exit 1 (the record is not k_c 87). The scan started by itself at 03:51:14 UTC: four processes (root pids 31324, 42076, 37628, 40392; lists 0.545,0.555 | 0.545,0.535 | 0.540 | 0.550), caps 28800 s (11:51 UTC at the latest), prediction 0.5455 (macm3's root 0.544982 + 0.0005, bar 0.005); the orientation is read against macm3's `- to +` at this D.
- 2026-11-25 04:57 UTC: **scan done, reading (D 22.0, k_c 95, from part b2)** (`read_lower.txt`, `leg_read.txt`, `summary_scan.txt`; four processes, exit 0 each; P3 0.540 and P4 0.550 in 2106 and 2107 s, P1 and P2 two evaluations each in 3982 s). Every process printed the record system (|F| 4.17006e-10 against the record's 4.17013e-10, steps 3139 = 3139).

### Result (D 22.0, k_c 95)
Hybrid signs: 0.535 -, 0.540 -, 0.545 -, 0.550 +, 0.555 +. Not noise-robust: none. **The float64 sign differs from the hybrid sign at 0.550** (float64 -1, hybrid +1; at 0.555 both are +1; the hybrid sign has the double-double block and the noise test and is the one read). The repeat of 0.545 (P1 and P2) agrees bit for bit (ln|det| -2800.4769864417; `read_lower.py`, `repeat_check.py`, `pair2025.py` pass).
One robust change in the window, **- to +**, in (0.545, 0.550): det-linear 0.545920, estimator range [0.545581, 0.545920] (a spread over estimator choices, not an enclosure). Orientation: the same as macm3's k_c 87 reading at this D (`- to +`, bracket (0.540, 0.545), det-linear 0.544982). No ln|det| local minimum without a sign change; end signs - at 0.535 and + at 0.555.
Prediction (macm3's root 0.544982 + 0.0005 = 0.545482, bar 0.005): change minus prediction +0.000420, within the bar. The k_c 87 to k_c 95 shift of the det-linear root is +0.000938 (0.545920 against 0.544982); at D 21.875 it was +0.002113 and at D 21.75 -0.000991 (the coordinator's figure). The float64 signs alone would put the bracket at (0.550, 0.555), also `- to +`.
