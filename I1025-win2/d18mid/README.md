# I1025-win2/d18mid: xfkappa's hybrid sign scan at D 18.1875 (k_c 63, ell = 1), lambda 1.70 to 1.95 at 0.01, two processes, on win2

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session, beside win2b's jobs. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task: the coordinator's hc of 2026-11-21
(~13:30 UTC), the follow-on after the #1064 precross_natural rungs. Between D 18 (two roots, 1.775 minus-to-plus and 1.807 plus-to-minus) and D 18.25 (one root, 1.7425) the pair either crossed or met. The leap saved states between them;
winb scans D 18.125; this folder scans D 18.1875 (D 18.0625 first came to me and went to win2b, see the next section). With winb's D 18.125 and win2b's D 18.0625, the gap against D shows whether the pair approaches to a meeting or passes through (the coordinator reads that).

## Queue change, before any scan (2026-11-21 14:06 UTC)

The coordinator's hc (~14:00 UTC): win2b takes D 18.0625 now; I run only D 18.1875, as two processes of 13 points with one point repeated in both as a check (winb does the same at D 18.125); change the driver before it starts and note it here.

- The first driver (bash pid 21684, waiting for the #1064 precross_natural `all.done`) was stopped by its exact pid at 14:05:23 UTC, before any scan or any `d18_hybsign.py` process; its script is kept as `stopped_before_start/run_d18mid_two_D.sh`. Its pin and reader controls had passed (`selftest_read*.txt`, the first lines of `exits_d18mid.txt`). The pre-run post (#1025 comment 7063372421) describes that first plan; the change is posted in a second comment before the run.
- The new driver `run_d18mid.sh` runs D 18.1875 only: **process A** lambda 1.70 to 1.82 (13 points); **process B** the check point 1.75 first, then lambda 1.83 to 1.95 (13 points). Together they cover all 26 points of the window, and 1.75 is in both (A has it among its 13), so the reader's repeated-point rule compares the two processes (same sign, ln|det| within 1e-6).
- **A conflict, named:** 13 + 13 points with one repeated would cover 25 distinct points of the 26-point window (1.70 to 1.95 at 0.01) and drop one end, and the top end matters for where the plus-to-minus root went. I kept the whole window, so process B has 14 evaluations (13 + the check point) and A has 13: 27 evaluations in all. I told the coordinator by hc at the same time; a correction before the scans start would change `run_d18mid.sh` only.


## Setup (written 2026-11-21 13:32 UTC, before any run)

| | |
|---|---|
| scan command (xfkappa's, `I1025-mac/d18/lane_d185S.sh`, line 34, quoted) | `timeout 21600 nice -n 10 $PY -u $Q/d18_hybsign.py $REC $ST 18.5 $L $SCAN`, with `L` = lambda 1.55 to 1.90 at 0.01 (`1.55 + 0.01 * i`, 36 points), `OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4`, `P4_WT_MATTER=$W`, cwd the worktree's `solver/matter` |
| my scan command | `python.exe -u D:/choptuik-large-d-raw-push/I1025-mac/d18/d18_hybsign.py REC ST 18.1875 L OUT`, REC = `.../l1kc63Wm1025.jsonl`, ST = `.../sol_l1kc63Wm1025_D18.187500.npy`; process A: L = `1.70,1.71,...,1.82` (13 points), OUT = `scan_D18.1875_A.jsonl`; process B: L = `1.75,1.83,1.84,...,1.95` (the check point, then 13 points), OUT = `scan_D18.1875_B.jsonl`; the logs (`scan_D18.1875_A.log`, `_B.log`) carry the full lines; 4 threads each (the same four environment variables), `P4_WT_MATTER=D:/choptuik-i1025d/solver/matter`, BelowNormal, venv-md510 instead of xfkappa's venv-1025dd |
| inputs (read only, raw main) | `I1025-mac/d18/d18_hybsign.py` blob e089207a (xfkappa's pin), the state `sol_l1kc63Wm1025_D18.187500.npy` (3f06b92e, 33208 bytes), the record `l1kc63Wm1025.jsonl` (08f4dbf3); the script exits 3 if the state is not its record's system (|F| and steps compared), the same check as the Mac's |
| reader (xfkappa's, unchanged) | `d18d_read.py` blob 6b608903 with `d185_scan_read.py` 7c9d400f and `d18c_read.py` 1383470f (pins checked by the driver); `gap_table.py` (new, here) imports its functions |
| solver code | worktree `D:/choptuik-i1025d` at 48c36355: `dss_ell.py`, `ell_ddm.py`, `ddnp.py` equal 505d8399's (xfkappa's pin) and `ell_delta.py` equals 48c36355's, checked by the driver (it refuses otherwise) |
| python | venv-md510 (Python 3.14.10, numpy 2.5.4, multidouble 5.1.0 at 8c4360ac; the Mac's venv-1025dd differs) |
| run | `run_d18mid.sh WAIT_FILE`: pins and controls first; the scans start when `../../I1064-win2/precross_natural/all.done` exists (the follow-on, the #1064 rungs are not disturbed); the two processes side by side, each capped at 28800 s (8 h) by the exact root pid (`taskkill /T /F /PID` after the command line is checked); then the reader on the two files together and `gap_table.py` |
| memory | `mem_watch.ps1` and `commit_watch.ps1`: alert-only, 30 s samples, kill nothing. I tell the coordinator at commit over 99 GB, a page file up by 2 GB, or available under 1 GB for 5 min. win2b's jobs share the machine |

## Windows (fixed before the run)

- D 18.1875, k_c 63, ell = 1, the leap's saved state (D 18.0625 is win2b's, D 18.125 winb's).
- lambda **1.70 to 1.95 at 0.01**: 26 points, as two processes (A: 1.70 to 1.82, B: 1.83 to 1.95), with the check point 1.75 in both. The earlier scans covered 1.55 to 1.90 (D 18, D 18.5) and 1.55 to 1.95 (D 18.25).
- Each point: the hybrid sign (float64 blocks 0-11, double-double block 12), the noise test (1e-15 relative noise on blocks 0-11, 2 seeds), the float64 sign beside.

## Readings fixed before the run (the coordinator's, with xfkappa's reader's definitions)

1. **Every robust sign change is reported with its orientation** (the sign below the root to the sign above it), its bracket and its estimator range. A change is robust when both of its grid points are noise-robust; a change that touches a non-robust point is listed and not counted. The estimator range is the span of four estimates inside the bracket (information, not a bound).
2. **Every ln|det| local minimum without a sign change beside it is reported** (the reader's definition: a minimum of the hybrid ln|det| not beside a sign change; the scan's end points cannot hold one), with its depth.
3. **The gap**: for a D with two robust changes, the gap interval between the lower root's and the upper root's estimator ranges, listed beside D 18, D 18.25 and D 18.5 (`gap_table.py`, from the Mac scans of `I1025-mac/d18`). With win2b's D 18.0625 and winb's D 18.125 the coordinator reads the gap against D (approach to a meeting, or passing through). No reading of mine decides it.
4. A cap that fires, or a scan that exits non-zero, is a result: the points done are read and reported as partial; nothing is rerun or loosened. Exit 3 (not the record system) stops that scan.
5. Seconds per point are reported (this machine, this load: win2b's jobs on the machine, 4 threads each, BelowNormal), not compared with xfkappa's.

## Controls

- the reader's selftest (`d18d_read.py selftest`, exit 0) and `--mutate=orient` (exit 1), run by the driver before the scans;
- `gap_table.py` reads the D 18 and D 18.25 scans of the Mac and must give roots near 1.775 (- to +) and 1.807 (+ to -), and one root near 1.7425 (- to +), each within 0.005 (the numbers in the hc); it exits 1 otherwise (tested before the launch: passes on the real scans, fails when the expected 1.775 is changed to 1.80, and reads planted scans with roots 1.7610 and 1.8123 as 1.761011 and 1.811688 to 1.812539, and the two-process planted scan with roots 1.7480 and 1.9040 as 1.747772 and 1.903387);
- the scan's own record-system check (exit 3 if the state does not reproduce its record's |F| and step count).
- the repeated point 1.75 (in both processes): same sign and ln|det| within 1e-6 (the reader's rule); a disagreement is STOP-level, no reading (`gap_table.py` exits 2; tested on planted scans: an agreeing repeat passes, a repeat off by 1e-3 in ln|det| exits 2).

## Result (scans 2026-11-21 14:27:38 to 16:12:19 UTC)

Both processes ran to the end (exit 0, no cap): A 13 points in 5760 s (421 to 487 s per point), B 14 points in 6281 s (424 to 493 s per point), 4 threads each, BelowNormal, win2b's scans on the machine. Both passed the scan's own
record-system check (|F| 2.7545108188e-10 against the record's 2.7479600600e-10, steps 2519 = 2519). All 26 points of the window are noise-robust. The reader (`d18d_read.py`, blob 6b608903) on the two files together (`read_D18.1875.log`):

| reading (the coordinator's) | D 18.1875, lambda 1.70 to 1.95 at 0.01 |
|---|---|
| robust sign changes | **one**: in (1.75, 1.76), **plus to minus**; det-linear estimate 1.754208, estimator range [1.754208, 1.754399] (information, not a bound) |
| changes touching a non-robust point | none |
| ln\|det\| local minima without a sign change | **none** |
| signs | `+` at 1.70 to 1.75, `-` at 1.76 to 1.95 |
| repeated point 1.75 (A and B) | agree: sign +1 in both, ln\|det\| -1918.0546856478 in both (difference 0.0), float64 sign -1 in both; the check passes |
| float64 beside | 9 float64 sign changes in the window, and float64 differs from the hybrid at 6 of 26 points (as at the Mac's D 18 and D 18.25) |

`points_D18.1875.md` lists the 26 points (hybrid sign and ln|det|, the two noise signs, float64, seconds). `gap_table.md` (the controls on the Mac's D 18 and D 18.25 scans pass) lists the pair beside D 18, D 18.25 and D 18.5:

| D | robust changes over the window (orientation, bracket, det-linear, range) | gap interval |
|---|---|---|
| 18 | - to + (1.77, 1.78) 1.775263 [1.774793, 1.775263]; + to - (1.80, 1.81) 1.806298 [1.806298, 1.807635] | [0.031035, 0.032842] |
| **18.1875** | **+ to - (1.75, 1.76) 1.754208 [1.754208, 1.754399]** | only one root: none |
| 18.25 | - to + (1.74, 1.75) 1.742506 [1.742506, 1.742860] | none |
| 18.5 | - to + (1.67, 1.68) 1.677016 [1.677016, 1.677225] | none |

For the gap against D the coordinator combines this with win2b's D 18.0625 and winb's D 18.125. From this folder alone: at D 18.1875 the window shows one root, in the position of D 18's lower root continued (1.7753 at D 18, 1.7542 at D 18.1875, 1.7425 at D 18.25, 1.6770 at D 18.5), and no second root anywhere in 1.76 to 1.95 (D 18's upper root was at 1.8063 to 1.8076).

**An orientation difference to flag, not explained.** The one root here reads plus to minus, while the lower root at D 18 and the single root at D 18.25 and D 18.5 read minus to plus. At fixed lambda the sign below the root alternates from state to state:

| D | sign at 1.70 | at 1.75 | at 1.80 | at 1.85 | at 1.90 |
|---|---|---|---|---|---|
| 18 | - | - | + | - | - |
| 18.1875 | + | + | - | - | - |
| 18.25 | - | + | + | + | + |
| 18.5 | + | + | + | + | + |

(D 18.5's root is at 1.677, minus to plus, so it reads + from 1.70.) So the D 18.1875 scan reads as D 18.25's with every sign negated, while its root position follows the trajectory of the lower root. I do not know whether the overall sign of the hybrid determinant is a convention that can flip between states (or between this machine's multidouble 5.1.0 and the Mac's venv-1025dd), or whether the orientation is real; a signs-only reading of orientation depends on this. Nothing here tests it. A possible control, not run (not ordered): one point of the Mac's D 18 scan (lane_d18b.sh: `d18_hybsign.py STUB STATE 18 1.8 OUT`, the Mac read +1, ln|det| -1925.0182289868) on this machine with venv-md510, which separates a machine or version sign convention from the state.

Memory: lowest available 50.4 GB, peak commit 50.4 GB of 101.47 GB, page file peak 2610 MB (as at the start); no alert fired (no `alerts.log`). The reader blobs in `I1025-mac/d18` at the scan end equal the pins (e089207a, 6b608903, 7c9d400f, 1383470f), so the readings above are from the pinned scripts (copies in `pinned/`).
Slips: none in the scan. The first driver stopped before any scan for the queue change (above).
