# I1025-dh610/kc95_d195: my k_c 87 D 19.5 state regridded to k_c 95, then a hybrid sign scan at lambda_1 1.380 to 1.420

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task from the coordinator (hc, 23 Nov 2026), after `../kc87_d195/` (raw 94e9ebc6) and `../kc87_d1925/` (raw 9a96d4f4): k_c 95 at D 19.5, a third high k_c where k_c 79 and k_c 87 differ by 1.6e-3.

## Order (the coordinator's)

1. **Regrid** my accepted k_c 87 D 19.5 state (raw `I1025-dh610/kc87_d195/`, a373049a: state `sol_l1kc87dh610d195_D19.5000.npy` blob 57f8e2d3, record `l1kc87dh610d195.jsonl` blob 64b8db7c) to k_c 95 with `ell_refine.py` as before (lambda_0(19.5) = 2.1132623525). First my k_c 87 check on the source (must accept, both controls refuse). Accept the result only by a k_c 95 check made from my k_c 87 check by changing the k_c test to 95 and nothing else (the diff is in this folder; its selftest, both controls refuse), and the k_c 87 check must refuse the result. 8 threads, nice 10, a systemd unit. If `ell_refine.py` cannot reach k_c 95 (a size or array limit), stop and report; change no code.
2. **Scan** lambda 1.38 to 1.42 at 0.005 (9 values) plus a repeat of 1.40, 4 processes of 1 thread (k_c 95 points may need more memory: check free memory first, stop under 4 GiB; **corrected by the coordinator on 23 Nov: no memory guard may stop or kill a process, memory watchers only alert, only a refusal to start is allowed; see Setup**), `read_lower.py`.
3. Read roots by position. Post on #1025, send the coordinator each step's verdict with the raw commit.

Beside which I report (information, not a pass rule; the coordinator's numbers): k_c 79 at D 19.5 has lambda_1 at **1.397565** (the line root near lambda_1's line) and k_c 87 at **1.399169** (`../kc87_d195/`, raw 94e9ebc6: det-linear, range [1.398747, 1.399169]).

## Setup

