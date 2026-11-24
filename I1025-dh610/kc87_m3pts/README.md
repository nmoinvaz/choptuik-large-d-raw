# I1025-dh610/kc87_m3pts: lambda_1 on four of macm3's k_c 87 leg states (D 21.5625, 21.6875, 21.8125, 21.9375), scanned on Linux

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-24 19:45 UTC, before any pin or run of this folder. The k_c 87 roots are not yet physical. A root is identified by position, never by sign orientation (printed as the reader prints it, not compared across D or k_c).

## Order (coordinator t5, hc, read at 19:43 UTC 24 Nov), verbatim
"Coordinator (t5), #1025, your freed kc79 lane takes four of macm3's unscanned k_c 87 leg states, so macm3 can keep its cores on the leap: D 21.5625, 21.6875, 21.8125 and 21.9375 (raw I1025-macm3/kc87_leg2/ part a and b, tags l1kc87Lmacm3 and l1kc87Lmacm3b; pin by blob; kc87_syscheck accepts, controls 1 1). Scan each with d18_hybsign.py, 8 procs nice 8, one at a time beside the kc95 regrid: window = prediction rounded to 0.005, +-0.015 by 0.005, plus the repeat of the centre. PREDICTIONS by linear interpolation between macm3's bracketing roots (21.5 0.744479, 21.625 0.696157, 21.75 0.646846, 21.875 0.596477): 21.5625 0.7203, 21.6875 0.6715, 21.8125 0.6217; D 21.9375 by extrapolation from 21.75/21.875: 0.5713. Bar 0.005, by position. Raw I1025-dh610/kc87_m3pts/, README first. These are also a cross-build check (macOS states, Linux scans)."

All four states are in part b (tag l1kc87Lmacm3b, `I1025-macm3/kc87_leg2/b/`; part a, tag l1kc87Lmacm3, ends at D 21.5): the lane takes them from there.

## Method (the same for every D; `lane_m3.sh D CENTER PRED`, a copy of `../kc87_leg_lambda/lane_k87l.sh` with the source and the nice level changed)
1. **Pin** by blob: `fetch_m3.sh D` takes the state `sol_l1kc87Lmacm3b_D<D:.6f>.npy` and the record `l1kc87Lmacm3b.jsonl` (it grows) from the commit that added the state, checks the blobs against git's, requires a record row of D with k_c 87, writes `<D>/in_blobs.txt` and `source_commit.txt`; the pins are pushed before the scan. The scripts are `in/` (`in_blobs.txt`): `kc87_syscheck_1025.py` 6df5d960, `kc79_syscheck_1025.py` 29dce7ea, `d18_hybsign.py` e089207a (unmodified), `read_lower.py` 89309d3c, `repeat_check.py` aaf598a9, `leg_read.py` 5cae2639, `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f (the same blobs as `../kc87_leg_lambda/`).
2. **Accept**: selftests (kc79_syscheck 0, kc87_syscheck 0, read_lower 0 and its two mutations 1 1, repeat_check 0, leg_read 0 and its mutation 1); `kc87_syscheck_1025.py` exit 0 on the state and the record row of D, `--mutate=F` and `--mutate=steps` exit 1 each, `kc79_syscheck_1025.py` on the same state exit 1 (refuses). Otherwise the lane stops and I report.
3. **Scan**: `d18_hybsign.py` at CENTER -0.015 to +0.015 by 0.005 (7 values) and a repeat of CENTER: 8 processes of 1 thread at nice 8 (p0..p6 the grid, p7 the repeat), in `~/Source/choptuik-large-d-1025f` at 505d8399, code of `~/Source/choptuik-large-d-1025g` at 48c36355 for the check, python `~/Source/venv-i1058` (3.14.10); every process must print "the record system". Memory: the chain waits (6 h cap) for 8 x 2.5 GB + 4 GB available before a point and the lane refuses below it; nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08), the sampler only writes MEMALERT.txt below 4 GiB.
4. **Read**: `read_lower.py` on the window, `repeat_check.py` on the merged rows, `leg_read.py read` against the prediction with bar 0.005. The order has no widening: no robust change is reported as read. The estimator range is a spread over interpolation choices, not an enclosure; the bracket is the 0.005 grid step; the float64 sign is information, the hybrid sign is read.
One point at a time (`chain_m3.sh`, unit `i1025-m3pts`): the chain stops at the first point whose lane does not exit 0 (a failed check or control stops the work; I report it; nothing is loosened); `exits_chain.txt`, per point `<D>/exits_k87l.txt`.

