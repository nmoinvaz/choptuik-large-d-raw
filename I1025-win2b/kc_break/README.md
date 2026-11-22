# I1025-win2b/kc_break: where the k_c-stable branch of lambda_1 breaks, the hybrid sign scans at D 18.375 at k_c 63 and k_c 55 (win2b)

Machine win2 (Windows 11, Intel Core Ultra 7 265K, 20 cores). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025

Written before the run, 2026-11-22 03:00 UTC by `date -u`.

## Order

The coordinator (hc, about 02:50 UTC 22 Nov, after Nathan lifted the usage pause): lambda_1's branch is k_c-stable through D 18.25 (k_c 55 minus k_c 63: 1.3e-4 at D 17.75, 9.4e-4 at D 18.125, 1e-4 at D 18.25; comments 7071508693, 7072529186, 7072669877). At D 18.5 it is not (k_c 55 has a complex pair near 1.684). Find where it breaks. Your state is D 18.375. Scan both k_c there over lambda 1.62 to 1.80 at 0.01 (19 points each): k_c 63 on raw `I1025-mac/d18/sol_l1kc63Wm1025_D18.375000.npy` (its leap record line) and k_c 55 on raw `I1025-mac/out/sol_l1kc55F1025_D18.375000.npy` (its record line), each with the system check first, `d18_hybsign.py`, the noise test and the float64 sign. Run the two k_c side by side, 4 threads each, nice 10 (BelowNormal on Windows), 8 h caps. Window and reading go into this README first, raw `I1025-win2b/kc_break`. Post on #1025.

