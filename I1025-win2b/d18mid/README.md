# I1025-win2b/d18mid: the hybrid sign scan at D 18.0625, k_c 63, on xfkappa's leap state (win2b)

Machine win2 (Windows 11, Intel Core Ultra 7 265K, 20 cores). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025

Written before the run, 2026-11-21 14:08 UTC by `date -u` (see the Log for the start).

## Order

The coordinator (hc, about 14:05 UTC 21 Nov, moved here from win2's queue so that it starts at once): between D 18 (two roots, 1.7750 minus-to-plus and 1.8074 plus-to-minus) and D 18.25 (one root, 1.7425) the pair either crossed or met. winb scans D 18.125 and win2 D 18.1875; this folder is D 18.0625. Use xfkappa's `d18_hybsign.py` (raw `I1025-mac/d18`, its scan command quoted from `lane_d185S.sh` below) on raw `I1025-mac/d18/sol_l1kc63Wm1025_D18.062500.npy` (k_c 63), lambda 1.70 to 1.95 at 0.01, with the noise test and the float64 sign, **two processes of 13 points with one point repeated in both as a check**, 4 threads each, BelowNormal, 8 h caps by exact pid, venv-md510. Window and reading go into this README first, raw `I1025-win2b/d18mid`. Post on #1025.

Reading (the coordinator's, fixed before the run): **report every robust change with its orientation and every ln|det| local minimum without a change.**

## Inputs (raw origin/main 7d54d10c, taken by `git show`, checked with `git hash-object --no-filters`; `in/pins.txt`, `in/pins_check.log`)

| item | raw path | blob |
|---|---|---|
| scanner | `I1025-mac/d18/d18_hybsign.py` | e089207a61fbd98614716abd309571cbc4888db2 |
| state | `I1025-mac/d18/sol_l1kc63Wm1025_D18.062500.npy` (33208 bytes) | f2307f0e8ffb4621b61f74450a920c652981d973 |
| record | `I1025-mac/d18/l1kc63Wm1025.jsonl`, the leap's D 18.0625 line (F 2.6753918623791614e-10, 2540 steps, kappa 0.7, u0 0.04, Ks 30, h 0.0625) | 08f4dbf367edba55814e5cf989ccd32a9a5dbe67 |
| the lane script quoted below | `I1025-mac/d18/lane_d185S.sh` | a019238b1dfbd91c7f258ea64d617c1edd2e9cb6 |
| merge (repeat check) | `I1025-win/d18mid/merge_d18mid_1025.py` (winb) | b8b47a44a050499b34bdac850cdcf282800959fd |
| reader | `I1025-win/d18mid/read_d18mid_1025.py` (winb) | 017ae1dabfb3d07d50ff2d885ad1f6af5db7bbca |
| xfkappa's D 18 and D 18.5 scans (controls of the reader) | `I1025-mac/d18/d18_scan_1025.jsonl`, `d185_scan_1025.jsonl` | ac80e9d5bd9c42b1ff10eea65d26258b3314021f, 90540dafdae9ff4093240cdc79d3ef8cc0506000 |

The merge and the reader are winb's, taken unchanged by blob, so that the D 18.0625 and D 18.125 scans are read by the same code (winb tested them on the two reference scans; I test them again below, with failing plants).

Code: worktree `D:/choptuik-1025p4` at 505d8399, clean (`P4_WT_MATTER`; xfkappa's lane requires the solver code to equal 505d8399, and the driver checks that `dss_ell.py`, `ell_ddm.py` and `ddnp.py` do), PY `C:/Users/nathan/Source/venv-md510` (multidouble 5.1.0), BelowNormal, 4 BLAS and rayon threads per process.

## The scan command, quoted

`d18_hybsign.py` docstring: `usage (venv-1025dd): d18_hybsign.py STUB.jsonl STATE.npy D LAMS OUT.jsonl   (LAMS comma-separated)`. It takes the record line at D from the first file (the leap's jsonl works as it is), rebuilds the record's discrete system (`|F|` within 1% and equal steps, else exit 3) and, at each lambda, prints the hybrid sign and ln|det| (`p4_hybrid.py`'s `sd()`, unchanged) with its 1e-15 noise test on blocks 0 to 11 (2 seeds, `default_rng(100 + k)`) and the plain float64 sign beside it. Each point is independent (the system is built once, each lambda has its own fixed seeds), so a split changes nothing per point.

xfkappa's D 18.5 scan in `lane_d185S.sh` (blob a019238b):

```
L=$($PY -c 'print(",".join(f"{1.55 + 0.01 * i:.2f}" for i in range(36)))')
timeout 21600 nice -n 10 $PY -u $Q/d18_hybsign.py $REC $ST 18.5 $L $SCAN < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d185_scan.log
```

Mine, per process (`d18mid_driver.sh`): `python -u in/d18_hybsign.py in/l1kc63Wm1025.jsonl in/sol_l1kc63Wm1025_D18.062500.npy 18.0625 <LAMS> <OUT>`, with `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=RAYON_NUM_THREADS=VECLIB_MAXIMUM_THREADS=4` and `P4_WT_MATTER`. Differences from the quoted lines, all outside the computation: the interpreter is venv-md510 (venv-1025dd on the Mac), there is no `nice` (BelowNormal by the launcher, inherited), no `timeout` (an exact-pid cap with a command-line check instead, as my other runs), and the warning filter (the same `grep -vE`) is applied to a copy of the raw log after the run (`scanA_raw.log`, `scanA.log`).

## Window and lambda lists, fixed before the run

Window: lambda 1.70 to 1.95 at 0.01, 26 points. It holds both D 18 roots (1.7750 and 1.8074), D 18.25's root (1.7425) and the region between; D 18.5's root is at 1.6772 (outside). This is the window winb uses at D 18.125, for comparison.

| process | lambda, in this order | points |
|---|---|---|
| A | 1.82, then 1.70, 1.71, ..., 1.81 | 13 |
| B | 1.82 again, then 1.83, 1.84, ..., 1.95 | 14 |

The repeated point (1.82, first in both, as winb's split) makes 27 evaluations for 26 distinct points. Each process has a cap of 28800 s (8 h), killed at the cap by the exact pid of its root process (`taskkill /T /F /PID`) after a check that the command line contains `d18_hybsign.py`; nothing else is killed, and a cap is not retried.

## Reading, fixed now (the coordinator's: report every robust change with its orientation and every ln|det| local minimum without a change)

Definitions, as implemented by the pinned reader `read_d18mid_1025.py`:

- a point is robust if the hybrid's sign survives its 1e-15 noise test (2 seeds); a change is two consecutive points of different hybrid sign, robust if both points are; its orientation is minus-to-plus or plus-to-minus;
- a ln|det| local minimum is an interior point whose ln|det| is below both neighbours'; it is "beside a change" if its sign differs from a neighbour's, else "WITHOUT a change"; a point at the scan's end that is below its only neighbour is listed as "at the scan edge";
- with two robust changes the reader also gives the gap between the brackets and centre to centre, beside D 18's 0.0325 (the step is 0.01, so the gap is known to about 0.01);
- the float64 sign beside the hybrid is information.

Nothing else is read into the scan. A change touching a point that fails its noise test is listed and not counted. The numbers go into the post as the reader prints them.

## Repeat check, fixed now

At the repeated lambda 1.82 the two records (A's and B's) must have the same hybrid sign and ln|det| equal to 1e-6 (the pinned `merge_d18mid_1025.py`). The merged 26-point scan is written, and the reader run, only if this check passes and every lambda from 1.70 to 1.95 is present. The result is written into this README after the run.

## Controls, before the run

`plant_checks.py` runs the pinned merge and reader on planted scans and on xfkappa's D 18 and D 18.5 scans, 18 cases (`plant_checks.log`, rerun by the driver as `plant_checks_run.log`; the driver does not start the scan unless it passes): the merge passes on equal repeats and fails on a ln|det| difference of 1e-3, on a flipped repeat sign, with no repeated point, with lambda 1.95 missing, and writes no merged file when it fails; the reader finds the planted minus-to-plus and plus-to-minus changes and the gap, reports a minimum next to a change as "beside a change" and a minimum with the same sign on both sides as "WITHOUT a change", lists a change with a non-robust point as "NOT ROBUST" without the gap line, swaps the orientation when the signs are negated, and on xfkappa's real scans gives winb's quoted readings (D 18: minus-to-plus in (1.77, 1.78) and plus-to-minus in (1.80, 1.81), centre to centre 0.030; D 18.5: minus-to-plus in (1.67, 1.68), no second change). All 18 pass.

## Run

`d18mid_driver.sh` (launcher `launch_d18mid.ps1`, BelowNormal): checks the pins, the worktree and the record line, runs the planted controls, starts the two processes and a passive sampler, then merges and reads. A sampler (`sample_d18mid.ps1`) writes every 60 s the machine cpu %, commit and free physical memory, and each `d18_hybsign.py` process's working set, private bytes, cpu seconds and priority, to `samples.csv` (reads only; ended by its exact pid). Output: `scanA.jsonl`, `scanB.jsonl`, `scan_merged.jsonl`, the logs `scanA_raw.log`, `scanB_raw.log`, `scanA.log`, `scanB.log`, `merge.log`, `reading.log`, `rc_A`, `rc_B`, and one line per event in `../exits_1025.txt` (prefix `1025 d18mid`). The driver's last lines are `1025 d18mid reading: ...` and `1025 d18mid done`. No RESUME: a stopped scan is reported, not retried.

Estimate (made before the run): not known on this machine; it came out at 425 to 507 s a point (see Result).

## Log

(appended below as the run goes)

- 2026-11-21 14:08:49 UTC: both scan processes started (A root pid 34808, B root pid 35752; the driver's pre-checks, including the 18 planted controls, passed at 14:08:48). Record system ok on both: |F| 2.6777188645e-10 against the record's 2.6753918624e-10, steps 2540 against 2540.
- 2026-11-21 15:45:43 UTC: A ended, exit 0, 5814 s, not capped. 15:53:01 UTC: B ended, exit 0, 6252 s, not capped. 425 to 507 s a point. The sampler (`samples.csv`) was ended by its exact pid at 15:53:02.
- 2026-11-21 15:53:04 UTC: merge and reading by the driver (`merge.log`, `reading.log`), done.

## Result (15:53 UTC)

**Repeat check (lambda 1.82, first in both halves): PASS.** Hybrid sign +1 in A and in B; ln|det| -1917.7593852316775 in both, difference 0.000e+00 (bar 1e-6); noise robust in both; float64 sign -1 in both; 506 s and 507 s. The merged 26-point scan was written (`scan_merged.jsonl`; the repeated point from A).

**Reading (the pinned reader's output, `reading.log`):**

- every point is noise robust (none fails its 1e-15 noise test);
- hybrid signs: minus at 1.70 to 1.79, plus at 1.80 to 1.95;
- **one robust change: (1.79, 1.80), minus-to-plus**; no other change in the window (no plus-to-minus change between 1.80 and 1.95, and none between 1.70 and 1.79);
- ln|det| local minima: at 1.79 (ln -1921.620358) **beside the change**; at 1.70 (ln -1918.890716) **at the scan edge**; **none WITHOUT a change**;
- the reader prints no gap line (that needs two robust changes);
- float64 sign differs from the hybrid's at 9 of 26 points (1.80 to 1.88, where the hybrid is plus and float64 minus; information).

Reported as the order fixes it, nothing further read: the minus-to-plus change at D 18 (bisected 1.7749781, in (1.77, 1.78) on xfkappa's scan) is in (1.79, 1.80) here; the plus-to-minus change that D 18 had in (1.80, 1.81) is not in 1.70 to 1.95 here; D 18.25's root (1.7425) is inside the window and shows no change at 1.74. The scan does not show what lies below 1.70, where the ln|det| minimum at the edge is.

**cpu and memory (`samples.csv`, a sample every 60 s, 102 samples 14:08 to 15:52 UTC).** My two `d18_hybsign.py` processes (python child of each root; the roots are launcher stubs): A peak working set 1.02 GiB, private 1.62 GiB, 8541 cpu-s in 5814 s; B peak working set 0.62 GiB, private 1.32 GiB, 9208 cpu-s in 6252 s; both BelowNormal throughout; the two together at most 1.64 GiB working set and 2.82 GiB private in one sample. Machine: cpu mean 38.1% (1 s samples), max 69.4%; commit 45.5 to 50.4 of 101.5 GiB; free physical at least 50.5 GiB. Two other `d18_hybsign.py` processes (not mine; launcher stubs 15348 and 18128, pythons 34584 and 10848, from 14:28 UTC, still running at 15:52) shared the machine and are in the machine figures.

---

# Part 2: the same D 18.0625 state above the window, lambda 1.95 to 2.35 (win2b)

Written before the run (the push was at 15:58:30 UTC by `date -u`; I typed 15:59 before reading the clock, corrected here after the start). Part 1 above (lambda 1.70 to 1.95) is done; its files are unchanged, and the files of this part have the prefix `up_`.

## Order

The coordinator (hc, about 15:58 UTC 21 Nov): where D 18's plus-to-minus root went. At D 18 it sat at 1.8074 and at D 18.0625 there is none in 1.70 to 1.95. Scan the same D 18.0625 state above the window: lambda 1.95 to 2.35 at 0.01 (41 points), same script, noise test, float64 sign, two processes with 1.95 repeated in both as the check (it also repeats Part 1's 1.95), 4 threads each, BelowNormal, 8 h caps. Window and reading go into this README first, raw `I1025-win2b/d18mid`. Post on #1025.

Reading (the coordinator's, fixed before the run): **a robust plus-to-minus change places the root, which then rose at least 2.3 per unit D. None up to 2.35 means it is not there.** xfkappa's check of the determinant's sign convention across these states reports about 16:20 UTC, and **all orientation readings wait for it**: this post reports the orientation as the reader prints it (the det sign of this scan's own convention) and reads nothing from the orientation until that check is in.

## Inputs

The same as Part 1 (`in/pins.txt`, `in/pins_check.log`, all blobs checked again by the driver before the start): scanner `d18_hybsign.py` e089207a, state `sol_l1kc63Wm1025_D18.062500.npy` f2307f0e, leap record `l1kc63Wm1025.jsonl` 08f4dbf3 (D 18.0625 line: F 2.6753918623791614e-10, 2540 steps), winb's reader `read_d18mid_1025.py` 017ae1da. Worktree `D:/choptuik-1025p4` at 505d8399, venv-md510, 4 BLAS and rayon threads per process, BelowNormal. Plus Part 1's merged scan `scan_merged.jsonl` (blob 8b0c3bfc01d19768df4a20de2e2f0d8017887089), for the 1.95 comparison.

New scripts of this part (mine; blobs): `merge_up.py` 3c648aa9, `rate_up.py` af1d97cd, `plant_checks_up.py` 00e68429, `d18up_driver.sh` 5e4d74e4 (launcher `launch_d18up.ps1`), the sampler `sample_d18mid.ps1` 9437f3ef (unchanged). winb's `merge_d18mid_1025.py` is not used here: it hard-codes the window 1.70 to 1.95. `merge_up.py` has the same logic and bar with this window.

## Window and lambda lists, fixed before the run

Window: lambda 1.95 to 2.35 at 0.01, 41 points. D 18's upper root was 1.8074339746 (my hybrid root, comment 7062464335); a root at 1.95 or above at D 18.0625 means a rise of at least (1.95 - 1.8074339746) / 0.0625 = 2.281 per unit D at the window's lower end; the coordinator's "at least 2.3" is that figure rounded, and the window's top, 2.35, is a rise of 8.7 per unit D.

| process | lambda, in this order | points |
|---|---|---|
| A | 1.95, then 1.96, 1.97, ..., 2.15 | 21 |
| B | 1.95 again, then 2.16, 2.17, ..., 2.35 | 21 |

The repeated point (1.95, first in both) makes 42 evaluations for 41 distinct points. Caps 28800 s (8 h) each by the exact pid of the root process (`taskkill /T /F /PID`) after a check that its command line contains `d18_hybsign.py`; a cap is not retried.

## Reading, fixed now

As Part 1 (the pinned reader, the same definitions): every robust change with its orientation, and every ln|det| local minimum without a change, with the added line of `rate_up.py`:

- a **robust plus-to-minus change** (two consecutive points, plus then minus, both passing the 1e-15 noise test) places the root in that bracket; `rate_up.py` prints the rise from D 18's root 1.8074339746330934 over 0.0625 in D, per unit D, at the bracket's two ends;
- **no robust plus-to-minus change from 1.95 to 2.35**: the root is not there (the coordinator's reading); a change that touches a non-robust point is listed and not counted;
- other changes (minus-to-plus), ln|det| minima and the float64 sign are reported as the reader prints them;
- orientation readings wait for xfkappa's sign-convention check (see the Order).

## Repeat check, fixed now

At the repeated lambda 1.95 the two records (A's and B's) must have the same hybrid sign and ln|det| equal to 1e-6 (`merge_up.py`; it is the gate). The merged 41-point scan is written, and the reader run, only if this check passes, every record is at D 18.0625 and every lambda from 1.95 to 2.35 is present. In addition `merge_up.py` compares A's 1.95 with Part 1's 1.95 (sign +1, ln|det| -1913.464809719331, noise robust, float64 +1) at the same bar and prints AGREES or DIFFERS; that is information, not a gate. The results are written into this README after the run.

## Controls, before the run

`plant_checks_up.py`, 25 cases (`plant_checks_up.log`, rerun by the driver as `plant_checks_up_run.log`; the driver does not start the scan unless it passes): `merge_up.py` merges equal repeats and fails on a ln|det| difference of 1e-3, on a flipped repeat sign, with no repeated point, with a second point in both files, with lambda 2.35 missing and with records at another D, and writes no merged file then; it reports a prior scan that agrees and one that differs by 5e-3 (the merge still written); `rate_up.py` finds a planted plus-to-minus change in (2.10, 2.11) and prints its rise (4.681 to 4.841 per unit D), says "the root is not there" for a scan without one, for a change with a non-robust point and for a minus-to-plus change only, and reads xfkappa's D 18 scan's own plus-to-minus change; the pinned reader finds the planted changes, orientation and minimum "WITHOUT a change", and gives winb's quoted readings on xfkappa's D 18 scan. All 25 pass.

## Run

`d18up_driver.sh` (launcher `launch_d18up.ps1`, BelowNormal): checks the pins, the worktree, the record line and the first window's scan blob, runs the planted controls, starts the two processes and the passive sampler (`up_samples.csv`, a sample every 60 s, only the processes whose command line holds this folder's `d18_hybsign.py` path, so win2-build's own scan on this machine is not in it), then merges, reads and runs `rate_up.py`. Output: `up_scanA.jsonl`, `up_scanB.jsonl`, `up_scan_merged.jsonl`, `up_scanA_raw.log`, `up_scanB_raw.log`, `up_scanA.log`, `up_scanB.log`, `up_merge.log`, `up_reading.log`, `up_rate.log`, `up_rc_A`, `up_rc_B`, and one line per event in `../exits_1025.txt` (prefix `1025 d18up`); the last lines are `1025 d18up reading: ...`, `1025 d18up rate: ...` and `1025 d18up done`.

Estimate (from Part 1: 425 to 507 s a point with two processes): 21 points take about 2.5 to 3 h per process, in parallel; the 3 h progress post is due if it is still running then.

## Log (Part 2)

(appended below as the run goes)
- 2026-11-21 15:58:51 UTC: both scan processes started (A root pid 20080, B root pid 8028; pre-checks including the 25 planted controls passed at 15:58:51). Record system ok on both: |F| 2.6777188645e-10 against the record's 2.6753918624e-10, steps 2540 against 2540.
- 2026-11-21 18:33:55 UTC: B ended, exit 0, 9304 s, not capped. 18:34:07 UTC: A ended, exit 0, 9316 s, not capped. 423 to 532 s a point. The sampler (`up_samples.csv`, my processes only) was ended by its exact pid at 18:34:08.
- 2026-11-21 18:34:08 to 18:34:10 UTC: merge, reading and rate by the driver (`up_merge.log`, `up_reading.log`, `up_rate.log`), done. In the driver's `exits_1025.txt` line for the merge the repeat-check segment is empty: my `cut -c1-200` truncated that line before the `sed` that takes its verdict (the same in Part 1's line). The verdict is in `up_merge.log`.

## Result (Part 2, 18:35 UTC)

**Repeat check (lambda 1.95, first in both halves): PASS.** Hybrid sign +1 in A and in B; ln|det| -1913.464809719331 in both, difference 0.000e+00 (bar 1e-6); noise robust in both; float64 sign +1 in both; 491 s and 485 s. **Comparison with Part 1's 1.95 (information): AGREES**, sign +1 and ln|det| -1913.464809719331, difference 0.000e+00 (a different pair of processes, two hours apart). The merged 41-point scan was written (`up_scan_merged.jsonl`; the repeated point from A).

**Reading (the pinned reader and `rate_up.py`, as fixed before the run):**

- every point is noise robust (none fails its 1e-15 noise test);
- hybrid signs: plus at 1.95 to 2.33, minus at 2.34 and 2.35;
- **one robust change: (2.33, 2.34), plus-to-minus**, so by the coordinator's reading the root is placed there;
- `rate_up.py`: from D 18's root 1.8074339746330934 the rise is 0.5226 to 0.5326 in 0.0625 D, **8.361 to 8.521 per unit D** (the ordered bar was at least 2.3 per unit D; 2.281 at the window's lower end);
- ln|det| local minima: at 2.33 (ln -1906.677998) beside the change; at 1.95 (ln -1913.464810) at the scan edge; none without a change. The edge minimum at 1.95 is the window's end: with Part 1's 1.94 (ln -1913.734, plus) the combined scan has no minimum there;
- no gap line (it needs two robust changes in one scan);
- the float64 sign differs from the hybrid's at 3 of 41 points (2.31, 2.32, 2.33; information);
- orientation: as the reader prints it, plus-to-minus, the orientation of D 18's upper root; **the orientation reading waits for xfkappa's sign-convention check** (not read here).

Beside, as facts and not read: the minus-to-plus change that was at 1.7749781 at D 18 is in (1.79, 1.80) at D 18.0625 (Part 1), a rise of 0.240 to 0.400 per unit D (the bracket (1.79, 1.80) against 1.7749781 over 0.0625 D).

**cpu and memory (`up_samples.csv`, a sample every 60 s, 153 samples 15:58:51 to 18:34:06 UTC; my processes only).** A's python child (pid 9064): peak working set 0.84 GiB, private 1.56 GiB, 13770 cpu-s in 9316 s; B's (pid 19084): peak working set 0.99 GiB, private 1.62 GiB, 13761 cpu-s in 9304 s; BelowNormal throughout (the roots are launcher stubs); the two together at most 1.59 GiB working set and 2.88 GiB private in one sample. Machine: cpu mean 32.8% (1 s samples), max 65.0%; commit 47.2 to 50.1 of 101.5 GiB; free physical at least 50.3 GiB.