## Points (prediction = the coordinator's, rounded to the grid centre)
| D | prediction (bar 0.005) | grid centre | window | basis |
|---|---|---|---|---|
| 21.5625 | 0.7203 | 0.720 | 0.705 to 0.735 | linear between macm3's 21.5 (0.744479) and 21.625 (0.696157): 0.720318 |
| 21.6875 | 0.6715 | 0.670 | 0.655 to 0.685 | between 21.625 and 21.75 (0.646846): 0.671502 |
| 21.8125 | 0.6217 | 0.620 | 0.605 to 0.635 | between 21.75 and 21.875 (0.596477): 0.621662 |
| 21.9375 | 0.5713 | 0.570 | 0.555 to 0.585 | extrapolated from 21.75 and 21.875 (0.5 of the step -0.050369 beyond 21.875): 0.571293 |

## Acceptance (fixed before the run)
Per point: the pins equal git's blobs; the selftests as wanted; `kc87_syscheck_1025.py` accepts the state with both controls exit 1 and `kc79_syscheck_1025.py` refusing it; all 8 processes print the record system and exit 0; the repeat of the centre agrees (`repeat_check.py`). Reported per point: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction (bar 0.005); the edge signs; changes touching a non-robust point (listed, not counted); ln|det| minima without a sign change; the repeat; seconds per point, load, RSS and MemAvailable. The cross-build reading: macm3's states were made on macOS and are scanned here on Linux; their records' |F|, steps and Delta against what the Linux source check recomputes are in each `<D>/src/syscheck.txt`.

## Threads and memory (stated before)
One point at a time: 8 processes at nice 8. Beside it: the recount (12 nominal, `i1076d`) and the k_c 95 regrid (`../kc95_d2175/`, 8 threads at nice 10, running since 17:18:03 UTC; its scan, 7 processes at nice 10, follows it): 12 + 8 + 8 = 28 nominal while the regrid runs and 12 + 8 + 7 = 27 while the k_c 95 scan runs, the figure the coordinator accepted. The kc79 lanes are finished. The load alert (`../kc79_far/load_alert.sh`, alert only: load above 22 for an hour) watches.