Reading (the coordinator's, fixed before the run): **the k_c 55 root's det-linear estimate within 0.01 of the k_c 63 root's means stable at D 18.375; no k_c 55 root there, or one further off, means it breaks by D 18.375. Report any ln|det| minimum without a change, with a dip fit.**

## Inputs (raw origin/main 7d6e1e09, taken by `git show`, checked with `git hash-object --no-filters`; `in/pins.txt`, `in/pins_check.log`)

| item | raw path | blob |
|---|---|---|
| scanner | `I1025-mac/d18/d18_hybsign.py` | e089207a61fbd98614716abd309571cbc4888db2 |
| k_c 63 state | `I1025-mac/d18/sol_l1kc63Wm1025_D18.375000.npy` (33208 bytes) | aa04459266643be3dfd46c2d83c52f556ed6254c |
| k_c 63 record | `I1025-mac/d18/l1kc63Wm1025.jsonl`, the leap's one D 18.375 line (line 6: k_c 63, F 2.791072127489636e-10, 2483 steps, kappa 0.7, u0 0.04, Ks 30, h 0.0625) | 08f4dbf367edba55814e5cf989ccd32a9a5dbe67 |
| k_c 55 state | `I1025-mac/out/sol_l1kc55F1025_D18.375000.npy` (29048 bytes) | 6a1df3d65f5baa6611feaea06cf8fa631cadea21 |
| k_c 55 record | `I1025-mac/out/l1kc55F1025.jsonl`, its one D 18.375 line (line 10: k_c 55, F 2.743469379731208e-10, 2169 steps, kappa 0.7, u0 0.04, Ks 30, h 0.0625) | 0fb77df8281d634e6ecf2d3b2038e3706df3c960 |
| xfkappa's scan reader (the det-linear estimate) | `I1025-mac/d18/d185_scan_read.py` | 7c9d400fd0966a35ac306b5495febb4ec4efe7da |
| the lane script and the k_c 63 D 18.5 scan (controls) | `I1025-mac/d18/lane_d185S.sh`, `d185_scan_1025.jsonl` | a019238b, 90540daf |

Code: worktree `D:/choptuik-1025p4` at 505d8399, clean (`P4_WT_MATTER`; the driver checks that `dss_ell.py`, `ell_ddm.py` and `ddnp.py` equal 505d8399), PY `C:/Users/nathan/Source/venv-md510` (multidouble 5.1.0), BelowNormal, 4 BLAS and rayon threads per process. Both states are the Mac's, taken as they are; whether each is its record's system is the scanner's own first check.

## The scan command, quoted

`d18_hybsign.py` docstring: `usage (venv-1025dd): d18_hybsign.py STUB.jsonl STATE.npy D LAMS OUT.jsonl   (LAMS comma-separated)`. It takes the record line at D from the first file (the record's jsonl works as it is), **rebuilds the record's discrete system and checks it first** (|F| within 1% of the record's F and equal steps, else "NOT the record system", exit 3, before any lambda; the driver then stops and nothing is read), and at each lambda prints the hybrid sign and ln|det| (`p4_hybrid.py`'s `sd()`, unchanged) with its 1e-15 noise test on blocks 0 to 11 (2 seeds) and the plain float64 sign beside it.

xfkappa's D 18.5 scan in `lane_d185S.sh` (blob a019238b): `timeout 21600 nice -n 10 $PY -u $Q/d18_hybsign.py $REC $ST 18.5 $L $SCAN < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d185_scan.log`. Mine, per k_c (`break_driver.sh`): `python -u in/d18_hybsign.py in/<record> in/<state> 18.375 <LAMS> <OUT>` with the same environment as my earlier scans. Differences from the quoted line, outside the computation: venv-md510, no `nice` (BelowNormal by the launcher, the Windows form of nice 10), no `timeout` (an exact-pid cap with a command-line check), and the warning filter applied to a copy of the raw log after the run.

## Window and lambda list, fixed before the run

Window: lambda 1.62 to 1.80 at 0.01, 19 points, at each k_c. By interpolation between the k_c 63 roots at D 18.25 (1.7425) and D 18.5 (1.6772) the k_c 63 root at D 18.375 is expected near 1.71 (information, not a reading); the window holds both ends of that with margin. One process per k_c, side by side, each evaluating the 19 points in ascending order and then **1.71 again** (20 evaluations): the coordinator ordered no repeat, and the two k_c cannot repeat a point for each other, so each process repeats one point inside itself, a determinism check at the bar of the earlier scans.

| process | lambda, in this order | evaluations |
|---|---|---|
| k_c 63 | 1.62, 1.63, ..., 1.80, then 1.71 again | 20 |
| k_c 55 | 1.62, 1.63, ..., 1.80, then 1.71 again | 20 |

Caps 28800 s (8 h) each by the exact pid of the root process (`taskkill /T /F /PID`) after a check that its command line contains `d18_hybsign.py`; a cap is not retried.

## Reading, fixed now (`kc_break_compare.py`, `read_fine.py`, `dip_fit3.py`)

A **root** is a robust change of the hybrid sign: two consecutive points of different sign, both passing the 1e-15 noise test; it lies in its 0.01 bracket. Its **det-linear estimate** and estimator range (the span of four estimates, information) are computed by `changes()` of xfkappa's `d185_scan_read.py` (blob 7c9d400f, in `in/`), the code `d18f_read.py` uses; the planted controls check the script against that function. For the k_c 63 root (the one expected), the nearest k_c 55 robust change by estimate, and the difference **d = estimate(k_c 55) - estimate(k_c 63)**, printed with its sign:

- **|d| <= 0.01 (inclusive): STABLE at D 18.375.**
- **|d| > 0.01: BREAKS by D 18.375** (the k_c 55 root is further off).
- **no k_c 55 robust change in the window: BREAKS by D 18.375** (no k_c 55 root there).
- no k_c 63 robust change in the window: reported, not covered by the fixed reading. More than one k_c 63 robust change: each is paired and reported, and the overall line says OTHER (the fixed reading is for one root). A k_c 55 robust change paired with no k_c 63 root is listed. A change that touches a non-robust point is listed with its estimate and not counted.
- information beside each verdict, not used by it: the orientations (the same or the opposite) and whether the two estimator ranges overlap. **All orientation readings wait for xfkappa's sign-convention check.**

**Every ln|det| local minimum without a change** (an interior point below both neighbours', the hybrid sign the same on both sides) is reported by `read_fine.py` (step 0.01) and fitted by `dip_fit3.py` with the dip model of Part 2 and Part 3 in `../kc55` (ln|det| = a + ln((l - l0)^2 + e^2) + b (l - l0) + c (l - l0)^2, a complex pair l0 +- i e times a smooth factor) over the 11 points around the minimum, with the 1-sigma uncertainties and quartic and quadratic polynomials over the same points. Version 3 adds the two limits found at D 18.25 as flags: the fit is NOT RESOLVED when |e| is below half a step, its uncertainty exceeds |e|, **l0 lies outside the fit window**, or **the quartic polynomial fits the same points better than the model**. The fit is information, a model and not a root search.

The float64 sign beside the hybrid is information. The line "FINE READING" of `read_fine.py` is the 0.002 scan's rule and is not used here.

## Repeat check, fixed now

At the repeated lambda 1.71, in each process, the two records must have the same hybrid sign and ln|det| equal to 1e-6 (`merge_repeat.py`; the gate, per k_c). The merged 19-point scan of a k_c is written only if its check passes, 1.71 occurs exactly twice and every other lambda once, every record is at D 18.375 and the right k_c, and all 19 lambda are present. The reading is made only if both scans merge.

## Controls, before the run

`plant_checks_break.py`, 32 cases (`plant_checks_break.log`, rerun by the driver as `plant_checks_break_run.log`; the driver does not start the scans unless it passes): `kc_break_compare.py` on planted 19-point scans gives d = 0 and STABLE for the same bracket, BREAKS (further off) for a change 0.02 away, STABLE for d = +0.010 exactly (the bar is inclusive) and for d = -0.010, **BREAKS for a tilted estimate whose bracket midpoint would be 0.010 away but whose det-linear estimate is 0.0145 away**, BREAKS (no k_c 55 root) with no k_c 55 change and with only a non-robust one, "not covered" with no k_c 63 change, OTHER with two k_c 63 changes, the extra k_c 55 change listed, and the orientation printed as the same or the opposite; its estimate equals xfkappa's own `changes()` on the real k_c 63 D 18.5 scan (1.677016) to 5e-7; `merge_repeat.py` merges an equal repeat and fails on a ln|det| difference of 1e-3, a flipped sign, no repeated point, a missing lambda, records at another k_c and the point three times, and writes no merged file then; `read_fine.py` at step 0.01 finds the planted change; `dip_fit3.py` passes its own selftest (a resolved pair; an unresolved one; a centre outside the window; a pure quartic polynomial; the minimum finder) and recovers a planted pair inside a 19-point scan, and applied to the two earlier dips flags the D 18.25 one (l0 1.658 outside its window, the quartic better) and passes the D 18.5 fine-scan one. All 32 pass; a first run had 4 cases wrong, all my planted cases (a tilt placed on the wrong point, a flipped sign equal to the existing one, an expected sign that was wrong), which I corrected, not a script.

## Run

`break_driver.sh` (launcher `launch_break.ps1`, BelowNormal): checks the pins, the worktree and both record lines, runs the planted controls, starts the two processes and the passive sampler (`samples.csv`, a sample every 60 s, only my `d18_hybsign.py` processes), then merges, reads, compares and fits. Blobs of the new scripts (mine): `kc_break_compare.py` fd057ccc, `merge_repeat.py` c9a827e4, `dip_fit3.py` 5e57ea24, `plant_checks_break.py` 96d151f4, `break_driver.sh` da3d52da, `launch_break.ps1` e5d5cdb0; `read_fine.py` fe01f2e5 and the sampler 9437f3ef as in `../kc55`. Output: `b63_scan.jsonl`, `b55_scan.jsonl`, `b63_scan_merged.jsonl`, `b55_scan_merged.jsonl`, `b63_raw.log`, `b55_raw.log`, `b63.log`, `b55.log`, `b63_merge.log`, `b55_merge.log`, `b63_reading.log`, `b55_reading.log`, `b63_dipfit.log`, `b55_dipfit.log`, `compare.log`, `rc_63`, `rc_55`, and one line per event in `../exits_1025.txt` (prefix `1025 kcbreak`); the last lines are `1025 kcbreak compare: ...` and `1025 kcbreak done`.

Estimate: at k_c 63 a point took 425 to 530 s with two processes running, at k_c 55 262 to 345 s: 20 evaluations take about 2.5 to 3 h at k_c 63 and 1.5 to 2 h at k_c 55. The 3 h progress post is due if the k_c 63 scan is still running then.

## Log

(appended below as the run goes)
