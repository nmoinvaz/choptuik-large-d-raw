# I1025-dh610/kc95_d1975: dh170's k_c 87 D 19.75 state regridded to k_c 95, then a hybrid sign scan at lambda_1 1.30 to 1.36

Machine dh610 (Fedora 45, 20 logical CPUs, 64 GB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 04:16:36 UTC, before any run of this folder.

## Order (coordinator t5, #1025 comment of 04:15 UTC 23 Nov and hc), in part
k_c 95 at D 19.75 from dh170's accepted k_c 87 D 19.75 state (raw I1025-dh170/kc87_d1975/, state blob 352107a8, record 6078a0b4). Step 1: pin them; `kc87_syscheck_1025.py` accepts the source (selftest 0,
`--mutate=F` and `--mutate=steps` exit 1), the k_c 95 check refuses it; then as a systemd-run --user unit, 8 threads, nice 10, in solver/matter: `ell_refine.py l1kc87dh170d1975 87 l1kc95dh610d1975 95 1 19.75
2.1120935738 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`; accept only by the k_c 95 check (selftest 0, both controls exit 1) with the k_c 87 check refusing the result. Step 2, only after
ACCEPTED and after the D 19.5 scan ends: `d18_hybsign.py` at 1.30 to 1.36 by 0.01 plus a repeat of 1.33 (p0 1.30,1.34; p1 1.31,1.35; p2 1.32,1.36; p3 1.33,1.33), then the `read_lower.py` selftest, its
`shift` and `round2` mutations and the reader. Report Delta beside 1.0860022726 (dh170 k_c 87) and 1.0860054437 (k_c 79), every robust change by position, lambda_1 beside 1.326378 (dh170 k_c 79). Memory
alerts only. Send each step's verdict. Roots are read by position, never by sign orientation.

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs and both lanes refuse any other blob)
| item | source | blob |
|---|---|---|
| dh170's k_c 87 D 19.75 state (accepted 04:10:58 UTC 23 Nov) | I1025-dh170/kc87_d1975/sol_l1kc87dh170d1975_D19.7500.npy at raw 9f63ed51 | 352107a8 |
| its record: D 19.75, k_c 87, \|F\| 3.987605893965491e-10, 3124 steps, psi-constraint 9.696e-4, Delta 1.0860022726137006 (Delta_src 1.0860054437335125, the k_c 79 state's) | same folder, l1kc87dh170d1975.jsonl | 6078a0b4 |
| my k_c 87 check, and the k_c 95 check (the k_c 87 check with 3 lines changed: the k_c test, its message, the selftest's planted record; `kc95_syscheck_1025.diff`) | I1025-dh610/kc95_d195/in/ | 6df5d960, d487e628 |
| the scanner, xfkappa's, unmodified; its change finder, `d18c_read.py` | I1025-mac/d18/ | e089207a; 7c9d400f, 1383470f |
| reader (dh170's); `repeat_check.py` | I1025-dh170/lower_root/read_lower.py; I1025-dh610/kc71_d19125/in/ | 89309d3c; aaf598a9 |
Code: worktree `~/Source/choptuik-large-d-1025g` at 48c36355 for the regrid (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_refine.py` blob 631e5801), worktree
`~/Source/choptuik-large-d-1025f` at 505d8399 (clean) for the scan, python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble avx2). The lanes copy the source state into the
regrid worktree's `solver/matter/data/` under the name `ell_refine.py` reads. The result of the regrid is copied into `in/` when accepted, and its blobs are written to `in_blobs_regrid.txt`, which the scan lane requires.

## Commands (systemd user units under `systemd-inhibit`, so no terminal owns them)
**Regrid** (`lane_kc95_regrid.sh`, unit i1025v via `start_kc95_regrid.sh`; stops at the first failure, writes `regrid/steps.txt` and `regrid/VERDICT.txt`), in `solver/matter`:

    nice -n 10 timeout 21600 env OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8 ~/Source/venv-i1058/bin/python -u ell_refine.py \
      l1kc87dh170d1975 87 l1kc95dh610d1975 95 1 19.75 2.1120935738 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma

preceded by the pins, the rebuilt diff of the two checks (three changed lines), the worktree checks, lambda_0(19.75) from `ell_delta.lam0_at` (must read 2.1120935738), both selftests, and the source check.
**Scan** (`lane_kc95_scan.sh`, unit i1025w via `start_kc95_scan.sh`): started now and waiting; it proceeds only when `regrid/VERDICT.txt` reads ACCEPTED and unit i1025u (the D 19.5 scan) has ended (6 h cap on the
wait; it stops if the regrid is REFUSED). Then 4 processes of 1 thread at nice 10, `d18_hybsign.py in/l1kc95dh610d1975.jsonl in/sol_l1kc95dh610d1975_D19.7500.npy 19.75 LAMS scan/scan_D19.75_p<p>.jsonl`: p0 1.30,1.34;
p1 1.31,1.35; p2 1.32,1.36; p3 1.33,1.33 (the order's split: the repeat runs on the same process as its original, so a repeat on another process is not tested here). Then the reader selftests and `read_lower.py scan 1.30 1.36`.

## Acceptance (the order's, fixed before the run)
1. **Step 1, source.** `kc87_syscheck_1025.py` accepts the source (|F| at most 1e-9, `freeze_from` gives 3124 steps, |F| within 1% of the record), its selftest exits 0, `--mutate=F` and `--mutate=steps` exit 1, and
   `kc95_syscheck_1025.py` refuses the source (exit 1). Otherwise no regrid.
2. **Regrid.** `ell_refine.py` exits 0 (the cap 21600 s is a stop); `kc95_syscheck_1025.py` accepts the result, its selftest exits 0, both controls exit 1, and `kc87_syscheck_1025.py` refuses the result (exit 1).
   A control that fires stops the work, and I report it; no bar is loosened.
3. **Scan.** Each process prints the record system; `read_lower.py selftest` exits 0, `--mutate=shift` and `--mutate=round2` exit 1, `repeat_check.py selftest` exits 0; the repeat of 1.33 agrees (sign, ln|det| within
   1e-6, noise signs, float64 sign).

## Reading, fixed now (by position)
Every robust change (both neighbouring points noise-robust) with bracket, det-linear estimate and estimator range (the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure); the
bracket is the grid step 0.01. Orientation only as the reader prints it. The edge signs; changes touching a non-robust point listed and not counted; every ln|det| minimum without a sign change flagged; the repeat's
bits. The window 1.30 to 1.36 holds the root near lambda_1's line; the second root (macm3's k_c 87: 1.276162) is below it and is not scanned. Reported beside dh170's k_c 79 1.326378 and macm3's k_c 87 1.338993
(macOS); dh170's own k_c 87 reading of the same state on Linux is running as I write. These are k_c 95 roots, not yet physical. Delta is reported beside 1.0860022726 and 1.0860054437.

## Predictions, registered before the runs
- Source check passes with all four controls firing about 95%; regrid exits 0 and is accepted with both controls firing and the k_c 87 check refusing the result about 85%.
- Steps: the k_c 79 to 87 step ratio was 1.1014 (D 19.5) and 1.1004 (D 19.75, dh170), and the 87 to 95 ratio at D 19.5 was 1.0911, so about 3409 steps (within 10 about 60%). |F| below 1e-9 about 95%.
- Delta: the 79 to 87 shift was -3.17e-6 at D 19.5 and -3.17e-6 at D 19.75, and the 87 to 95 shift at D 19.5 was -2.24e-6, so Delta about 1.0860000329 (within 3e-7 about 65%).
- Regrid wall: 4291 s at D 19.5 for 3460 steps with the machine idle, so about 4230 s plus a few percent while the D 19.5 scan's 4 processes run beside it; 3900 to 4900 s about 70%; peak RSS below 3 GiB about 85%.
- Scan: every point noise-robust about 70%; the repeat bit-identical about 90%; exactly one robust change in 1.30 to 1.36 about 85%, lying between 1.322 and 1.345 about 80% (the build alone moved lambda_1 by 0.0032 at
  D 19.5); a scan point about 1500 to 2300 s on 4 processes alone.

## Status
- 2026-11-23 04:16:36 UTC: folder, inputs, lanes and the reading prepared before any run. The D 19.5 scan (../kc95_d195, unit i1025u) is still running (8 of 10 points; processes 2 and 3 ended at 04:08 UTC).
- 04:16:43 to 04:16:49 UTC: pins, rebuilt diff of the two checks (3 changed lines), worktree 48c36355, lambda_0(19.75) = 2.1120935738, both selftests exit 0, then the source check: `kc87_syscheck_1025.py` on dh170's state exit 0 (|F| 3.9876058940e-10 = his record's, `freeze_from` 3124 = 3124), `--mutate=F` exit 1, `--mutate=steps` exit 1, `kc95_syscheck_1025.py` on the k_c 87 source exit 1. The regrid started 04:16:49 UTC (unit `i1025v`, 8 threads, nice 10); unit `i1025w` (the scan lane) started 04:17:36 UTC and waited.
- 04:50:40 UTC the D 19.5 scan (../kc95_d195, unit i1025u) ended; its last two points had run beside this regrid. 05:07:55 UTC the regrid exited 0 (wall 3066 s); 05:08:01 UTC ACCEPTED (below). 05:08:36 UTC the scan lane saw both conditions, passed its pins and selftests (exits 0 1 1 0, MemAvailable 36.4 GB) and started the 8 evaluations on 4 processes.

## Regrid result (23 Nov, 04:16:49 to 05:08:01 UTC): ACCEPTED

`ell_refine.py` (8 threads, nice 10, unit `i1025v`) exited 0 after 3066 s (the record's own 3064 s; predicted 3900 to 4900 s: no, it was faster; the D 19.5 regrid took 4293 s, the cause of the difference is unmeasured); peak sampled RSS 2.00 GB, 776% CPU on average (`regrid/regrid_samples.csv`, 51 samples); 25 numpy RuntimeWarning lines in the log, as in the earlier regrids; no memory alert.
- Record `l1kc95dh610d1975.jsonl` (blob 7aca695d) and state `sol_l1kc95dh610d1975_D19.7500.npy` (blob 57875891, copied to `in/`; `in_blobs_regrid.txt`): k_c 95 at D 19.75, |F| 3.9634509412e-10, F_start 3.337e-06, **3411 steps** (predicted about 3409: yes), constraint 3.967e-04 (dh170's k_c 87 state: 9.696e-04), **Delta 1.0860000558** (predicted 1.0860000329, within 3e-7: yes, it differs by 2.3e-8).
- **Delta beside the numbers given:** dh170's k_c 87 1.0860022726 (this regrid's source): -2.2168e-6; k_c 79 1.0860054437: -5.3880e-6. At D 19.5 the same step from k_c 87 moved Delta by -2.2397e-6.
- **Acceptance:** `kc95_syscheck_1025.py` exit 0 (the state's |F| equals the record's, `freeze_from` gives 3411 steps = the record's); selftest PASS; `--mutate=F` exit 1 (the state's |F| is not within 1% of 1.5 times the record's), `--mutate=steps` exit 1 (`freeze_from` gives 3411, the record 3412); extra control: `kc87_syscheck_1025.py` on the k_c 95 result exits 1 (the record is not k_c 87). The source check, its controls and the k_c 95 check's refusal of the k_c 87 source are in `regrid/source_*.txt` (above).
- 06:35:48 UTC the scan ended (all four processes exit 0; `exits_kc95_scan.txt`); reading below. Round 1 ran beside `../cross_macm3_d1975` (from 05:40:05 UTC), round 2 beside it until 06:19:54 UTC and, from 06:33:38 UTC, beside the two re-convergence units of `../reconv_d1975` (load up to 17.96).

## Scan result (23 Nov, 05:08:36 to 06:35:48 UTC): one robust change in 1.30 to 1.36, between 1.32 and 1.33; the repeat agrees

All four processes exit 0. Walls 1:27:11 (process 0), 1:26:53 (1), 1:27:08 (2), 1:26:43 (3); peak RSS 3.14 to 3.33 GB per process (`scan/scan_p<p>.raw`, `/usr/bin/time -v`). Sampled every 30 s (`scan/sampler.log`, 174 samples): summed RSS at most 9.54 GB, MemAvailable at least 26.57 GB, load at most 17.96. The pre-run checks passed (reader selftest exit 0, `--mutate=shift` and `--mutate=round2` exit 1, `repeat_check.py` selftest exit 0), all four processes printed "the record system" (|F| 3.9645666015e-10 against the record's 3.9634509412e-10, steps 3411 = 3411). No memory alert fired (no `scan/MEMALERT.txt`, no `ALERTS.txt`).

| lambda_1 | process | hybrid sign | noise signs | noise_robust | float64 sign | ln\|det\| | point sec |
|---|---|---|---|---|---|---|---|
| 1.30 | 0 | -1 | -1, -1 | True | +1 | -3160.0033618426 | 2461 |
| 1.31 | 1 | -1 | -1, -1 | True | +1 | -3161.1815177930 | 2450 |
| 1.32 | 2 | -1 | -1, -1 | True | +1 | -3162.9657080570 | 2455 |
| 1.33 | 3 | +1 | +1, +1 | True | +1 | -3163.4034338844 | 2442 |
| 1.33 (repeat) | 3 | +1 | +1, +1 | True | +1 | -3163.4034338844 | 2758 |
| 1.34 | 0 | +1 | +1, +1 | True | +1 | -3162.9234086833 | 2767 |
| 1.35 | 1 | +1 | +1, +1 | True | +1 | -3162.9564591131 | 2760 |
| 1.36 | 2 | +1 | +1, +1 | True | +1 | -3163.1198183109 | 2770 |

Reading (`read_lower.txt`, `read_lower.py` dh170's, unedited; signs as the reader prints them):
- **Robust change:** one, between 1.320 and 1.330, `- to +` as the reader prints it, det-linear estimate **1.326077**, estimator range [1.323726, 1.326077] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.01). No change touches a non-robust point; every point is noise-robust.
- **Edge signs:** - at 1.30, + at 1.36.
- **ln|det| minima without a sign change:** none (the reader). ln|det| is lowest at 1.33, beside the change; it rises to -3162.92 at 1.34 and falls again to -3163.12 at 1.36, so it is still falling at the upper edge: nothing was scanned above 1.36.
- **Repeat of 1.33:** agrees, bit-identical (`repeat_check.py` PASS; ln -3163.403433884402 twice), on the same process as its original, as the order placed it, so it tests repeatability within a process, not another process.
- **Float64:** its sign is +1 at every point, so it differs from the hybrid at 1.30, 1.31 and 1.32 (+ against -) and shows no change in the window; the hybrid is the reading.

Beside which I report (information, not a pass rule; the coordinator's numbers), by position the root near lambda_1's line at D 19.75:
| k_c | lambda_1 | state, machine |
|---|---|---|
| 79 | 1.326378 | dh170, Linux |
| 87 | 1.325410 (in (1.32, 1.33), his round 1) | dh170, Linux, regridded from his k_c 79 state (my regrid's source) |
| 87 | 1.338993 | macm3, macOS, regridded from the same k_c 79 state (a different state: `../cross_macm3_d1975/`) |
| 95 | 1.326077, range [1.323726, 1.326077] | this scan, Linux, regridded from dh170's k_c 87 state |
- The k_c 95 root is 0.000301 below dh170's k_c 79 (1.326378) and 0.000667 above his k_c 87 (1.325410), both Linux; it is 0.012916 below macm3's k_c 87 (1.338993), which is a different state, as the cross-check found. Both grids are 0.01, so differences of a few 1e-4 are below what the interpolation resolves; I do not read them as a k_c effect.
- **Delta** (regrid, above): k_c 95 1.0860000558 beside dh170's k_c 87 1.0860022726 (-2.2168e-6) and k_c 79 1.0860054437 (-5.3880e-6).
- No second change in 1.30 to 1.36. Nothing was scanned outside it.

Predictions (written before the run): every point noise-robust (70%): yes; the repeat bit-identical (90%, same process): yes; exactly one robust change in 1.30 to 1.36 (85%): yes, lying between 1.322 and 1.345 (80%): yes (1.326077); a point 1500 to 2300 s on 4 processes alone: no, 2442 to 2461 s in round 1 and 2758 to 2770 s in round 2, both beside other jobs (above), so the prediction was for an idle machine and the point cost 6 to 20% more than the top of the predicted range.

These are k_c 95 roots, not yet physical.