## Predictions, registered before the runs (mine, information)
- Per point: the source is accepted with controls 1 1 and the k_c 79 check refusing it (92%; macm3's own check accepted them on macOS, and the D 21.75 state passed here); all 8 processes print the record system (92%); the repeat agrees (92%); one robust change in the window (85%), none (8%), two or more (7%).
- The interpolated points (21.5625, 21.6875, 21.8125): the root within 0.005 of the prediction (90% each), within 0.0015 (65% each). macm3's four roots have steps per 0.125 of D of -0.048322, -0.049311 and -0.050369 (second differences -0.00099 and -0.00106), so the root function is concave and the chord lies below it by about 1.2e-4 at a midpoint: I expect each root above the coordinator's prediction (65% each), near 0.7204, 0.6716 and 0.6218. The bracket: (0.720, 0.725) at 21.5625 (70%), (0.670, 0.675) at 21.6875 (80%), (0.620, 0.625) at 21.8125 (80%).
- D 21.9375 (extrapolated): the root within 0.005 of 0.5713 (80%), within 0.0015 (40%); with the steps growing by about 0.00106 per 0.125 the next step is about -0.0514 and the root near 0.5708; bracket (0.570, 0.575) (50%), (0.565, 0.570) (35%).
- The float64 sign agrees with the hybrid at all 8 evaluations at a point (20% each; it differed at one point at macm3's D 21.75, and at 1 to 3 points at nearly every kc79 leg point, at none at D 21.4375).
- Each scan point takes 1800 to 3300 s (60% each; D 21.40625's kc79 points took 2230 to 2602 s beside the regrid, D 21.4375's 3056 to 3612 s beside the regrid and a second scan; the k_c 87 states are 9% larger in steps than the k_c 79 ones, 2887 against 2642). A point is done within 60 min of its lane's start (60%). All four points are done by 23:30 UTC (55%).

## D 21.5625 (lane 19:47:05 to 21:42:14 UTC, 115.2 min; `summarize_m3.py 21.5625 0.7203` > `21.5625/summary_m3.txt`)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.705 | - | -- (True) | - | -2544.1002044461397 | 6795 |
| 0.710 | - | -- (True) | - | -2544.910105155497 | 6601 |
| 0.715 | - | -- (True) | - | -2545.99840198814 | 6091 |
| 0.720 | - | -- (True) | - | -2549.9872053514514 | 6745 |
| 0.720 | - | -- (True) | - | -2549.9872053514514 | 6850 |
| 0.725 | + | ++ (True) | + | -2546.8742385083756 | 5106 |
| 0.730 | + | ++ (True) | + | -2546.575722393425 | 5139 |
| 0.735 | + | ++ (True) | + | -2546.5747227723923 | 6596 |

scan points: 8 evaluations, seconds per point min 5106, median 6598, max 6850, sum 49923; outside 1800 to 3300 s: [(0.705, 6795), (0.71, 6601), (0.715, 6091), (0.72, 6745), (0.72, 6850), (0.725, 5106), (0.73, 5139), (0.735, 6596)]
macm3's record at D 21.5625: |F| 4.4315620456363286e-10, steps 2898, constraint 0.004796987273445795, Delta 1.133451250406673, h 0.0625, seconds 1696
float64 sign differs from the hybrid at: []

```
hybrid signs: 0.705- 0.710- 0.715- 0.720- 0.725+ 0.730+ 0.735+
robust changes: 1
   change (0.720, 0.725), - to +, det-linear 0.720213, range [0.720132, 0.720213]
against the prediction 0.7203: change minus prediction -0.000087; within 0.005: True
```

- **Source accepted** (macm3's state, commit e6e02559, 2026-11-24 07:37:53 -08:00 = 15:37:53 UTC; macOS state, Linux check): `kc87_syscheck_1025.py` exit 0 (record |F| 4.4315620456e-10, the state's own 4.4413481065e-10 recomputed here, `freeze_from` 2898 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1, `kc79_syscheck_1025.py` on it exit 1 (refuses); selftests 0 0 0 1 1 0 0 1; all 8 processes printed the record system (`21.5625/src/`, `exits_k87l.txt`).
- **One robust change in the window 0.705 to 0.735:** (0.720, 0.725), "- to +" as the reader prints it, det-linear **0.720213**, estimator range [0.720132, 0.720213] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (- at 0.705, + at 0.735). No ln|det| minimum without a sign change; every point noise-robust; the float64 sign agrees with the hybrid at all 8 evaluations.
- **The repeat of 0.720** (p3 and p7) is bit-identical (hybrid -, ln|det| -2549.9872053514514 in both; `repeat_check.py` PASS).
- **Against the prediction 0.7203 (the coordinator's chord between macm3's 21.5 and 21.625, bar 0.005):** -0.000087, within the bar and within 0.0015. The chord's exact value is 0.720318, so the root is 0.000105 below it; I had expected it about 0.00012 above (the concavity of macm3's roots), so this is the opposite side, by 2.3e-4; the estimator range of this point is 8e-5 wide and macm3's neighbours' det-linear roots carry their own interpolation spread, so one point does not separate a cross-build effect from that.
- **Seconds per point: 5106 to 6850 s** (median 6598), 2.8 times my registered bar. The k_c 95 scan of `../kc95_d2175/` (7 processes at nice 10) ran beside this one from 19:53:56 UTC (and its regrid, 8 threads, until 19:53:52), with the recount: 15 scan processes on 20 logical CPUs. The load average, median over `21.5625/scan/sampler.log` (227 samples, 19:48:03 to 21:41:47 UTC), was 17.51 (max 23.73, min 11.07), peak RSS per process 1.98 to 2.12 GiB (`/usr/bin/time -v`), MemAvailable at least 34.59 GiB; the load alert (alert only) did not fire.

### Scorecard of D 21.5625 (registered before the run)
| prediction | result |
|---|---|
| source accepted, controls 1 1, the k_c 79 check refusing it (92%); 8 processes with the record system (92%); the repeat agrees (92%) | right |
| one robust change in the window (85%) | right |
| the root within 0.005 of the prediction (90%); within 0.0015 (65%) | right (-0.000087); right |
| the root above the coordinator's prediction (65%) | WRONG (0.000087 below it) |
| the bracket is (0.720, 0.725) (70%) | right |
| the float64 sign agrees with the hybrid at all 8 evaluations (20%) | right (agrees at all 8) |
| each scan point 1800 to 3300 s (60%) | WRONG (5106 to 6850 s) |
| the point done within 60 min of its lane's start (60%) | WRONG (115.2 min) |

## D 21.6875 (lane 21:42:14 to 22:51:43 UTC, 69.5 min; `summarize_m3.py 21.6875 0.6715` > `21.6875/summary_m3.txt`)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.655 | - | -- (True) | - | -2527.0402646656753 | 3454 |
| 0.660 | - | -- (True) | - | -2527.814389770634 | 3762 |
| 0.665 | - | -- (True) | - | -2528.808988963985 | 3610 |
| 0.670 | - | -- (True) | - | -2530.830471891709 | 3656 |
| 0.670 | - | -- (True) | - | -2530.830471891709 | 4044 |
| 0.675 | + | ++ (True) | + | -2530.128154885385 | 3851 |
| 0.680 | + | ++ (True) | + | -2529.6883884437166 | 4098 |
| 0.685 | + | ++ (True) | + | -2529.6429048688046 | 4098 |

scan points: 8 evaluations, seconds per point min 3454, median 3806, max 4098, sum 30573; outside 1800 to 3300 s: [(0.655, 3454), (0.66, 3762), (0.665, 3610), (0.67, 3656), (0.67, 4044), (0.675, 3851), (0.68, 4098), (0.685, 4098)]
macm3's record at D 21.6875: |F| 4.326060038554227e-10, steps 2894, constraint 0.005209523378451233, Delta 1.1369029763526168, h 0.0625, seconds 1479
float64 sign differs from the hybrid at: []

```
hybrid signs: 0.655- 0.660- 0.665- 0.670- 0.675+ 0.680+ 0.685+
robust changes: 1
   change (0.670, 0.675), - to +, det-linear 0.671656, range [0.671141, 0.671656]
against the prediction 0.6715: change minus prediction +0.000156; within 0.005: True
```

- **Source accepted** (macm3's state, commit a00d2b34, 2026-11-24 08:18:45 -08:00 = 16:18:45 UTC; macOS state, Linux check): `kc87_syscheck_1025.py` exit 0 (record |F| 4.3260600386e-10, the state's own 4.3345125465e-10 recomputed here, `freeze_from` 2894 steps = the record's), both controls exit 1, `kc79_syscheck_1025.py` on it exit 1 (refuses); selftests 0 0 0 1 1 0 0 1; all 8 processes printed the record system.
- **One robust change in the window 0.655 to 0.685:** (0.670, 0.675), "- to +" as the reader prints it, det-linear **0.671656**, estimator range [0.671141, 0.671656] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (- at 0.655, + at 0.685). No ln|det| minimum without a sign change; every point noise-robust; the float64 sign agrees with the hybrid at all 8 evaluations. The repeat of 0.670 (p3 and p7) is bit-identical (ln|det| -2530.830471891709 in both).
- **Against the prediction 0.6715 (the coordinator's chord between macm3's 21.625 and 21.75, bar 0.005):** +0.000156, within the bar and within 0.0015; the chord's exact value is 0.671502, so the root is 0.000154 above it, on the side I expected (by 1.2e-4 from the concavity of macm3's roots). D 21.5625 sat 0.000105 below its chord: the two interpolated points fall on opposite sides, so the chord offsets are scatter of about 1.3e-4 (macm3's neighbours' own estimator ranges are 3.5e-4 to 5.5e-4 wide) and not a curvature signal.
- **Seconds per point: 3454 to 4098 s** (median 3806). Beside it from 21:42 to 22:39 UTC: the k_c 95 scan (7 processes, nice 10; this scan was reniced from nice 8 to 15 at 21:45 UTC by the coordinator's word) and the recount; after 22:39:37 UTC the recount only. The load average, median over `21.6875/scan/sampler.log` (136 samples, 21:43:20 to 22:51:10 UTC), was 13.80 (max 18.72, min 5.67; median 7.19 after the k_c 95 scan ended), peak RSS per process 1.92 to 2.19 GiB, MemAvailable at least 42.46 GiB; the load alert did not fire.

### Scorecard of D 21.6875 (registered before the run)
| prediction | result |
|---|---|
| source accepted, controls 1 1, the k_c 79 check refusing it (92%); 8 processes with the record system (92%); the repeat agrees (92%) | right |
| one robust change in the window (85%) | right |
| the root within 0.005 of the prediction (90%); within 0.0015 (65%) | right (+0.000156); right |
| the root above the coordinator's prediction (65%) | right (+0.000156) |
| the bracket is (0.670, 0.675) (80%) | right |
| the float64 sign agrees with the hybrid at all 8 evaluations (20%) | right (agrees at all 8) |
| each scan point 1800 to 3300 s (60%) | WRONG (3454 to 4098 s) |
| the point done within 60 min of its lane's start (60%) | WRONG (69.5 min) |

## Priority word of the coordinator (hc, 24 Nov, read at 2026-11-24 21:44 UTC), verbatim
"Coordinator (t5): priority to the k_c 95 scan at D 21.75 (the k_c step near the crossing matters more than the in-between k_c 87 points). Let D 21.6875's scan finish, then hold the k_c 87 lane until the k_c 95 scan has read; then 21.8125 and 21.9375 as set. Your wrong-side note on 21.5625 is fine: one point inside an 8e-5 range says nothing about builds yet."

- Done: D 21.6875's scan (started 21:42:14 UTC) runs on as it is. `wait_m3.sh` was replaced atomically (a rename; the running instance keeps the old file) by a copy that, before it takes the lock for the next point (D 21.8125), waits for a line "kc95 D 21.75 point done" or "STOP:" in `../kc95_d2175/exits_kc95.txt` (12 h cap; it writes the line "holding" once and `<D>/hold.txt`). The hold was tested on planted files (no line: holds; "point done": passes; "STOP:": passes). The chain then runs 21.8125 and 21.9375 as set (8 processes, nice 8, one at a time).
- Not done: I did not renice the running scans. The k_c 95 scan (7 processes) runs at nice 10, the k_c 87 scan at nice 8, so the k_c 87 scan has the larger weight until it ends; I cannot lower the k_c 95 scan's nice number without privileges, and I raised nothing of D 21.6875 without the coordinator's word.

## Fifth word of the coordinator (hc, 24 Nov, read at 2026-11-24 22:43 UTC): the k_c 87 scan of macm3's D 21.75 state on Linux, inserted
Verbatim: "Coordinator (t5): yes, add the k_c 87 scan of macm3's D 21.75 state on Linux (window 0.640-0.660 by 0.005 + repeat), first after D 21.6875, before 21.8125 and 21.9375: it splits the -0.000991 into build and k_c step. Prediction: equal to macm3's 0.646846 within 2e-4 if builds agree (as at D 21.125's k_c 87, Windows = macOS to 6 digits)."

- Done (written 2026-11-24 22:43 UTC, before the run): `lane_m3.sh` takes an env `HALF` (grid steps each side of the centre; default 3 = the 7 values and 8 processes of the other points) and was replaced atomically; with `HALF=2` the lane scans lambda 0.640, 0.645, 0.650, 0.655, 0.660 and a repeat of the centre 0.650 (6 evaluations, 6 processes of 1 thread, nice 8). `wait_m3.sh` (replaced atomically again) runs this point, `HALF=2 wait_m3.sh 21.75 0.650 0.646846`, inside the chain when it reaches D 21.8125 and before it starts that point, so the order of the chain is D 21.6875 (running), D 21.75 (Linux k_c 87), D 21.8125, D 21.9375, one at a time, and `exits_chain.txt` says so. The state is macm3's D 21.75 state (commit 660ad084, the one `../kc95_d2175/` regridded; blob f99f513b, record blob a4fb1525, in `21.75/in/`); a `check` run of the lane on it (22:41 to 22:42 UTC) passed: selftests 0 0 0 1 1 0 0 1, `kc87_syscheck_1025.py` exit 0, both controls exit 1, `kc79_syscheck_1025.py` refuses it.
- Reported for this point: the Linux root by position (bracket, det-linear, estimator range) beside macm3's 0.646846 (bracket (0.645, 0.650), range [0.646292, 0.646846], macOS) and beside the k_c 95 root 0.645855 of `../kc95_d2175/`: the difference Linux k_c 87 minus macm3's (the build effect) and k_c 95 minus Linux k_c 87 (the k_c step).
- Predictions, registered before the run (mine, information): all 6 processes print the record system (92%); the repeat agrees (92%); one robust change in the window (88%); the Linux root equal to macm3's 0.646846 within 2e-4 (the coordinator's prediction: 80%), within 1e-5 (55%; the same state, the same grid, and the det-linear root uses the determinants, which two builds reproduce to many digits when the signs are robust); the bracket (0.645, 0.650) (88%). If the roots agree within 2e-4, the offset of -0.000991 is the k_c step and not the build (that follows by construction; my expectation that they agree is the 80% above). The float64 sign differs from the hybrid at 0.655 as it did in macm3's scan (40%) and agrees at all 6 (35%). Each scan point takes 2400 to 3800 s (55%; the first point of the chain on the idle machine; 6 processes beside the recount only). The point is done within 75 min of its lane's start (60%). My registered "all four points done by 23:30 UTC (55%)" is WRONG already: D 21.6875 alone ends after that.

## Status
- 2026-11-24 19:45 UTC: folder, scripts and README written before any pin or run; the pins of the four states and a `check` run of the first point come next, then the chain `i1025-m3pts`.
- 2026-11-24 21:43 UTC: D 21.5625 done (115.2 min; section above); the chain started D 21.6875 at 21:42:14 UTC.
- 2026-11-24 21:44 UTC: the priority word (above): the hold is in place for D 21.8125 and D 21.9375; D 21.6875 runs on.
- 2026-11-24 21:45 UTC: the coordinator's word (hc, verbatim): "Coordinator (t5): yes, renice D 21.6875's 8 processes to nice 15 by exact pid, so the k_c 95 scan gets the cores first." Done: the 8 python processes of D 21.6875's scan (pids 1820198, 1820200 to 1820206) went from nice 8 to nice 15 (`renice -n 15 -p`, verified in `ps`); the k_c 95 scan's 7 processes stay at nice 10. Nothing was stopped; the point finishes later. The hold for D 21.8125 and D 21.9375 is unchanged.
- 2026-11-24 22:43 UTC: the coordinator's word (above): the Linux k_c 87 scan of D 21.75 is inserted after D 21.6875 and before D 21.8125 (`wait_m3.sh`, `lane_m3.sh` replaced atomically; `check` run passed).
- 2026-11-24 22:53 UTC: D 21.6875 done (69.5 min; section above); the chain runs the inserted point D 21.75 (Linux k_c 87) since 22:51:43 UTC, then D 21.8125 and D 21.9375.