- Regrid: unit `i1025t` (`lane_kc95_regrid.sh`, started by `start_kc95_regrid.sh`), `OMP`, `OPENBLAS`, `MKL` = 8, nice 10, cap 21600 s, under `systemd-inhibit` with the alert-only memory log; steps and verdicts in `regrid/steps.txt` and `regrid/VERDICT.txt`. The lane is `../kc87_d195/lane_kc87_regrid.sh` with the source and target changed one k_c up (the checks, the tags, the source blobs, `ell_refine.py ... 87 ... 95 ...`) and a free-memory rule added (below); nothing else.
- Code (as at the k_c 87 regrids): worktree `~/Source/choptuik-large-d-1025g` at 48c36355 for `ell_refine.py` (blob 631e5801; `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's) and worktree `~/Source/choptuik-large-d-1025f` at 505d8399 (clean) for the scan; Python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble avx2). The lanes refuse on any other pin.
- Free memory (corrected on 23 Nov at the coordinator's order, Nathan's standing rule of 2026-11-08: no memory guard stops or kills a process): the regrid lane refuses to start with less than 8 GiB available and the scan lane refuses to start with less than 4 x 4 GB + 4 GB available (k_c 87's peak was 2.9 GB per process); nothing is stopped or terminated for memory. Below 4 GiB the lane's sampler only writes `regrid/MEMALERT.txt` or `scan/MEMALERT.txt`, and a watcher of the runner session (`ALERTS.txt`) posts the free memory to the coordinator by hc. As first written the regrid lane terminated `ell_refine.py` (exact pid) below 4 GiB and the scan lane its `d18_hybsign.py` processes; the regrid started with that guard (a one-minute sample loop, never fired; the lane as started is `lane_kc95_regrid_as_started.sh`). At 00:51 UTC I stopped that sample loop by its exact pid (the computation's pids were not touched and it was not restarted), and the watcher took over the once-a-minute lines of `regrid/regrid_samples.csv`; `lane_kc95_regrid.sh` and `lane_kc95_scan.sh` are now alert-only. Other projects' jobs are left alone. At the start: 38.9 GiB available.
- Inputs (copied to `in/`, pinned by `git hash-object --no-filters`, `in_blobs.txt`): my `sol_l1kc87dh610d195_D19.5000.npy` 57f8e2d3 and `l1kc87dh610d195.jsonl` 64b8db7c (the same blobs at raw a373049a: k_c 87, D 19.5, |F| 3.5228509267e-10, 3171 steps, constraint 7.311e-04, Delta 1.0798374906); `kc87_syscheck_1025.py` 6df5d960; `kc95_syscheck_1025.py` d487e628 (below); `d18_hybsign.py` e089207a (xfkappa's, unmodified), `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9 (dh170's, unedited).
- The k_c 95 check, `in/kc95_syscheck_1025.py`: `kc87_syscheck_1025.py` with the k_c test changed to 95, which is three lines as at D 19.5 (the test `rec.get("kc") != 95`, its message "the record is not k_c 95 ...", and the selftest's planted record `kc=95`, without which the selftest's converged-record case could not pass); nothing else, not the docstring either (`kc95_syscheck_1025.diff`; the lane rebuilds the diff, requires that it equals this file and has three changed lines). Its selftest exits 0.

## Commands

Regrid (cwd `~/Source/choptuik-large-d-1025g/solver/matter`; the source state is copied to `data/sol_l1kc87dh610d195_D19.5000.npy`, where it already is, and checked by blob):

    nice -n 10 timeout 21600 env OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8 \
      ~/Source/venv-i1058/bin/python -u ell_refine.py l1kc87dh610d195 87 l1kc95dh610d195 95 1 19.5 2.1132623525 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma

Scan (`lane_kc95_scan.sh`, unit `i1025u`, written from `../kc87_d1925/lane_kc87_d1925_scan.sh` with the D, the tags, the lambda list and the free-memory rule changed): `d18_hybsign.py in/l1kc95dh610d195.jsonl in/sol_l1kc95dh610d195_D19.5000.npy 19.5 <lambdas> scan/scan_D19.5_p<p>.jsonl` in 4 processes of 1 thread, nice 10; the list is 1.380, 1.385, ..., 1.420 then the repeat 1.400, value i to process i mod 4: p0 1.380, 1.400 (the original), 1.420; p1 1.385, 1.405, 1.400 (the repeat); p2 1.390, 1.410; p3 1.395, 1.415, so the repeat runs on a different process than its original. Three rounds. Then `read_lower.py scan 1.38 1.42` (it keys and prints lambda to three decimals; its selftest has a 0.005 grid) and `repeat_check.py` (`read_lower.txt`), after the reader's selftest and its mutations `shift` and `round2` (exits wanted 0 1 1 0 with `repeat_check.py selftest`).

## Acceptance (fixed before the run, as at k_c 87)

1. **Source.** `kc87_syscheck_1025.py` accepts my k_c 87 D 19.5 state and record (the record's |F| at most 1e-9, `freeze_from` gives the record's step count, 3171, and |F| within 1% of the record's), `--mutate=F` and `--mutate=steps` exit 1, both selftests exit 0, and the k_c 95 check refuses the k_c 87 source. Otherwise no regrid. (The dry run of the lane, `regrid/source_syscheck*.txt`, has done this: exit 0, the controls exit 1, 1, the k_c 95 check exit 1.)
2. **Result.** `kc95_syscheck_1025.py` accepts the regridded record and state (k_c 95 at D 19.5, |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%), `--mutate=F` and `--mutate=steps` exit 1, and `kc87_syscheck_1025.py` on the k_c 95 result exits 1. A regrid that exits non-zero (a size or array limit, the 21600 s cap) is a stop, and I report; no code is changed.
3. **Scan.** Starts only after the verdict ACCEPTED. Each process first prints `the record system`; anything else is a stop. The reader's selftest passes and its two mutations exit 1; the repeat of 1.400 agrees (`repeat_check.py`). No other machine holds this state, so there is no cross-machine control for the k_c 95 scan: the system check and the repeat are the controls, as at k_c 87.

## Reading (fixed before the run)

Every robust change (bracket, orientation as printed by the reader, det-linear estimate, estimator range); the edge signs; every ln|det| minimum without a change; the repeat; the float64 sign beside the hybrid (information); each point's noise-robustness. The estimator range is a spread over interpolation choices, not an enclosure; the bracket is the 0.005 grid step. A root is named by position (the root near lambda_1's line, the rising root), its orientation printed only as the reader prints it and never compared across D. Roots are called k_c 95 roots, not yet physical.

## Predictions (written before the run; information)

The regrid reaches k_c 95 and is accepted (80%; a size or array limit 10%, a check refusing it 10%); k_c 79 to k_c 87 added 10% to the step count (2879 to 3171 here, 2925 to 3222 at D 19.25), so about 3450 steps and a wall of 3500 to 4300 s (k_c 87: 3215 s). The scan shows one robust change in 1.380 to 1.420 (75%), within 0.002 of k_c 87's 1.399169 (75% given one), and no second (85%); a point takes 1800 to 2200 s with 4 processes (k_c 87: 1597 to 1724 s), the scan three rounds of that, 1.5 to 1.8 h.

## Status (23 Nov)

- 00:48:22 UTC the dry run of the regrid lane passed the pins, the diff rebuild, the selftests and the source check (see Acceptance 1); nothing started yet.
- 00:49:32 UTC the regrid started (unit `i1025t`, 8 threads, nice 10; the source check of the real run passed again: exit 0, controls exit 1, 1, the k_c 95 check refuses the k_c 87 source). 00:51 UTC the memory guard was made alert-only as above (the running regrid was not restarted).
- 02:01:05 UTC the regrid exited 0 (wall 4293 s) and 02:01:11 UTC it was ACCEPTED (below). My session lost the API from about 01:00 to 02:50 UTC (the coordinator's account: the home network was down; the unit kept running, the machine did not reboot), so the scan, which the order starts after the verdict, started late: 02:52:27 UTC (unit `i1025u`, `lane_kc95_scan.sh`, alert-only for memory), 10 evaluations on 4 processes of 1 thread, nice 10, pins and selftests passed (exits 0 1 1 0; the dry run at 02:52:20 UTC). The alert-only watcher (`ALERTS.txt` would list any alert) wrote none, and no `MEMALERT.txt` exists.
- 04:50:40 UTC the scan ended (all four processes exit 0; `exits_kc95_scan.txt`); reading below. The last two points of processes 0 and 1 ran beside the D 19.75 regrid of `../kc95_d1975/` (8 threads, from 04:16:49 UTC), which another order started on this machine.

## Regrid result (23 Nov, 00:49:32 to 02:01:11 UTC): ACCEPTED

`ell_refine.py` (8 threads, nice 10, unit `i1025t`) exited 0 after 4293 s (the record's own 4291 s; predicted 3500 to 4300 s); peak sampled RSS 2.70 GB, 778% CPU on average; no size or array error: `ell_refine.py` reached k_c 95 (`regrid/regrid.log`, `regrid/regrid_samples.csv`, `regrid/steps.txt`). Its log carries 24 numpy RuntimeWarnings (overflow, invalid value) from `dss_ell.py` lines 88, 211 to 219, 325 and 334 in the solver's trial evaluations (the k_c 87 regrids' logs had 25 and 21 at the same lines); the acceptance is the check below, not the log.
- Record `l1kc95dh610d195.jsonl` (blob 37796bb9) and state `sol_l1kc95dh610d195_D19.5000.npy` (blob e5ea14bd, copied to `in/`; `in_blobs_regrid.txt`): k_c 95 at D 19.5, |F| 3.5335625278e-10, F_start 2.395e-06, 3460 steps (predicted about 3450), constraint 2.860e-04, Delta 1.0798352509 (my k_c 87 source: |F| 3.5229e-10, 3171 steps, constraint 7.311e-04, Delta 1.0798374906; k_c 95's Delta is 2.24e-06 below).
- **Acceptance:** `kc95_syscheck_1025.py` exit 0 (the state's |F| equals the record's, `freeze_from` gives 3460 steps = the record's); `--mutate=F` exit 1 (the state's |F| is not within 1% of 1.5 times the record's), `--mutate=steps` exit 1 (`freeze_from` gives 3460, the record 3461); extra control: `kc87_syscheck_1025.py` on the k_c 95 result exit 1 ("the record is not k_c 87 at D 19.5 (kc 95, D 19.5)"). Verdict `regrid/VERDICT.txt`: ACCEPTED 02:01:11 UTC.

## Scan result (23 Nov, 02:52:27 to 04:50:40 UTC): one robust change in 1.380 to 1.420, between 1.395 and 1.400; the repeat agrees

All four processes exit 0. Walls 1:58:12 (process 0), 1:54:36 (1), 1:16:22 (2), 1:16:23 (3); peak RSS 3.14 to 3.30 GB per process (`scan/scan_p<p>.raw`, `/usr/bin/time -v`). Sampled every 30 s (`scan/sampler.log`, 236 samples):
summed RSS at most 10.92 GB, MemAvailable at least 24.19 GB, load at most 11.36. The pre-run checks passed (README Acceptance): reader selftest exit 0, `--mutate=shift` and `--mutate=round2` exit 1, `repeat_check.py` selftest exit 0,
all four processes printed "the record system" (|F| 3.5307904178e-10 against the record's 3.5335625278e-10, steps 3460 = 3460). No memory alert fired (no `scan/MEMALERT.txt`, no `ALERTS.txt`).

| lambda_1 | process | hybrid sign | ln\|det\| | noise_robust | float64 sign | point sec |
|---|---|---|---|---|---|---|
| 1.380 | 0 | -1 | -3188.0933117654 | True | -1 | 2337 |
| 1.385 | 1 | -1 | -3188.5694378172 | True | -1 | 2343 |
| 1.390 | 2 | -1 | -3189.1874472696 | True | -1 | 2329 |
| 1.395 | 3 | -1 | -3190.2085401142 | True | -1 | 2336 |
| 1.400 | 0 | +1 | -3191.3776333577 | True | -1 | 2238 |
| 1.400 (repeat) | 1 | +1 | -3191.3776333577 | True | -1 | 2286 |
| 1.405 | 1 | +1 | -3189.9772787360 | True | -1 | 2244 |
| 1.410 | 2 | +1 | -3189.5506268603 | True | -1 | 2250 |
| 1.415 | 3 | +1 | -3189.3385984907 | True | +1 | 2245 |
| 1.420 | 0 | +1 | -3189.2231421486 | True | +1 | 2514 |

Reading (`read_lower.txt`, `read_lower.py` dh170's, unedited; signs as the reader prints them):
- **Robust change:** one, between 1.395 and 1.400, `- to +` as the reader prints it, det-linear estimate **1.398815**, estimator range [1.398639, 1.398815] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). No change touches a non-robust point; every point is noise-robust.
- **Edge signs:** - at 1.380, + at 1.420.
- **ln|det| minima without a sign change:** none. ln|det| is lowest at 1.400, beside the change (1.17 below 1.395 and 1.40 below 1.405); on both sides it varies smoothly (rises from -3191.38 at 1.400 to -3189.22 at 1.420, rises from -3191.38 to -3188.09 going down to 1.380).
- **Repeat of 1.400:** agrees, bit-identical (`repeat_check.py` PASS; ln -3191.377633357704 on process 0 and on process 1, the same sign, noise signs and float64 sign). Same machine and build, so it tests repeatability, not another machine.
- **Float64:** its sign differs from the hybrid at 1.400 (both evaluations), 1.405 and 1.410 (- against +), so float64 alone would put the change between 1.410 and 1.415; the hybrid is the reading.

Beside which I report (information, not a pass rule; the coordinator's numbers), by position the root near lambda_1's line at D 19.5:
| k_c | lambda_1 | by | machine and grid |
|---|---|---|---|
| 79 | 1.397565 | the coordinator's number | not mine |
| 87 | 1.399169, range [1.398747, 1.399169] | my scan, `../kc87_d195/` | this machine, grid 0.01 |
| 95 | 1.398815, range [1.398639, 1.398815] | this scan | this machine, grid 0.005 |
- The k_c 95 root is 0.000354 below k_c 87's (same machine, same regrid code, the k_c 87 state is the k_c 95 state's source) and 0.001250 above k_c 79's. The two estimator ranges overlap ([1.398747, 1.398815]). The two grids differ (0.01 and 0.005), so a difference of 0.00035 is below what the interpolation resolves; I do not read it as a k_c effect. The step from k_c 87 to k_c 95 is smaller than the build alone moved lambda_1 at k_c 87 (macm3 1.396000, macOS, against my 1.399169: 0.0032, two regrids of the same state).
- No second change in 1.380 to 1.420. Nothing was scanned outside it (k_c 71's roots at D 19.5 are 1.3715 and 1.4492, the coordinator's numbers; the window's upper edge 1.420 is below 1.4492).

Predictions (written before the run): one robust change in the window within 0.002 of 1.399169 (75% given one): yes (0.000354); no second (85%): yes; a point 1800 to 2200 s: no, 2238 to 2514 s (2329 to 2343 s with four processes at once, 2238 to 2250 s in the second round; the last two points, 2286 and 2514 s, ran beside the D 19.75 regrid); the scan 1.5 to 1.8 h: no, 1:58:12 for the longest process.

These are k_c 95 roots, not yet physical.
