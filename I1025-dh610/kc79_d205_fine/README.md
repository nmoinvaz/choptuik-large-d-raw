# I1025-dh610/kc79_d205_fine: dh170's k_c 79 D 20.5 state on this build, scanned at lambda 1.060 to 1.090 by 0.005 (the fine grid), against this machine's k_c 87 root 1.077872 and dh170's coarse 1.087574

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 16:17 UTC, before any run of this folder. The k_c 79 and k_c 87 roots are not yet physical.

## Order (coordinator t5, hc, after `../kc87_d205`, raw 2514221e), in part
"D 20.5 k_c 87 accepted as read (raw 2514221e): 1.077872, and your post-hoc reading is right: the 0.0097 compares a 0.03 grid with a 0.005 one. Go on your proposal: dh170's k_c 79 D 20.5 state (30a92b78, record 5406e21c) on your build, kc79 check first (controls exit 1), d18_hybsign at 1.060-1.090 by 0.005 (7 evals, 5 procs; 1.060 and 1.090 again too, as repeats of dh170's on another build), read_lower. Written before (README): the k_c 79 root on the fine grid lies within 0.002 of 1.077872 (k_c 87), and the coarse two-point estimate is 0.010 high for this state, as you found. Raw I1025-dh610/kc79_d205_fine/."
Memory alerts only (standing rule). "7 evals" is read as the seven grid values 1.060, 1.065, ..., 1.090; 1.060 and 1.090 are the two lambdas dh170 evaluated on this state (`in/ref_dh170_k79_scan_D20.5.jsonl`: both noise-robust, signs - and +, ln|det| -2388.144894 and -2390.575506), so they are the repeats of his rows on this build. If t5 meant seven more evaluations beside those two, say so and I add them.

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs; the lane refuses any other blob)
| item | blob |
|---|---|
| dh170's k_c 79 D 20.5 state `sol_l1kc79dh170d205_D20.5000.npy` and record `l1kc79dh170d205.jsonl` (`I1025-dh170/kc79_d205`, raw 9535a78a; the same files as `../kc87_d205/in`) | 30a92b78, 5406e21c |
| `kc79_syscheck_1025.py` | 29dce7ea |
| `d18_hybsign.py` (xfkappa's, unmodified), `read_lower.py`, `d185_scan_read.py`, `d18c_read.py`, `repeat_check.py` | e089207a, 89309d3c, 7c9d400f, 1383470f, aaf598a9 |
| dh170's final k_c 79 reading and rows (`dh170_k79_read_lower.txt`, `ref_dh170_k79_scan_D20.5.jsonl`, raw 249571b8) | 317b8f61, b68c0f6d |
| this machine's k_c 87 reading and rows of `../kc87_d205` (raw 2514221e) | 493c7401, c96a65da |
| `rows_check.py` (mine: this machine's rows at 1.060 and 1.090 against dh170's, sign equal and ln|det| within 1e-9 relative, the bar of `../kc79_d195/in/control_check.py`; selftest exit 0, `--mutate` exit 1; run on the k_c 87 rows against dh170's k_c 79 rows it fails, as it must) | b26817b5 |
| `fine_read.py` (mine: the scan's change beside the k_c 87 root 1.077872 by position, bar 0.002, and beside dh170's 1.087574; selftest exit 0, `--mutate` exit 1) | 4fd1fd24 |
Code: `d18_hybsign.py` in `~/Source/choptuik-large-d-1025f` at 505d8399; the k_c 79 check reads the worktree `~/Source/choptuik-large-d-1025g` at 48c36355; python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0 avx2).

## Commands (`lane_kc79_d205_fine.sh` via `start_kc79_d205_fine.sh` = systemd user unit i1025ai under `systemd-inhibit` with the alert-only memory log; each step stops the lane when it fails; `notify_kc79_fine.sh` sends the coordinator an hc line at the source check and the end)
1. Pins and the tools' controls: selftests of `kc79_syscheck_1025.py` (exit 0), `read_lower.py` and its two mutations (0 1 1), `fine_read.py` (0, `--mutate` 1), `rows_check.py` (0, `--mutate` 1).
2. The source: `kc79_syscheck_1025.py` on dh170's record and state at D 20.5 accepts it (exit 0; `--mutate=F` and `--mutate=steps` exit 1). It already did so on 23 Nov at 13:39 UTC (`../kc87_d205/regrid/source_kc79_syscheck*.txt`); this folder runs it again as ordered.
3. The scan: `d18_hybsign.py` at 1.060 to 1.090 by 0.005 (7 evaluations), 5 processes of 1 thread, nice 10: p0 1.060, 1.085; p1 1.090, 1.065; p2 1.070; p3 1.075; p4 1.080 (1.060 and 1.090 in round 1). Each process prints the record system first (exit 3 if not). Refuses to start with less than 5 x 2.5 GB + 4 GB free.
4. The reading: `read_lower.py scan 1.060 1.090`, `fine_read.py`, and `rows_check.py` (1.060 and 1.090 against dh170's rows).
Threads: 5 beside the #1076 recount's up to 12 (`../../I1021-dh610/fu022mp_m3mp`), 17 at most, all at nice 10.

## Acceptance (fixed before the run)
- The k_c 79 check accepts the state with both controls exit 1; every scan process prints the record system; `rows_check.py` passes at 1.060 and 1.090 (a failing control stops the work and I report it; no bar is loosened).
- Reported: every robust change by position with bracket, orientation as printed, det-linear and range, beside this machine's k_c 87 root (1.077872) and dh170's 1.087574; the edge signs; ln|det| minima without a sign change; the rows at 1.060 and 1.090 beside dh170's (bit-identical or not); the coarse two-point estimate from this build's rows at 1.060 and 1.090.
- The coordinator's reading: the k_c 79 root on the fine grid lies within 0.002 of 1.077872 (k_c 87), and the coarse two-point estimate is 0.010 high for this state.

## Predictions, registered before the run (mine, information)
- The k_c 79 check accepts the state with both controls exit 1 (97%); all five processes exit 0 with the record system (92%).
- The rows at 1.060 and 1.090 have the same sign as dh170's (98%) and ln|det| within 1e-9 relative (90%), bit-identical (85%); the coarse two-point estimate from them is 1.087574 to 1e-6 (88%).
- Exactly one robust change in 1.060 to 1.090 (92%; the edge signs - and + differ); it lies within 0.002 of 1.077872 (55%, the coordinator's reading), within 0.001 (35%), within 0.005 (80%). The k_c 79 root minus the k_c 87 one is between -0.002 and +0.003 (60%). The coarse estimate minus the fine k_c 79 root is 0.010 +- 0.002 (55%).
- Each scan point takes 800 to 1700 s (65%; k_c 79 at D 20.25 took 699 to 1800 s); the lane ends 17:10 to 17:50 UTC (two rounds on p0 and p1).

## Status
- 2026-11-23 16:17 UTC: folder, inputs, lane and the reading prepared before any run; dry run of the lane passed (16:16:41 UTC; pins, selftests 0 0 1 1 0 1 0 1).
- 2026-11-23 16:16:51 UTC: lane started (unit i1025ai); source check 16:17:10 (ACCEPTED); scan 16:17:10 to 16:52:14 UTC; lane exit 0 (`exits_kc79_d205_fine.txt`). The order's "7 evals" was read as the seven grid values (1.060 and 1.090 being dh170's two lambdas); t5 did not object by 16:52.

## Result (`summarize_fine.py` > `summary_fine.txt` prints the tables from the files; its control and `--mutate` are described in its docstring)

| lambda | hybrid sign (this build k_c 79, dh170 k_c 79, this build k_c 87) | noise signs (robust) | float64 sign | ln of abs det (this build k_c 79, dh170 k_c 79) | seconds |
|---|---|---|---|---|---|
| 1.060 | -, -, - | -- (True) | - | -2388.1448941613307, -2388.1448941613307 | 1205 |
| 1.065 | -, n/a, - | -- (True) | - | -2388.83942149182, n/a | 889 |
| 1.070 | -, n/a, - | -- (True) | - | -2389.7144772346082, n/a | 1203 |
| 1.075 | -, n/a, - | -- (True) | + | -2391.2221684074034, n/a | 1193 |
| 1.080 | +, n/a, + | ++ (True) | + | -2391.417485918185, n/a | 1196 |
| 1.085 | +, n/a, + | ++ (True) | + | -2390.722431641437, n/a | 897 |
| 1.090 | +, +, + | ++ (True) | + | -2390.5755060955885, -2390.5755060955885 | 1194 |

scan points: 7 evaluations, seconds per point min 889, median 1194, max 1205, sum 7777; outside 800 to 1700 s: []

control: the two-point root of dh170's rows at 1.06 and 1.09 is 1.087574; his reader's det-linear is 1.087574; difference -3.91e-08 (bar 1e-5): ok
two-point root of this build's k_c 79 rows at 1.06 and 1.09: 1.087574 (minus dh170's reader -3.91e-08)
this scan's reader (0.005 grid, k_c 79): det-linear 1.077743; this machine's k_c 87 (0.005 grid, ../kc87_d205): 1.077872; k_c 79 minus k_c 87 -0.000129
coarse (0.03 grid) minus fine, k_c 79: +0.009831; k_c 87: +0.010167 (the k_c 87 rows' two-point value 1.088039)

=== (printed) read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_d205_fine/scan 1.060 1.090
points 7 in 1.060-1.090; not noise-robust: none
hybrid signs: 1.060- 1.065- 1.070- 1.075- 1.080+ 1.085+ 1.090+
float64 sign differs from the hybrid sign at: [(1.075, '-', '+')]
repeated points: none
  robust change (1.075, 1.080), - to +, det-linear 1.077743, range [1.077173, 1.077743]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: - at 1.060, + at 1.090
read_lower exit 0

hybrid signs: 1.060- 1.065- 1.070- 1.075- 1.080+ 1.085+ 1.090+
robust changes: 1
   change (1.075, 1.080), - to +, det-linear 1.077743, range [1.077173, 1.077743]
against this machine's k_c 87 root 1.077872: k_c 79 (fine grid) minus k_c 87 = -0.000129; within 0.002: True
against dh170's coarse two-point estimate 1.087574 (0.03 grid, bracket (1.060, 1.090)): fine grid minus coarse = -0.009831

```
PASS: lambda 1.06: sign -1 (dh170 -1), ln|det| -2388.1448941613307 (dh170 -2388.1448941613307), relative difference 0.000e+00 (bar 1e-09), bit-identical ln True, noise [-1.0, -1.0] (dh170 [-1.0, -1.0]), float64 sign -1 ln -2388.405611311015 (dh170 -1, -2388.405611311015)
PASS: lambda 1.09: sign +1 (dh170 +1), ln|det| -2390.5755060955885 (dh170 -2390.5755060955885), relative difference 0.000e+00 (bar 1e-09), bit-identical ln True, noise [1.0, 1.0] (dh170 [1.0, 1.0]), float64 sign +1 ln -2389.7024670931187 (dh170 +1, -2389.7024670931187)
```

### Reading (by position; orientation as the reader prints it; "robust change" is a sign change of the hybrid determinant between two grid points, not yet a physical root)

- **Acceptance held.** `kc79_syscheck_1025.py` exit 0 on dh170's state and record at D 20.5 (state |F| 4.6780067895e-10 against the record's 4.6763736498e-10, 2731 steps = the record's), `--mutate=F` 1, `--mutate=steps` 1. All five scan processes printed "the record system" (|F| 4.6786148313e-10, 2731 steps).
- **The rows at 1.060 and 1.090 are dh170's, bit for bit:** same hybrid signs, ln|det| bit-identical (-2388.1448941613307 and -2390.5755060955885), the noise signs and the float64 sign and ln the same (`rows_check.txt`, exit 0). The two machines (i7-7700 and i7-12700) and the two builds evaluate this state identically again.
- **One robust change in 1.060 to 1.090:** (1.075, 1.080), "- to +", det-linear 1.077743, estimator range [1.077173, 1.077743] (a spread over interpolation choices, not an enclosure). Hybrid signs: - at 1.060 to 1.075, + at 1.080 to 1.090. The float64 sign reads + at 1.075 where the hybrid reads -; the hybrid is the sign read.
- **k_c 79 against k_c 87 at D 20.5, both on the 0.005 grid:** 1.077743 against 1.077872, k_c 79 minus k_c 87 = -0.000129 (within the coordinator's 0.002, and within 0.001). The k_c 87 state is a regrid of this k_c 79 state (`../kc87_d205`).
- **The coarse estimate:** the two-point estimate on the 0.03 grid (this build's rows at 1.06 and 1.09) is 1.087574, dh170's number, to 4e-08 (the rows are bit-identical; the formula's control and its `--mutate` are in `summarize_fine.py`). Coarse minus fine is +0.009831 for k_c 79 and +0.010167 for k_c 87: the coarse estimate is 0.010 high for this state at both k_c, as found.
- **So dh170's 1.087574 and this folder's 1.077743 are the same k_c 79 state read at two grids**, and the first is the coarse-grid error of the det-linear estimate, not a difference of builds or machines.
- **The k_c 79 to 87 move of this root on equal grids** is -0.000129 here (k_c 87 higher by 0.000129); at D 20.25 here -0.000574 (k_c 87 lower), for win2 +0.000125; at D 20 for win2 -0.000856 (1.247484 against 1.248340, k_c 87 lower).

### Predictions scorecard (written before the run)

| prediction | result | verdict |
|---|---|---|
| k_c 79 check accepts, both controls exit 1 (97%); all 5 processes with the record system (92%) | accepted, 1 1; 5 of 5 | right |
| rows at 1.060 and 1.090: same sign (98%), ln within 1e-9 relative (90%), bit-identical (85%); coarse estimate 1.087574 to 1e-6 (88%) | same sign, relative difference 0, bit-identical; 1.087574 (4e-08) | right |
| exactly one robust change (92%) | one | right |
| within 0.002 of 1.077872 (55%, the coordinator's reading); within 0.001 (35%); within 0.005 (80%) | -0.000129 | right (all three) |
| k_c 79 minus k_c 87 in (-0.002, +0.003) (60%) | -0.000129 | right |
| coarse minus fine k_c 79 root 0.010 +- 0.002 (55%) | +0.009831 | right |
| each scan point 800 to 1700 s (65%) | 889 to 1205 s | right |
| the lane ends 17:10 to 17:50 UTC | ended 16:52:14 UTC | wrong (early; the points were faster than my estimate of two rounds at 1100 to 1700 s) |

The coordinator's written-before (the k_c 79 root on the fine grid within 0.002 of 1.077872, and the coarse estimate 0.010 high for this state) holds.
