# I1025-win2/d185map: the k_c 63 map at D 18.5 over lambda 1.00 to 2.60: win2's two windows (A = 2.40 to 2.60, B = 1.00 to 1.55) beside xfkappa's scans (1.55 to 2.40)

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session, beside win2b's jobs. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task: the coordinator's hc of 2026-11-21 (~19:20 UTC),
after `../d18hi/` (post 7067698486): complete the k_c 63 map at D 18.5 for the k_c comparison win2b runs at k_c 55 (1.55 to 2.40). xfkappa's scans at this state cover 1.55 to 2.40 (one root, 1.6772; and an odd count in 2.40 to 2.60 by the
sign-convention reference). Scan the same state over two windows side by side: A = 2.40 to 2.60 and B = 1.00 to 1.55, at 0.01, with `d18_hybsign.py`, the noise test and the float64 sign; 1.55 and 2.40 first, as repeats of xfkappa's points, which must agree.

## Restart of window B, split in two (2026-11-21 19:32 UTC)

The coordinator's hc (~19:32 UTC, 2 min after the launch): **split B now; keep A running; restart B as two processes** (B1 = 1.55 repeat, then 1.28 to 1.54; B2 = 1.55 repeat, then 1.00 to 1.27), 4 threads each, the same repeat gate and caps; record the restart, its time and the part of B's work lost here.
The Setup, Windows and timing below were written before the launch and describe the first run; the changes are these:

