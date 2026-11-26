# I1025-dh370/kc111_d2225: k_c 111 at D 22.25, regridded from my accepted k_c 103 state, then a hybrid sign scan at lambda 0.02 to 0.50

Written 2026-11-25 17:37 UTC by the clock, before any run of this folder (the pins, the worktree check and a dry run of the regrid driver's pins came first: `steps_dry.txt`; no regrid, no scan). Machine `dh370-fedora` (Fedora, i7-8700, 6 cores / 12 threads, 31 GB), session claude-me2. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Coordinator t5. Roots are identified by position; the orientation is printed as the reader prints it and is information.

## Order (t5's hc, 2026-11-25 about 17:35 UTC), verbatim
"Coordinator (t5): important result, thanks. The (0.02, 0.06) root is S-like: k_c 87 has S at 0.108 at this D, k_c 95 has none in 0.02-0.82, and your k_c 103 has one at 0.06. Present at k_c 87 and 103, absent at 95: that looks like a k_c-parity effect of the discretization. Next for dh370, the test: k_c 111 at D 22.25 from your accepted k_c 103 state (tag l1kc103dh370d2225; kc103 check accepts, controls 1 1, kc95 and kc111 checks refuse; result: kc111_syscheck_1025.py 85aeb312 accepts, kc103 refuses), dh170's k_c 111 regrid recipe, 6 threads, then a scan 0.02 to 0.50 by 0.04 plus the repeat of 0.14, 5 procs. Register first: (P) parity: no root in 0.02-0.30, one root near 0.43-0.46 (F); (S) S is physical and converging: a root below 0.06 again, plus F. Raw I1025-dh370/kc111_d2225/, README first."

## Inputs (raw origin/main 153d67447 at 17:36 UTC; copies in `in/`, `in_blobs.txt` has the full `git hash-object --no-filters` blobs; the drivers refuse any other blob)
| item | raw path | blob |
|---|---|---|
| source state: my k_c 103 at D 22.25 | I1025-dh370/kc103_d2225/sol_l1kc103dh370d2225_D22.2500.npy | 9b920bad |
| its record (|F| 4.0298416048e-10, 3392 steps, constraint 2.928e-03, Delta 1.152663118278, 7173 s) | I1025-dh370/kc103_d2225/l1kc103dh370d2225.jsonl | 1516ffe9 |
| k_c 103 check (the source's) | I1025-dh370/kc103_d2225/in/kc103_syscheck_1025.py | 3ab58d16 |
| k_c 111 check (the k_c 103 check with 3 lines changed; dh170's) | I1025-dh170/kc111_d2175/in/kc111_syscheck_1025.py | 85aeb312 |
| k_c 95 check (refuses the source) | I1025-dh370/kc103_d2225/in/kc95_syscheck_1025.py | d487e628 |
| scanner and its change finder; reader; repeat check | d18_hybsign.py, d185_scan_read.py; read_lower.py; repeat_check.py (copies in my kc103_d2225/in/) | e089207a, 7c9d400f; 89309d3c; aaf598a9 |
Code, python and lambda_0: as `../kc103_d2225/`: worktree `~/Source/choptuik-large-d-1025` at 48c36355 (`ell_refine.py` 631e5801, `ell_delta.py` fde699f5, `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's), python `~/Source/choptuik-large-d-1058b/.venv` (3.14.10, multidouble avx2), lambda_0(22.25) = **2.1019003706** (the driver stops if it reads otherwise; unused with `--no-gamma`). The source state is already in the worktree's `solver/matter/data/` (the output of my k_c 103 regrid; blob 9b920bad checked).

## Commands (one systemd user unit `i1025k111` under systemd-inhibit, `lane_k111.sh`; stops at the first failure, `exits_k111.txt`, `VERDICT.txt`, `steps.txt`)
Drivers: my `../kc103_d2225/run_regrid.sh`, `run_scan.sh` and `lane_k103.sh` (themselves dh170's k_c 103 drivers), with the changes of `diff_regrid_vs_kc103_d2225.txt` and `diff_scan_vs_kc103_d2225.txt`: the paths, the source and target k_c, the checks (k_c 103 for the source, k_c 111 for the result, k_c 95 as the second refusal of the source in the place of the k_c 87 check), the scan lists, and the gate level 22000 to 25000 MiB. dh170's k_c 111 driver differs from his k_c 103 one only in the source and target k_c and in the cap (8 h).
1. Pins; selftests of the k_c 103, k_c 111 and k_c 95 checks (exit 0); the source: `kc103_syscheck_1025.py` exit 0 on state and record, `--mutate=F` and `--mutate=steps` exit 1, the k_c 111 and k_c 95 checks exit 1 on the source.
2. Regrid, in `solver/matter`, 6 threads, nice 10, cap 43200 s (12 h, as at k_c 103; dh170's was 8 h): `ell_refine.py l1kc103dh370d2225 103 l1kc111dh370d2225 111 1 22.25 2.1019003706 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`. ACCEPTED only when `kc111_syscheck_1025.py` exits 0 on the result, `--mutate=F` and `--mutate=steps` exit 1, and `kc103_syscheck_1025.py` exits 1 on the result.
3. Scan, `d18_hybsign.py` on the accepted state: lambda 0.02, 0.06, ..., 0.50 (13 values) and the repeat of 0.14 (14 evaluations), **5 processes of 1 thread**, nice 10, 3 rounds (5, 5, 4): p0 0.06, 0.14, 0.34; p1 0.02, 0.18, 0.38; p2 0.42, 0.22, 0.50; p3 0.46, 0.26, 0.14 (the repeat); p4 0.10, 0.30. **Round 1 holds the brackets that decide P against S and the F bracket:** 0.02, 0.06, 0.10 and 0.42, 0.46; the repeat is on another process than its first. Memory gate before the scan (as at k_c 103): MemAvailable at least 25000 MiB (5 x 4.4 GiB + 3 GiB; dh170's k_c 111 points peaked at about 4.3 GiB), at most 6 h of waiting, nothing killed.
4. Reading: `read_lower.py selftest` (0) and its mutations `shift`, `round2` (1 each), `read_lower.py scan 0.02 0.50`, `repeat_check.py`. A change is placed only to a 0.04-wide bracket; the det-linear estimate and its range are crude (a spread over interpolation choices, not an enclosure); two roots inside one interval cancel. No widening.

## Acceptance (fixed before the run)
As at k_c 103: source accepted with controls 1 1 and refused by the k_c 111 and k_c 95 checks; regrid exits 0 inside 43200 s; the result accepted by the k_c 111 check with both controls exit 1 and refused by the k_c 103 check; every scan process prints the record system and exits 0; the repeat of 0.14 agrees. A control that fires, an exception or a refusal stops the work and I report it; no bar is loosened.

## Predictions, registered before the runs
**t5's:** **(P) parity:** no root in 0.02 to 0.30 and one root near 0.43 to 0.46 (F). **(S) S is physical and converging:** a root below 0.06 again, plus F.
How I read them on the 0.04 grid, fixed here: **P** = no robust change with a bracket inside (0.02, 0.30) and one robust change whose bracket is (0.42, 0.46) (the interval holding 0.43 to 0.46); **S** = a robust change with bracket (0.02, 0.06) plus the F change in (0.42, 0.46); anything else (a root elsewhere, a second F, F outside (0.42, 0.46), a non-robust point touching a change) is neither and is reported as read, with every robust change's printed orientation. Not decided by this scan: **a root of S below 0.02 would look like P** (no change in the window, the sign at 0.02 equal to the sign at 0.06); S moved from 0.108 (k_c 87) to 0.0596 (k_c 103), so k_c 111 could be near 0.03 or lower. I propose to t5 one more evaluation, lambda 0.01, which fits in round 3's free slot (process 4 has two points) at no extra wall time; it is **not in the order and is not run unless t5 agrees** (it would be added to `stage.conf` before the scan starts, in about 3 h).
**Mine (information, not pass rules):**
- Source accepted with controls 1 1, refused by the k_c 111 and k_c 95 checks: 90%. Regrid exits 0 and is accepted (both controls exit 1, the k_c 103 check refusing): 85%.
- Steps: dh170's k_c 103 to 111 ratio at D 21.125 was 1.0765 (3476 to 3742), so about 3652 for my 3392 (within 30: 60%). |F| below 1e-9: 90%. Delta(111) - Delta(103) between -2e-5 and -1e-7: 65%. Regrid wall 8000 to 14000 s (60%: dh170's k_c 103 to 111 took 9622 s on 8 threads against 7305 s for 95 to 103, a factor 1.32; my k_c 103 regrid took 7173 s on 6 threads, so about 9500 s). Peak RSS of the regrid below 4.5 GiB: 80% (dh170: 3.44 GiB).
- Scan: every point noise-robust 70%; the repeat bit-identical 85%. **P 55%, S 20%, neither 25%** (P: dh170 saw the printed orientation flip between k_c 103 and 111 at D 21.125, the pattern of 95 against 87 and 103, which suggests a k_c-parity effect; I do not know that the S root follows it). F in (0.42, 0.46) with printed orientation '- to +' (the k_c 95 form) 60% if P, '+ to -' (the k_c 87 and 103 form) 60% if S. The float64 sign differs from the hybrid at some point: 85%. Scan wall 6 to 10 h from its start (60%): points about 10000 to 11000 s on 5 processes (my k_c 103 ones took 7679 to 8266 s; dh170's k_c 111 ones were 1.29 times his k_c 103 ones), the last round on 4 processes about 7000 s.
- Load: the regrid takes 6 threads at nice 10, the walk d (#1080) about 1.3 cores, and t5's `i1088a` units; t5's rule: alert only on a kill.

## Status
- 2026-11-25 17:37 UTC: folder, inputs, drivers, dry run (pins, worktree, lambda_0 pass) and this README written before any run; the unit `i1025k111` starts next.
- 2026-11-25 17:38:10 to 17:38:24 UTC: unit `i1025k111` started. Selftests of the k_c 103, k_c 111 and k_c 95 checks exit 0 0 0. **Source check accepted:** `kc103_syscheck_1025.py` exit 0 on my state and record, `--mutate=F` and `--mutate=steps` exit 1, the k_c 111 and k_c 95 checks exit 1 on the source (`source_*.txt`). **Regrid started 17:38:24 UTC** (6 threads, nice 10, cap 43200 s), load 2.7, MemAvailable 28.0 GB.

## Amendment 1 (t5's hc, 2026-11-25 after 17:38 UTC; recorded at 17:40 UTC before the scan, the regrid being under way)
"Yes, add lambda 0.01 as the 15th evaluation, and also -0.03 if a slot is free (S's trend 0.108 -> 0.060 per 16 in k_c would put it near 0.01 at k_c 111). Register: a change in (-0.03, 0.02) means S persisted and moved, not parity."
- **lambda 0.01 is added** as the 15th evaluation, in round 3's free slot (process 4: 0.10, 0.30, 0.01), so the scan is 15 evaluations on 5 processes in 3 rounds of 5 with no extra wall time (`stage.conf`; the reader's window is 0.01 to 0.50). `d18_hybsign.py` takes any float lambda; the two ends of the window now are 0.01 and 0.50.
- **lambda -0.03 does not fit a free slot:** the 5 processes are full after 0.01 (15 = 3 x 5). Run on process 4 after 0.01 it would add a 4th round of one point, about 1.4 to 2 h at the end beside a nearly idle machine; I have asked t5 and **do not add it unless t5 says so** (it can also be run after the scan, on the accepted state, as its own job). `d18_hybsign.py` evaluates `S.mode_matrix(z, lam)` for any float lambda; a negative lambda has not been run here.
- **Registered reading of t5's addition:** with 0.01 and 0.02 evaluated, a robust change with bracket (0.01, 0.02) means S persisted and moved below 0.02 (not parity, in t5's reading). A change in (-0.03, 0.01) can be seen only if -0.03 is evaluated; without it, no change in (0.01, 0.50) together with equal signs at 0.01 and 0.02 leaves P and "S below 0.01" undecided, and I say so.
- P and S as registered above stand: P = no robust change in (0.01, 0.30) and one in (0.42, 0.46); S = a robust change with bracket (0.02, 0.06), or one in (0.01, 0.02), plus the F change in (0.42, 0.46). "Neither" is reported as read.
- **t5's answer on -0.03 (hc, 2026-11-25 about 17:40 UTC):** "add -0.03 as its own job after the scan, on the accepted state (win2 ran negative lambda through d18_hybsign at D 22.28125 without trouble). Only if 0.01 and 0.02 leave it undecided." So: after the scan ends, **if the scan shows no robust change in (0.01, 0.30) and equal hybrid signs at 0.01 and 0.02** (P and "S below 0.01" undecided), I run lambda -0.03 alone on the accepted state (`d18_hybsign.py`, 1 process, nice 10, its own unit, README first with the reading: a robust change in (-0.03, 0.01) means S persisted and moved). If the scan shows a change in (0.01, 0.30), S is decided and -0.03 is not run.

## Amendment 2: the i1088a yield rule (t5's hc, 2026-11-25 about 17:41 UTC; recorded before the unit starts)
"Another session (t2t) now runs a job of its own on dh370 (4 threads, CPUs 8-11, ~3.5 h). The quest's D 10^4 solve may also land on dh370 soon (i1088a units). Add dh610's rule to your k_c 111 lane: renice its compute processes to 19 by exact pid whenever an i1088a unit is active (alert-only, nothing stopped)."
- `yield_i1088a.sh` (unit `i1025k111y`, ends with the lane's unit `i1025k111`): every 30 s, if a systemd user unit `i1088a-*` is active, it raises to 19 the nice value of the lane's compute processes (python of `ell_refine.py l1kc103dh370d2225` in the regrid, python of `d18_hybsign.py ... l1kc111dh370d2225` in the scan, and their `timeout` / `time` wrappers) by exact pid, and logs one line per change to `i1088a_yield.txt`. It only raises, stops and kills nothing, and does not message t5 (the session reports its log).
- **A difference from dh610's script, with the reason:** it raises **every thread** of the process, not only the pid. On Linux a nice value is per thread, so `renice -n 19 -p PID` alone changes only the main thread: the regrid's 6 BLAS threads would stay at nice 10. Tested on a dummy 4-thread python at nice 10 (`renice_threads.sh`): by PID alone, nice 19 10 10 10 (the control); with the script, 19 19 19 19; a second call changes nothing. The watcher itself was tested with a fake-active switch: with no i1088a unit active nothing changes (control), with it forced the dummy's four threads go to 19 and one log line is written. The test also showed that a process match on the command text catches a shell whose command line contains the pattern; the script now acts only on `python*`, `timeout` and `time` processes.
- The walk d (#1080) and t2t's job are not touched. The scan processes and the regrid are already at nice 10; 19 is the lowest priority the kernel gives. Not in the order: nothing lowers the nice value back when the i1088a unit ends (an unprivileged user cannot), so a lane process reniced once stays at 19 for the rest of its life.

## Regrid result (25 Nov, 17:38:24 to 21:12:04 UTC): ACCEPTED
`ell_refine.py` (6 threads, nice 10, from 18:01:01 UTC at nice 19 on every thread by the yield rule while t5's `i1088a-L2828` ran) exited 0 after **12820 s** (the record's 12818 s); mean sampled CPU 554% (212 samples, `regrid_samples.csv`), peak sampled RSS **3.46 GiB**; 28 numpy RuntimeWarning lines in the log, as in the earlier regrids; MemAvailable stayed above 20 GB, no alert.
- Record `l1kc111dh370d2225.jsonl` (blob 06dc9d92) and state `sol_l1kc111dh370d2225_D22.2500.npy` (blob 7fc75ef8): k_c 111 at D 22.25, |F| **4.0650557270e-10** (my k_c 103: 4.0298416048e-10), F_start 1.266e-05, **3657 steps** (k_c 103: 3392; ratio 1.0781), constraint **1.924e-03** (k_c 103: 2.928e-03), **Delta 1.152660251704** (k_c 103: 1.152663118278; shift **-2.867e-06**).
- **Acceptance:** `kc111_syscheck_1025.py` exit 0 (the state's |F| equals the record's, `freeze_from` gives 3657 steps = the record's); `--mutate=F` exit 1, `--mutate=steps` exit 1; `kc103_syscheck_1025.py` on the k_c 111 result exit 1 (refuses it). Source check (17:38:24): k_c 103 check exit 0, controls 1 1, the k_c 111 and k_c 95 checks refuse it. The memory gate passed at once (MemAvailable 27.5 GB); the scan started **21:12:25 UTC**, 15 evaluations, 5 processes; all five printed the record system (|F| 4.0647893555e-10 against the record's 4.0650557270e-10, 3657 steps equal), at nice 19 from their start (the yield rule, `i1088a_yield.txt`).

### Regrid predictions scorecard (mine, registered before the run)
| prediction | result |
|---|---|
| source accepted, controls 1 1, k_c 111 and k_c 95 checks refuse it (90%); regrid accepted (85%) | right; right |
| steps about 3652 (within 30: 60%) | right (3657) |
| \|F\| below 1e-9 (90%) | right (4.07e-10) |
| Delta(111) - Delta(103) between -2e-5 and -1e-7 (65%) | right (-2.87e-6) |
| regrid wall 8000 to 14000 s (60%) | right (12820 s; slower than my 9500 s point estimate because the nice-19 yield beside t5's job began at 18:01) |
| peak RSS below 4.5 GiB (80%) | right (3.46 GiB) |

## Scan, round 1 done (21:12:25 to about 00:55 UTC, 5 processes at nice 19, 12712 to 13390 s per point)
| lambda | hybrid sign | noise-robust | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.02 | + | True | + | -3372.2335 | 13145 |
| 0.06 | + | True | + | -3376.4680 | 12742 |
| 0.10 | + | True | + | -3380.7154 | 12988 |
| 0.42 | + | True | - | -3417.8304 | 12712 |
| 0.46 | - | True | - | -3420.093 | 13390 |
- Interim (information; the reader's reading comes after the scan): the hybrid signs are **equal (+) at 0.02, 0.06 and 0.10**, so there is **no sign change in (0.02, 0.10)**: S as at k_c 103 ((0.02, 0.06), "- to +") is absent there. There is **a "+ to -" change in (0.42, 0.46)** (F by position; the printed orientation equals that of k_c 87 and 103 at this D, not k_c 95's "- to +"). P against S is **not yet decided**: a root in (0.01, 0.02) shows only at lambda 0.01 (round 3, process 4), and the points 0.14 to 0.38 and 0.50 are still to come. Per point 12712 to 13390 s (3.5 to 3.7 h at nice 19 beside t5's `i1088a` job and t2t's); rounds 2 and 3 should end about 04:40 and 08:00 UTC.

## Scan, round 2 done (about 00:55 to 03:45 UTC, 5 processes at nice 19, 9468 to 10304 s per point; walk d had been stopped at 01:57)
| lambda | hybrid sign | noise-robust | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.14 | + | True | + | -3384.9784 | 10304 |
| 0.18 | + | True | + | -3389.2610 | 9989 |
| 0.22 | + | True | + | -3393.5702 | 10094 |
| 0.26 | + | True | + | -3397.9169 | 9468 |
| 0.30 | + | True | + | -3402.3220 | 9925 |
- Interim (information; the reader's reading comes after the scan): with round 1, the hybrid sign is **+ at every evaluated lambda from 0.02 to 0.30 (8 values, all noise-robust)**, + at 0.42 and - at 0.46: no sign change in (0.02, 0.30), and the change in (0.42, 0.46) is "+ to -". Round 3 (0.34, 0.38, 0.50, the repeat of 0.14, and **0.01**) is running and should end about 06:30 to 07:00 UTC. Against the registration: P is consistent so far; what can still decide against it is the sign at 0.01 (a change in (0.01, 0.02) means S persisted and moved) and a change in 0.30 to 0.42 from 0.34 and 0.38.

## Scan result (25 Nov 21:12:25 to 26 Nov 05:48:48 UTC = 8.6 h; 5 processes at nice 19 from the start; `read_lower.txt`, `merged_D22.25.jsonl`)
All five processes printed the record system (|F| 4.0647893555e-10 against the record's 4.0650557270e-10, 3657 steps equal) and exited 0; 15 evaluations, **15 noise-robust**. `read_lower.py` selftest exit 0, mutations `shift` and `round2` exit 1; `repeat_check.py` PASS (the repeat of 0.14 on process 3 against the first on process 0: ln|det| -3384.9783764089902 in both, bit-identical).
| lambda | hybrid sign | noise-robust | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.01 | + | True | + | -3371.1766 | 7982 |
| 0.02 | + | True | + | -3372.2335 | 13145 |
| 0.06 | + | True | + | -3376.4680 | 12742 |
| 0.10 | + | True | + | -3380.7154 | 12988 |
| 0.14 | + | True | + | -3384.9784 | 7973 (repeat) and 10304 |
| 0.18 | + | True | + | -3389.2611 | 9989 |
| 0.22 | + | True | + | -3393.5702 | 10094 |
| 0.26 | + | True | + | -3397.9169 | 9468 |
| 0.30 | + | True | + | -3402.3220 | 9925 |
| 0.34 | + | True | + | -3406.8321 | 7915 |
| 0.38 | + | True | + | -3411.5865 | 7814 |
| 0.42 | + | True | - | -3417.8304 | 12712 |
| 0.46 | - | True | - | -3420.0932 | 13390 |
| 0.50 | - | True | - | -3423.4337 | 7890 |
**One robust change in the window 0.01 to 0.50** (the reader's output, orientation as printed; the det-linear estimate and its range are a spread over interpolation choices on a coarse grid, **not an enclosure**; the bracket is the grid step): **(0.420, 0.460), "+ to -", det-linear 0.456230, range [0.420156, 0.456230]**. Edge signs + at 0.010 and - at 0.500; no ln|det| minimum without a sign change; no change touches a non-robust point. The float64 sign differs from the hybrid at 0.42 only (not used). Peak RSS per process 4.29 to 4.43 GiB (`/usr/bin/time -v`); per-process wall 8:31:56 to 8:36:23; points 12712 to 13390 s in round 1, 9468 to 10304 s in round 2 (after walk d was stopped at 01:57), 7814 to 7982 s in round 3.

### Against t5's registered P and S (my reading, fixed above before the run)
- **P (parity): no robust change inside (0.01, 0.30) and one with bracket (0.42, 0.46): met on the evaluated points.** The hybrid sign is the same (+) at all 12 evaluated lambda from 0.01 to 0.38 and at 0.42, so there is no change in (0.01, 0.42); the one change is (0.420, 0.460).
- **S (a change with bracket (0.02, 0.06), or one in (0.01, 0.02), plus F): not met.** The sign at 0.01 equals the sign at 0.02, and 0.02 equals 0.06; S as at k_c 103 ((0.02, 0.06), "- to +") is absent, and S has not "persisted and moved" into (0.01, 0.02).
- **Not decided by the scan: P against an S root below 0.01** (lambda in (-0.03, 0.01), out of reach of the evaluated points). Per t5's ruling, lambda -0.03 now runs as its own job (below).
- **The printed orientation of F** by k_c at D 22.25, as the reader prints it (information, not interpreted): k_c 87 "+ to -" (macm3), k_c 95 "- to +" (dh610), k_c 103 "+ to -", **k_c 111 "+ to -"**. The pairing I registered (F "- to +" if P, "+ to -" if S) is **WRONG**: F prints "+ to -" at k_c 111 with S absent. The det-linear estimate of F at k_c 111, 0.456230, equals that of k_c 103 (0.455342) within the crude estimator (the two brackets are the same).

### Scan predictions scorecard (mine, registered before the run)
| prediction | result |
|---|---|
| every point noise-robust (70%); the repeat bit-identical (85%) | right (15 of 15); right |
| P 55%, S 20%, neither 25% | P on the evaluated points (undecided against an S root below 0.01, pending -0.03) |
| F printed "- to +" 60% if P, "+ to -" 60% if S | WRONG: "+ to -" with S absent |
| the float64 sign differs from the hybrid at some point (85%) | right (at 0.42) |
| scan 6 to 10 h from its start (60%) | right (8.6 h) |
| points about 10000 to 11000 s on 5 processes | partly: 7814 to 13390 s (13000 s in round 1 at nice 19 beside two other jobs, 8000 s in round 3) |

## lambda -0.03 (t5's ruling, condition met)
The condition written above is met: **no robust change in (0.01, 0.30), and equal hybrid signs at 0.01 and 0.02** (both +). So **lambda -0.03 runs now as its own job on the accepted state** (`run_neg003.sh`, unit `i1025k111n`): `d18_hybsign.py` (e089207a, unmodified) on state 7fc75ef8 and record 06dc9d92, 1 process of 1 thread, nice 10 (the yield rule follows it: `i1025k111ny`), output `scan/scan_D22.25_pneg003.jsonl`; then `read_lower.py scan -0.03 0.50` (`read_lower_neg003.txt`). **Registered reading:** the hybrid sign at -0.03 against the sign at 0.01 (+): **a different sign means a robust change in (-0.03, 0.01), S persisted and moved (t5's rule: not parity)**; the same sign leaves "no root in (-0.03, 0.50 up to F)", P stands, and a root below -0.03 stays outside what was measured. If the point is not noise-robust the reader's rule applies and I report it as such. Estimate (mine): 1 point alone, 4000 to 8000 s (the k_c 111 points took 7814 to 7982 s on 4 to 5 processes).

## Amendment 3: the yield rule stands for the -0.03 job (t5's hc, 2026-11-26 about 06:20 UTC; logged 05:56 UTC by dh370's clock)
t5: "The yield rule stands. #1088's units come first on every machine, so re-arm i1025k111ny for the -0.03 job now. ... By 'do not renice or stop it' I meant: no change to that job as part of the new lane. I did not mean to turn off the yield rule. Log both in the READMEs."
- At 05:53 UTC I had stopped the watcher unit `i1025k111ny` (the -0.03 job's yield rule) to follow "do not renice or stop it" in t5's order for the k_c 119 lane, and told t5 so. The job itself (unit `i1025k111n`, pid 2726378) was not touched and ran at nice 10; no `i1088a` unit was active in that interval (05:53 to 05:56), so no renice was missed.
- **Re-armed at 05:56:49 UTC:** unit `i1025k111ny` runs `yield_i1088a.sh` again with `YIELD_UNIT=i1025k111n` (it follows the -0.03 job's unit); the rule is unchanged (README amendment 2 above): every thread of the job's python and its `time` wrapper to nice 19 while an `i1088a-*` unit is active, one log line per change in `i1088a_yield.txt`, nothing stopped or killed.

## lambda -0.03 result (26 Nov, 05:49:48 to 06:53:38 UTC; unit `i1025k111n`, 1 process, nice 10, 3830 s alone; `read_lower_neg003.txt`)
`lam -0.030: hybrid +1 ln|det| -3366.9557 (noise robust True), float64 +1, 3824 s`; the process printed the record system (|F| 4.0647893555e-10 against the record's 4.0650557270e-10, 3657 steps equal), exit 0, peak RSS 3.33 GiB (3493932 kB), wall 1:03:49. No `i1088a` unit was active during the job, so the yield rule reniced nothing.
- The hybrid sign at -0.03 (+) **equals** the sign at 0.01 (+), so **no change in (-0.03, 0.01)**, and with the scan **no change in (-0.03, 0.42)**. The reader on the window -0.03 to 0.50: 15 points, all noise-robust; hybrid signs + at -0.030, 0.010, 0.020, 0.060, ..., 0.420, - at 0.460 and 0.500; **one robust change, (0.420, 0.460), "+ to -", det-linear 0.456230, range [0.420156, 0.456230]**; no ln|det| minimum without a sign change; the float64 sign differs from the hybrid at 0.42 only; the repeat of 0.14 agrees.
- **Against t5's rule** ("a change in (-0.03, 0.02) means S persisted and moved, not parity"): **there is none.** S, the root at 0.108 (k_c 87) and 0.0596 (k_c 103) at this D, is absent at k_c 111 from (-0.03, 0.42). That is **(P)** on the evaluated points, as at k_c 95 (none in 0.02 to 0.82, dh610). An S root below -0.03 is not excluded by anything measured here. The determinant's overall sign is not compared across k_c.
- By k_c at D 22.25 (by position; orientation as printed): the lower root S: k_c 87 yes (0.108, "- to +"), k_c 95 none, k_c 103 yes (0.0596, "- to +"), **k_c 111 none** (in -0.03 to 0.42); the upper root F: k_c 87 0.442516 "+ to -", k_c 95 0.434264 "- to +", k_c 103 0.455342 "+ to -", **k_c 111 0.456230 "+ to -"** (det-linear, a crude estimator on a 0.04 grid, not an enclosure).
