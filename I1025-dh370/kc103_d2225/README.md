# I1025-dh370/kc103_d2225: k_c 103 at D 22.25, regridded from dh610's accepted k_c 95 state, then a hybrid sign scan at lambda 0.02 to 0.50

Written 2026-11-25 09:34 UTC by the clock, before any run of this folder (the pins, the worktree check and a dry run of the regrid driver's pins came first: `steps_dry.txt`; no regrid, no scan). Machine `dh370-fedora` (Fedora, i7-8700, 6 cores / 12 threads, 31 GB), session claude-me2. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Coordinator t5. Roots are identified by position; the orientation is printed as the reader prints it and is information.

## Order (t5's hc, 2026-11-25 about 09:30 UTC), verbatim
"Next, #1025: k_c 103 at D 22.25 from dh610's accepted k_c 95 state (raw I1025-dh610/kc95_d2225, tag l1kc95dh610d2225; pin by blob; kc95 check accepts, controls 1 1, kc87 and kc103 checks refuse). Recipe as winb's k_c 103 runs (worktree at 48c36355 or later, which has kc103_syscheck_1025.py 3ab58d16): ell_refine.py l1kc95dh610d2225 95 l1kc103dh370d2225 103 1 22.25 <lambda_0(22.25) from ell_delta.lam0_at> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma, 6 threads, nice 10, systemd-run unit, cap 12 h; accept with kc103_syscheck (controls 1 1, kc95 check refusing). Then a scan lambda 0.02 to 0.50 by 0.04 plus the repeat of 0.14, 5 processes. Register first: A ('- to +') near 0.434 as at k_c 95 if k_c 95 is near converged at D 22.25; A dived (as k_c 87's 0.108) if not; B ('+ to -') above A. Report every robust change with printed orientation. Raw I1025-dh370/kc103_d2225/, README first. Walk d continues beside it."

## Inputs (raw origin/main e66a4244b at 09:31 UTC; copies in `in/`, `in_blobs.txt` has the full `git hash-object --no-filters` blobs; the drivers refuse any other blob)
| item | raw path | blob |
|---|---|---|
| source state: dh610's k_c 95 at D 22.25 | I1025-dh610/kc95_d2225/sol_l1kc95dh610d2225_D22.2500.npy | d709a8c0 |
| its record (one row: |F| 3.9737761418e-10, 3128 steps, constraint 4.701e-03, Delta 1.1526691088, 3203 s) | I1025-dh610/kc95_d2225/l1kc95dh610d2225.jsonl | e83e529e |
| k_c 95 check (the source's) | I1025-dh610/kc95_d2225/in/kc95_syscheck_1025.py | d487e628 |
| k_c 87 check | I1025-dh610/kc95_d2225/in/kc87_syscheck_1025.py | 6df5d960 |
| k_c 103 check (the k_c 95 check with 3 lines changed; dh170's) | I1025-dh170/kc103_d21125/in/kc103_syscheck_1025.py | 3ab58d16 |
| scanner (xfkappa's, unmodified) and its change finder | I1025-dh610/kc95_d2225/in/d18_hybsign.py, d185_scan_read.py | e089207a, 7c9d400f |
| reader, repeat check | I1025-dh610/kc95_d2225/in/read_lower.py, repeat_check.py | 89309d3c, aaf598a9 |
Code: worktree `~/Source/choptuik-large-d-1025` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_refine.py` 631e5801, `ell_delta.py` fde699f5, no changes in `solver/` outside `data/`); python `~/Source/choptuik-large-d-1058b/.venv` (3.14.10, multidouble avx2), the same as my k_c 79 regrids. **lambda_0(22.25)** from `ell_delta.lam0_at(22.25, *ell_delta.lam0_table())` in this worktree: **2.1019003706**, equal to dh610's regrid argument at this D (the driver stops if it reads otherwise; unused with `--no-gamma`).

## Commands (one systemd user unit `i1025k103` under systemd-inhibit, `lane_k103.sh`; stops at the first failure, `exits_k103.txt`, `VERDICT.txt`, `steps.txt`)
The drivers are dh170's `run_regrid.sh` and `run_scan.sh` of `I1025-dh170/kc103_d21125` (his k_c 95 to 103 at D 21.125 on this OS and machine class), changed in the lines of `diff_regrid_vs_dh170_kc103_d21125.txt` and `diff_scan_vs_dh170_kc103_d21125.txt`: the paths and worktree, 8 to 6 threads, the cap 21600 to 43200 s (t5's 12 h), the memory alert level 2048 to 1024 MiB (t5's rule: alert only under 1 GB or on a kill), and, new in the regrid driver, **the k_c 87 check's selftest and its refusal of the source** (t5's "kc87 and kc103 checks refuse"). `stage.conf` holds the tags, D, lambda_0, the pins and the scan lists.
1. Pins; selftests of the k_c 95, k_c 103 and k_c 87 checks (exit 0); the source: `kc95_syscheck_1025.py` exit 0 on state and record, `--mutate=F` and `--mutate=steps` exit 1, the k_c 103 check exit 1 and the k_c 87 check exit 1 on the source.
2. Regrid, in `solver/matter`, 6 threads, nice 10, cap 43200 s: `ell_refine.py l1kc95dh610d2225 95 l1kc103dh370d2225 103 1 22.25 2.1019003706 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`. ACCEPTED only when `kc103_syscheck_1025.py` exits 0 on the result, `--mutate=F` and `--mutate=steps` exit 1, and `kc95_syscheck_1025.py` exits 1 on the result. Stops: a refused result, an exception, the cap.
3. Scan, `d18_hybsign.py` on the accepted state: lambda 0.02, 0.06, ..., 0.50 (13 values) and the repeat of 0.14 (14 evaluations), **5 processes of 1 thread**, nice 10, in 3 rounds (5, 5, 4): p0 0.42, 0.50, 0.14 (the repeat); p1 0.46, 0.34, 0.06; p2 0.38, 0.30, 0.02; p3 0.14, 0.26, 0.18; p4 0.10, 0.22. Round 1 holds the two hypotheses' brackets, (0.42, 0.46) and (0.10, 0.14), and 0.38; the repeat is on another process than its first. Every process must print the record system. **Memory gate before the scan** (not in the order; dh610's idea): the scan starts when MemAvailable is at least 22000 MiB (5 x 3.8 GiB + 3 GiB; dh170's k_c 103 scan point peaked at 3.69 GiB) and waits at most 6 h, polling each 60 s; nothing is stopped or killed for memory, and a build (t5's `i1088a`, a 25 GB rustc for 10 to 40 min) delays the scan rather than competing with it.
4. Reading: `read_lower.py selftest` (0) and its mutations `shift`, `round2` (1 each), then `read_lower.py scan 0.02 0.50` and `repeat_check.py`. The reader prints lambda to three decimals and finds a change between two adjacent evaluated points of opposite hybrid sign; **on this 0.04 grid a change is placed only to a bracket 0.04 wide, and the det-linear estimate and its range are crude (a spread over interpolation choices, not an enclosure)**; two roots inside one interval cancel and are not seen. No robust change in the window: reported as read, no widening.

## Acceptance (fixed before the run)
Source accepted with controls 1 1, refused by the k_c 103 and k_c 87 checks; regrid exits 0 inside 43200 s; the result accepted by the k_c 103 check with both controls exit 1 and refused by the k_c 95 check; every scan process prints the record system and exits 0; the repeat of 0.14 agrees. A control that fires, an exception or a refusal stops the work and I report it; no bar is loosened.

## Predictions, registered before the runs
**t5's (the order's):** **A** (printed '- to +') **near 0.434** as at k_c 95 (dh610's k_c 95 at D 22.25: bracket (0.430, 0.435), det-linear 0.434264, range [0.434029, 0.434264], '- to +' as printed) **if k_c 95 is near converged at D 22.25**; **A dived** (as k_c 87's lower root, macm3 at D 22.25: bracket (0.100, 0.120), '- to +', det-linear 0.108387) **if not**; **B** (printed '+ to -') **above A** (k_c 87's upper root at D 22.25: 0.442516, '+ to -', macm3).
How I read it, fixed here: on the 0.04 grid, "A near 0.434" is a robust '- to +' change with bracket (0.42, 0.46), the only interval holding 0.434; "A dived" is one with bracket below 0.38 (as at k_c 87: (0.10, 0.14)); a robust change in (0.38, 0.42) or (0.46, 0.50), or anywhere else, is neither and is reported as read. B is a robust '+ to -' change whose bracket lies above A's. If k_c 95's single root at D 22.25 sits at 0.434 and k_c 103 moves it by less than 0.02, A is in (0.42, 0.46). Every robust change is reported with its printed orientation, bracket, det-linear and range.
**Mine (information, not pass rules):**
- Source accepted with controls 1 1 and the k_c 103 and k_c 87 checks refusing it: 90%. Regrid exits 0 and is accepted (both controls exit 1, the k_c 95 check refusing): 85%.
- Steps: the k_c 95 to 103 ratio was 1.0842 (D 21.125) and 1.0839 (D 21.0), so about 3391 for dh610's 3128 (within 30: 60%). |F| below 1e-9: 90%. Delta(103) - Delta(95) between -5e-5 and -1e-6: 65%. Regrid wall 4000 to 9000 s (60%: dh610's k_c 87 to 95 took 3203 s on 8 threads at this D, dh170's k_c 95 to 103 7305 s against 5523 s for 87 to 95 at D 21.125, a factor 1.32; mine has 6 threads and the load below). Peak RSS of the regrid below 4 GiB: 85% (dh170: 3.00 GiB).
- Scan: every point noise-robust 70%; the repeat bit-identical 85%; at least one robust change in the window 90%; A near 0.434 (bracket (0.42, 0.46)) 50%, A dived 20%, neither or none 30%; a B in the window 35%; the float64 sign equal to the hybrid at every point 25%. Scan wall 4 to 9 h from its start (60%): per point 3500 to 9000 s (dh170's k_c 103 points at D 21.125: 3500 s on a quiet machine, 8700 s with 4 processes beside another job; my k_c 79 points took 2021 s on 4 processes and 3813 s on 6, memory-bound), 3 rounds.
- Load: the regrid takes 6 threads at nice 10, the walk d (#1080) about 1.3 cores, and t5's `i1088a` units up to 6: about 13 on the 12 hardware threads, as t5 ordered.

## Status
- 2026-11-25 09:34 UTC: folder, inputs, drivers, dry run (pins, worktree and lambda_0 pass) and this README written before any run; the unit `i1025k103` starts next.
- 2026-11-25 09:34:44 to 09:34:56 UTC: unit `i1025k103` started. Selftests of the k_c 95, k_c 103 and k_c 87 checks exit 0 0 0. **Source check accepted:** `kc95_syscheck_1025.py` exit 0 on dh610's state and record, `--mutate=F` and `--mutate=steps` exit 1, the k_c 103 check exit 1 and the k_c 87 check exit 1 on the source (`source_*.txt`). **Regrid started 09:34:56 UTC** (6 threads, nice 10, cap 43200 s), load 2.5, MemAvailable 28.3 GB.

## Regrid result (25 Nov, 09:34:56 to 11:34:31 UTC): ACCEPTED
`ell_refine.py` (6 threads, nice 10, unit `i1025k103`) exited 0 after **7173 s** (7175 s wall); mean sampled CPU 569% (118 samples, `regrid_samples.csv`), peak sampled RSS **2.98 GiB**; 27 numpy RuntimeWarning lines in the log, as in the earlier regrids. A 27 GB rustc of t5's `i1088a` ran beside it from about 10:05 (MemAvailable fell to 0.7 GB at 10:14, no kill; recovered to 24 GB by 11:15).
- Record `l1kc103dh370d2225.jsonl` (blob 1516ffe9) and state `sol_l1kc103dh370d2225_D22.2500.npy` (blob 9b920bad): k_c 103 at D 22.25, |F| **4.0298416048e-10** (dh610's k_c 95: 3.9737761418e-10), F_start 1.944e-05, **3392 steps** (k_c 95: 3128; ratio 1.0844), constraint **2.928e-03** (k_c 95: 4.701e-03), **Delta 1.152663118278** (k_c 95: 1.1526691088; shift **-5.99e-06**).
- **Acceptance:** `kc103_syscheck_1025.py` exit 0 (the state's |F| equals the record's, `freeze_from` gives 3392 steps = the record's); `--mutate=F` exit 1, `--mutate=steps` exit 1; `kc95_syscheck_1025.py` on the k_c 103 result exit 1 (refuses it). Source check (09:34:56): k_c 95 check exit 0, controls 1 1, the k_c 103 and k_c 87 checks refuse it. The memory gate passed at once (MemAvailable 28.5 GB); the scan started **11:34:42 UTC**, 5 processes.

### Regrid predictions scorecard (mine, registered before the run)
| prediction | result |
|---|---|
| source accepted, controls 1 1, k_c 103 and k_c 87 checks refuse it (90%); regrid accepted (85%) | right; right |
| steps about 3391 (within 30: 60%) | right (3392) |
| \|F\| below 1e-9 (90%) | right (4.03e-10) |
| Delta(103) - Delta(95) between -5e-5 and -1e-6 (65%) | right (-5.99e-6) |
| regrid wall 4000 to 9000 s (60%) | right (7173 s) |
| peak RSS below 4 GiB (85%) | right (2.98 GiB) |

## Scan, round 1 done (11:34:42 to 13:52 UTC, 5 processes, 7679 to 8266 s per point)
| lambda | hybrid sign | noise-robust | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.10 | + | True | + | -3055.0710 | 8206 |
| 0.14 | + | True | + | -3058.4345 | 8117 |
| 0.38 | + | True | + | -3081.7544 | 8266 |
| 0.42 | + | True | - | -3087.4107 | 8137 |
| 0.46 | - | True | + | -3089.4372 | 7679 |
- Interim (information only; the reader's reading comes after the scan): between 0.42 and 0.46 the hybrid sign goes **+ to -** (both points noise-robust), where t5's A near 0.434 would show '- to +' there. No '- to +' change is seen in 0.10 to 0.46; the lower part of the window (0.02, 0.06) and 0.18 to 0.34 are not yet evaluated, and two roots inside one 0.04 interval would not be seen. The float64 sign differs from the hybrid at 0.42 and 0.46.
- Round 2 (0.50, 0.34, 0.30, 0.26, 0.22) and round 3 (the repeat of 0.14, 0.06, 0.02, 0.18) follow, about 2.3 h each; the scan should end about 18:30 UTC.