- **B1 and B2 started at 19:32:45 UTC** (`b_split/run_b_split.sh`, bash pid 19828; B1 root pid 27388, 28 evaluations: 1.55, 1.28 to 1.54; B2 root pid 36012, 29 evaluations: 1.55, 1.00 to 1.27), 4 threads each, BelowNormal, caps 28800 s by the exact root pid, the same pins and controls,
  their own repeat gate (`repeat_check_b.py`: both first points, lambda 1.55, against xfkappa's: same sign, ln|det| within 1e-2; a disagreement kills both B scans by exact pid), their own watchers (`b_split/mem.log`, `commit.log`). The command is the first run's with only L and OUT changed (`b_split/scan_B1.log`, `scan_B2.log` carry the lines).
- **The first run's window B (root pid 26404, started 19:30:16) was stopped by its exact pid at 19:39:00 UTC** (`stop_old_B.sh`, `exits_d185map.txt`), not at once: the first driver's repeat gate needs B's first point to pass, and killing B earlier would have ended with that gate killing A after 2700 s ('no first points'). The first run's gate passed at 19:38:55 UTC
  (A 2.40: +1, ln|det| -1887.295413402769 against xfkappa's -1887.295420450760, difference +7.0e-6; B 1.55: -1, -1899.880897756068 against -1899.880900137170, difference +2.4e-6; both agree, `repeat_check.txt`). **A (root pid 27396) was not touched** and keeps running under the first driver (`run_d185map.sh`, bash pid 34024).
- **Work lost:** the stopped B had run 526 s: 1 of its 56 evaluations done (the 1.55 repeat, 495 s), kept as `scan_B_stopped.jsonl` / `scan_B_stopped.log` (a third evaluation of 1.55, used only to compare duplicates). The 1.00 point, started within about 35 s before the stop, was lost. Nothing else of B's 55 new points existed. So about 8.8 min of one process, of which 495 s are a kept data point.
- The first driver's final steps (`map_read.py`, `points_table_map.py`) were renamed `*_v1.py` before they could run on A and the stopped B; when A ends that driver will log two failed calls and touch `all.done` (which stops its watchers; `b_split/` has its own). The final reading is `map_read2.py` (A, B1 and B2 with xfkappa's scans; the repeats 2.40 and 1.55 (twice) checked by `repeat_check.py`'s rule; the stopped B's duplicate points compared at the same-machine bar 1e-6) and `points_table_map2.py`, run after A, B1 and B2 have all ended.
- **Load:** A + B1 + B2 (12 threads) beside win2b's four k_c 55 scans (16 threads) is 28 threads on 20, so the per-point times may rise above the earlier 440 s; expected ends: A about 22:10 UTC, B1 and B2 about 23:00 to 23:30 UTC, against the 8 h caps (03:30 UTC).

## Setup (written 2026-11-21 19:29 UTC, before any run)

| | |
|---|---|
| state and record | `I1025-mac/d18/sol_l1kc63Wm1025_D18.500000.npy` (blob 33c1a58b; `..._D18.5000.npy` is the same blob) and its leap record line in `l1kc63Wm1025.jsonl` (blob 08f4dbf3; the D 18.5 line: |F| 2.7672415504278416e-10, steps 2461), k_c 63, ell = 1; the script exits 3 if the state does not reproduce the record |
| xfkappa's scans at this state (copies in `inputs/`, blobs in `inputs/BLOBS.txt`, equal to the raw files, checked by the driver) | `d185_scan_1025.jsonl` 1.55 to 1.90 (36 points), `d185_scanhi_1025.jsonl` 1.90 to 2.10 (21), `d185_scanup_1025.jsonl` 2.10 to 2.40 (31); one robust change, (1.67, 1.68) minus to plus (1.677016, bisected root 1.6772090983), and + at all 31 points of 2.10 to 2.40; the sign-convention reference `d18_refsign_1025.jsonl`: D 18.5 is -1 at lambda 1.20 and -1 at 2.60 |
| the repeats | lambda 2.40: sign +1, ln|det| -1887.2954204507596 (`d185_scanup_1025.jsonl`); lambda 1.55: sign -1, ln|det| -1899.8809001371699 (`d185_scan_1025.jsonl`) |
| command | xfkappa's `d18_hybsign.py REC ST 18.5 L OUT` (blob e089207a), as in `../d18mid/` and `../d18hi/` (comments 7063372421, 7065529024); `P4_WT_MATTER=D:/choptuik-i1025d/solver/matter`, 4 threads each, BelowNormal, venv-md510 (multidouble 5.1.0); **window A**: L = 2.40, 2.41, ..., 2.60 (the repeat first, then 20 new points; 21 evaluations), OUT = `scan_A.jsonl`; **window B**: L = 1.55, 1.00, 1.01, ..., 1.54 (the repeat first, then 55 new points; 56 evaluations), OUT = `scan_B.jsonl`; each capped at 28800 s (8 h) by the exact root pid (`taskkill /T /F /PID` after the command line is checked) |
| timing | the d18mid and d18hi scans took 420 to 513 s per point (mean about 440 s) under the same load (win2b's four k_c 55 scans, 16 threads, on the machine): A about 21 x 440 s = 2.6 h, **B about 56 x 440 s = 6.9 h against the 8 h cap** (a mean above 514 s per point would hit the cap in B's last points, which would then be reported as partial) |
| solver code | worktree `D:/choptuik-i1025d` at 48c36355: `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's and `ell_delta.py` equals 48c36355's (checked by the driver, which refuses otherwise) |
| reader | xfkappa's `d18d_read.py` (blob 6b608903, with `d185_scan_read.py` 7c9d400f and `d18c_read.py` 1383470f; the copies in `../d18mid/pinned/`, blobs checked by the driver), unchanged; `map_read.py` (new, here) feeds it |
| run | `run_d185map.sh`: pins and controls, then the two windows side by side, with a **repeat gate**: when both first points exist (about 8 min), `repeat_check.py` compares them with xfkappa's; on a disagreement the driver kills both scans by their exact root pids and stops. After the scans: `map_read.py` and `points_table_map.py` |
| memory | `mem_watch.ps1`, `commit_watch.ps1`: alert-only, 30 s samples, kill nothing. I tell the coordinator at commit over 99 GB, a page file up by 2 GB, or available under 1 GB for 5 min |

## Windows (fixed before the run)

- D 18.5, k_c 63, the leap's saved state. **Window A: lambda 2.40 to 2.60 at 0.01** (2.40 repeats xfkappa's point; 2.41 to 2.60 are new, 20 points). **Window B: lambda 1.00 to 1.55 at 0.01** (1.55 repeats xfkappa's point; 1.00 to 1.54 are new, 55 points).
  Together with xfkappa's 1.55 to 2.40 this covers D 18.5 over 1.00 to 2.60 (the junctions: 1.54|1.55 and 2.40|2.41 are read with xfkappa's points).
- Each point: the hybrid sign (float64 blocks 0-11, double-double block 12), the noise test (1e-15 relative noise on blocks 0-11, 2 seeds), the float64 sign beside.

## Readings fixed before the run (the coordinator's, with xfkappa's reader's definitions)

1. **The repeats must agree** (the coordinator's). I fix the criterion as the control's: **the same sign, ln|det| within 1e-2 of xfkappa's**, both noise-robust. The reader's same-machine repeat bar (1e-6) does not apply across machines (the control at D 18 differed by 8.9e-4), so the two repeats are checked by `repeat_check.py` and taken out of the files given to the reader.
   If a repeat disagrees (the gate, or `map_read.py`): the scans stop (or the reading is withheld) and I report it for the coordinator's decision (AGENTS.md: a control that fires on real data stops the work).
2. **Every robust sign change with its bracket and orientation**, with the estimator range and the delta from lambda_0 (2.1181259879 at D 18.5) (the reader's; information, not a bound); a change that touches a non-robust point is listed and not counted.
   **Every ln|det| local minimum without a sign change beside it.** Over 1.00 to 2.60 with xfkappa's scans (`map_read.txt`): this gives D 18.5's roots for the k_c comparison.
3. Information, not readings: the reference signs of the sign-convention check at lambda 1.20 and 2.60 against this folder's points there (same sign, ln within 1e-2); the parity they imply: the signs at 2.40 (+, xfkappa's) and 2.60 (-, the reference) imply an odd number of sign changes in (2.40, 2.60); the signs at 1.20 and 1.55 (both -) an even number in (1.20, 1.55).
4. A cap that fires, or a scan that exits non-zero, is a result: the points done are read and reported as partial; nothing is rerun or loosened. Exit 3 (not the record system) stops that scan.
5. Seconds per point are reported (this machine, this load), not compared with xfkappa's.

## Controls

- `repeat_check.py --selftest` (exit 0: identical agrees; a flipped sign, ln off by 0.05 and a non-robust point do not; ln off by 5e-3 does) and `--selftest --break` (exit 1), and the reader's selftest (0) and `--mutate=orient` (1), run by the driver first;
- `map_read.py` was run on planted windows before the launch: with agreeing repeats it reads the roots and minima of the planted signs, and with the 2.40 repeat off by 0.05 it exits 2 with 'STOP-level: a repeated point does not agree: no reading';
- the repeat gate and the scans' record-system check (exit 3 if the state does not reproduce its record's |F| and step count).

## Result (scans 2026-11-21 19:30:16 to 23:02:12 UTC; final reading 23:02 UTC)

All three processes ran to the end (exit 0, no cap): **A** 21 evaluations in 9316 s (420 to 495 s per point, mean 443 s); **B1** 28 in 12226 s (408 to 496 s, mean 437 s); **B2** 29 in 12566 s (403 to 493 s, mean 433 s). 4 threads each, BelowNormal, beside win2b's four k_c 55 scans. All passed the scan's
record-system check (|F| 2.7724871480e-10 against the record's 2.7672415504e-10, steps 2461 = 2461). All 161 points of 1.00 to 2.60 are noise-robust. The reading (`map_read_final.txt`, `map_read2.py`, xfkappa's `d18d_read.py` 6b608903 unchanged) on xfkappa's three D 18.5 scans and these windows:

**D 18.5, k_c 63, lambda 1.00 to 2.60 at 0.01 (161 points): two robust sign changes, and no ln|det| local minimum without a sign change.**

| root | bracket | orientation | det-linear estimate | estimator range (information, not a bound) | delta from lambda_0 = 2.1181259879 | where it comes from |
|---|---|---|---|---|---|---|
| 1 | (1.67, 1.68) | minus to plus | 1.677016 | [1.677016, 1.677225] | -0.441110 | xfkappa's scan (already known; winb's bisected root 1.6772090983 lies in the range) |
| 2 | (2.42, 2.43) | **plus to minus** | **2.420394** | **[2.420394, 2.420550]** | **+0.302268** | **window A (new)** |

| window | signs by lambda | changes |
|---|---|---|
| B, 1.00 to 1.55 (56 points: B1 28, B2 29, the 1.55 repeat in both) | `-` at all 55 new points and at 1.55 | **none**; ln\|det\| falls monotonically from -1888.8530 (1.00) to -1899.8681 (1.54), steps -0.458 to -0.010 |
| xfkappa, 1.55 to 2.40 | `-` to 1.67, `+` from 1.68 to 2.40 | one: root 1 |
| A, 2.40 to 2.60 (21 points: the 2.40 repeat and 20 new) | `+` at 2.40 to 2.42, `-` at 2.43 to 2.60 | **one: root 2** |

- **The repeats agree (the gate and `map_read2.py`):** 2.40: +1, ln|det| -1887.2954134028 against xfkappa's -1887.2954204508 (difference +7.0e-6); 1.55 in B1, in B2 and in the first run's stopped B: -1, -1899.8808977561 in all three (bit-identical) against xfkappa's -1899.8809001372 (difference +2.4e-6). Same sign, ln within 1e-2 (the bar I fixed): all agree, and to about 1e-5, closer than the control's 8.9e-4.
- **The reference points of xfkappa's sign-convention check (information):** lambda 1.20: -1 here, -1 there (ln -1896.58714060 against -1896.58714190, difference +1.3e-6); lambda 2.60: -1 here, -1 there (ln -1880.06922392 against -1880.06922532, difference +1.4e-6).
- **The parity they implied is as found:** the signs at 2.40 (+) and 2.60 (-) imply an odd number of sign changes in (2.40, 2.60): one (root 2). The signs at 1.20 and 1.55 (both -) imply an even number in (1.20, 1.55): none.
- **float64 beside:** 4 float64 sign changes over 1.00 to 2.60 ((1.63, 1.64), (1.64, 1.65), (1.66, 1.67), (2.42, 2.43)); float64 differs from the hybrid at 2 of 161 points. Root 2 is also a float64 change.
- The first run's stopped B had only its 1.55 point (the restart section above), so the same-machine comparison of duplicate points has nothing to compare for lambda below 1.55.

`points_map_final.md` lists every evaluation of A, B1 and B2 (and the stopped B's one). The first run's `map_read.txt` and `points_map.md` hold only the error line 'can't open file ...': the first driver's final calls failed as planned (`summary_d185map.txt`: `map_read: exit 2`, `points_table_map: exit 2`) because their scripts were renamed `*_v1.py`; the final files are `map_read_final.txt` and `points_map_final.md`.

Memory: lowest available 44.67 GB (during A, B1 and B2 together), peak commit 56.89 GB of 101.47 GB, page file peak 2610 MB (as at the start); no alert fired in either watch (no `alerts.log`).
Slips and changes: the restart of window B (the section at the top); the first driver's final calls failing as planned; `__pycache__` folders from importing my scripts were removed from this folder and from `../d18mid/pinned/` before the push. No other slips.
