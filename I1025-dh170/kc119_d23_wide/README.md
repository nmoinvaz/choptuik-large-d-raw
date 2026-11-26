# I1025-dh170/kc119_d23_wide: #1025 k_c 119 at D 23.0 (macm3's accepted state), a wide-window scan for a second root outside macm3's -0.02..0.06

Machine: dh170 (Fedora, i7-7700, 4 cores / 8 logical CPUs, 31 GiB), session `choptuik-dh170-i1025` (the claude-me2 continuation of session 5e14df5b). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-26 06:43:52 UTC, before any run of this folder.

## Order (the coordinator t5's hc, 26 Nov 06:40 UTC), quoted in full
"Read: k_c 111 at D 23.0 has one robust change in -0.06..0.06, (0.020, 0.040), det-linear 0.039279. That agrees with macm3's secant on your state, robust bracket [0.03538070, 0.03558301]. Your scan is the wide-window check of that root. Good post.
Next lane, #1025: a wide-window scan of k_c 119 at D 23.0, to look for a second root. k_c 119 shares the 16-step parity of 87 and 103, where S appeared at D 22.25. macm3 scans -0.02..0.06 on the same state for the threshold root; you cover what lies outside that.
- Inputs, pinned by blob: macm3's accepted k_c 119 state, raw I1025-macm3/kc119_d23/in/sol_l1kc119macm3d23_D23.0000.npy (blob 2771cf87), and its record l1kc119macm3d23.jsonl (blob 158e3086). The acceptance check is raw I1025-mac/checks/kc119_syscheck_1025.py (blob fc6e0dd6): it must exit 0 on this state and record, its --mutate=F and --mutate=steps must exit 1, and the kc111 check must refuse.
- Folder: raw I1025-dh170/kc119_d23_wide/. Write the README registration first. Use your kc111_d23 scan drivers with the state, check and window changed, and put the diff in the folder.
- Scan: d18_hybsign.py at lambda -0.10, -0.08, -0.06, -0.04, 0.08, 0.10, 0.12, plus one repeat of -0.06 (8 evaluations). Rounds of at most 3 processes of one thread (macm3 estimates about 7 GiB per k_c 119 process), nice 10. Then read_lower.py over the whole window, and give the signs at macm3's points beside yours once his scan is pushed.
- Yield rule: renice the lane's processes to 19 while an i1088a unit is active on your machine (#1088 comes first).
- Stop and report on: a state that is not accepted, an exception, or any step over 10 h. Nothing is killed on memory (alert only). Report every robust change; widen nothing.
- My registered prediction: no robust change in these 7 values (60%). If there is one, it is most likely in (0.06, 0.10) or below -0.06.
- ETA about 6-8 h. Post on #1025 when it ends."

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs and the drivers refuse any other blob)
| item | where | blob |
|---|---|---|
| macm3's accepted k_c 119 state at D 23.0 (tag l1kc119macm3d23), the state scanned; his regrid from my k_c 111 state ACCEPTED 2026-11-26 06:30:46 UTC | `in/sol_l1kc119macm3d23_D23.0000.npy` = raw `I1025-macm3/kc119_d23/in/` at origin/main 89a89ffb2, 62328 bytes | **2771cf87** |
| its record (1 row: D 23.0, k_c 119, kappa 0.7, u0 0.04, Ks 30, rk 1, |F| 3.2079513797870025e-10, F_start 1.2512516402778284e-05, steps 3914, psi-constraint 2.13890547520122e-3, Delta 1.1743249686574218, Delta of its k_c 111 source 1.1743265504807439, regrid wall 2273 s on his 6 threads) | `in/l1kc119macm3d23.jsonl`, 370 bytes | **158e3086** |
| the k_c 119 check (accepts), the k_c 111 check (refuses) | `in/kc119_syscheck_1025.py` = raw `I1025-mac/checks/`; `in/kc111_syscheck_1025.py` (my k_c 111 runs') | **fc6e0dd6**, 85aeb312 |
| scan driver (unmodified), the reader's imports, reader, repeat check | `in/d18_hybsign.py`, `in/d185_scan_read.py`, `in/read_lower.py`, `in/repeat_check.py` | e089207a, 7c9d400f, 89309d3c, aaf598a9 |
The k_c 119 check is the k_c 111 check with k_c 111 changed to 119 in three lines and one header comment line (`kc119_check_vs_kc111.diff`; macm3's reading: 3 lines removed, 4 added; the acceptance driver requires exactly that). Worktree: my k_c 111 runs' (`~/Source/choptuik-large-d-1025k79` at 48c36355; dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; clean; no file for the k_c 119 tag in `solver/matter/data/`), the venv `~/Source/choptuik-large-d-1058b/.venv` (Python 3.14.10, multidouble 5.1.0 avx2). **No regrid**: the state is macm3's, accepted here by the check.

## Commands (systemd user units, so no terminal owns them)
```
./run_accept.sh dry; systemd-run --user --unit=i1025-k119w-a --working-directory=$PWD systemd-inhibit --what=sleep --why="#1025 kc119 accept" --mode=block ./run_accept.sh
systemd-run --user --unit=i1025-k119w-y --working-directory=$PWD ./yield_watch.sh
systemd-run --user --unit=i1025-k119w-s --working-directory=$PWD systemd-inhibit --what=sleep --why="#1025 kc119_d23_wide scan" --mode=block ./run_scan.sh      # only after VERDICT.txt says ACCEPTED, after ./run_scan.sh dry
```
`run_accept.sh`: the pins, the diff of the two checks, the worktree, both selftests (exit 0), then **`kc119_syscheck_1025.py` on the state and record: exit 0; `--mutate=F` and `--mutate=steps`: exit 1 each; `kc111_syscheck_1025.py` on it: exit 1**; on success it copies the state and record to this folder and to the worktree's `solver/matter/data/` (blob checked) and writes `VERDICT.txt` ACCEPTED. `run_scan.sh` (the `../kc111_d23/run_scan.sh` driver with the folder, window, lists and comments changed and the reading block replaced by three reads; the diff is `run_scan_vs_kc111_d23.diff`): `d18_hybsign.py` points as **3 single-thread processes at nice 10 in three rounds**: p0 0.08, 0.12, -0.04; p1 0.10, -0.10, -0.06 (the repeat); p2 -0.08, -0.06 (the first -0.06). Round 1 is 0.08, 0.10, -0.08 (t5: a root is most likely in (0.06, 0.10) or below -0.06), round 2 is 0.12, -0.10, -0.06, round 3 is -0.04 and the repeat of -0.06 (two processes). At the end: `read_lower.py` selftest and its two mutations, then three reads: the **low window -0.10 to -0.04**, the **high window 0.08 to 0.12** and the **whole window -0.10 to 0.12**, `repeat_check.py`, `SCAN_DONE.txt`. **The whole window brackets the unscanned gap (-0.04, 0.08)** (macm3's -0.02 to 0.06 covers it): a sign difference across that gap is a sign difference, not a located root; it is reported as such, and only the two sub-windows give located changes.
**Yield rule (t5): `yield_watch.sh`** (unit `i1025-k119w-y`): every 20 s, while any `i1088a*` unit is active (user or system scope), it renices the scan's processes (command lines `time -v python -u .../d18_hybsign.py ... l1kc119macm3d23`) to 19 and logs to `yield.log`. A user cannot lower a nice value again, so a process once reniced stays at 19 (no cost without contention). Tested before the run (`yield_watch_test.log`): with no `i1088a` unit active a dummy process of the same command shape keeps nice 10; with a dummy unit `i1088a-test` active both of its processes go to 19 and my shell is untouched. No `i1088a` unit is active now.
Guards tried before the run (dry mode, each exit 1): a wrong state blob, a changed check file (`ctl_stateblob.txt`, `ctl_checkblob.txt`); the dry run passes with the true pins.

## Acceptance and stop rules (the order's, fixed before the run)
1. **State.** `kc119_syscheck_1025.py` exit 0 on macm3's state and record on this machine (|F| at most 1e-9, `freeze_from` gives the record's 3914 steps, |F| within 1% of the record's), both controls exit 1, the k_c 111 check refuses it, both selftests exit 0. Otherwise no scan (reported to t5).
2. **Scan.** Each process prints the record system; `read_lower.py` selftest exit 0, mutations exit 1; the repeat of -0.06 agrees.
**Stop and report on:** a state that is not accepted; an exception; any step over 10 h. Nothing is killed on memory (alert only: `alert.log` if MemAvailable falls below 2048 MiB). **Report every robust change; widen nothing.** I change nothing at a stop.

## Reading and registration, fixed now (by position)
Every robust change with bracket (**0.02 wide** in the scanned stretches: the grid is -0.10, -0.08, -0.06, -0.04 and 0.08, 0.10, 0.12), det-linear estimate and estimator range (the spread over interpolation choices, not an enclosure), orientation as printed (information only; not compared across k_c); the edge signs; changes touching a non-robust point listed and not counted; ln|det| minima without a sign change flagged; the repeat's bits. Beside my signs, **macm3's signs at -0.02 to 0.06** once his scan (`I1025-macm3/kc87_leg_lambda/23.0_kc119/`) is pushed; the root of k_c 119 he is looking for is near +0.040 (t5's registration: +0.040 +- 0.003). **t5's registration, here before any run: no robust change in these 7 values (60%); if there is one, it is most likely in (0.06, 0.10) or below -0.06.** (The k_c 119 state shares the 16-step parity of k_c 87 and 103, where a second root S appeared at D 22.25.)

## Predictions (mine, information; the k_c 111 runs: scan points 12617 to 13420 s with five processes, 6617 to 7020 s with three; peak RSS of a scan process 3.20 to 4.24 GiB at k_c 111; macm3's estimate for k_c 119 about 7 GiB)
- The state is accepted here with all controls firing and the k_c 111 check refusing about 85% (a different step count here than on macOS about 10%; other about 5%); the four check runs take under 5 min about 80%.
- The scan: every point noise-robust about 65%; **no robust change in the 7 distinct values about 55%** (t5: 60%); given a change: between 0.08 and 0.10 about 40%, between -0.10 and -0.06 about 35%, elsewhere (0.10 to 0.12, -0.06 to -0.04) about 25%. **The hybrid signs at -0.04 and at 0.08 differ about 85%** (macm3's root near +0.040 lies between them: the whole-window read then shows a robust change across the gap (-0.04, 0.08), which is the threshold root, not a second root). The repeat of -0.06 bit-identical about 90%; the float64 sign differs from the hybrid at more than half of the 7 points about 30%.
- Time: each scan point 8000 to 13000 s with three processes (k_c 111: 6617 to 7020 s; k_c 119 has N 7775 against 7255 and 3914 steps against 3653, about 1.3 to 1.5 times the work) about 60%; the three rounds end 6 to 9.5 h after the scan starts (round 3 has two processes and is faster per point) about 65%. Peak RSS of a scan process (up to three points each) 4.5 to 7.5 GiB about 70%; lowest MemAvailable above 6 GiB about 85%.

## Budget
Acceptance: about 1 to 5 min (starts at once). Scan: 3 single-thread processes at nice 10 on the 4 cores, starts only after ACCEPTED: about 7 h, ends about 14:00 UTC on 26 Nov if it starts at 07:00. Nothing else of mine runs. Memory: alert only; 3 processes of up to about 7 GiB are about 21 GiB of the 28 GiB free.

## Log
- 2026-11-26 06:43:52 UTC: README written before the run; folder set up (pins, `stage.conf`, three drivers; `run_scan_vs_kc111_d23.diff`, `kc119_check_vs_kc111.diff`; dry run passes; two guard controls exit 1; yield watcher tested with and without an i1088a unit).
- 2026-11-26 06:44:05 to 06:44:18 UTC: **STATE ACCEPTED** (`run_accept.sh`, unit `i1025-k119w-a`, 12 s for the four runs; `source_syscheck.txt` and the controls): `kc119_syscheck_1025.py` exit 0 on macm3's state and record (record |F| 3.2079513798e-10, state |F| 3.2167311359e-10 here, 0.27% from it; `freeze_from` 3914 = the record's: this Linux build reproduces his macOS step count), `--mutate=F` and `--mutate=steps` exit 1 each, the k_c 111 check refuses it (exit 1: "the record is not k_c 111 at D 23 (kc 119, D 23.0)"), both selftests exit 0, the diff of the two checks as required (3 removed, 4 added). State and record copied to this folder and to the worktree's data/ (blobs 2771cf87, 158e3086).
- 2026-11-26 06:44:27 UTC: **SCAN** started (unit `i1025-k119w-s`, 3 processes of 1 thread, nice 10, 8 evaluations in three rounds, the lists above); all three print the record system (|F| 3.2180583182e-10 against the record's 3.2079513798e-10, 3914 steps equal), about 99% CPU each, MemAvailable 27.2 GiB. The yield watcher (unit `i1025-k119w-y`, started 06:44:05) is running; no `i1088a` unit is active, `yield.log` is empty.
- 2026-11-26 06:46:37 UTC: step logged (this entry).
- 2026-11-26 09:48:43 UTC: **round 1 landed (3 of 8 evaluations; PARTIAL reading, `read_lower.py` on a scratch copy of the three files, not the driver's final reading):** hybrid signs **-0.08 +, 0.08 -, 0.10 -**, all noise-robust, the float64 sign equals the hybrid at all three; ln|det| -0.08 -3564.1702, 0.08 -3582.5805, 0.10 -3584.3264; points 9236 to 9278 s (three processes); peak RSS so far 2.56 to 2.77 GiB (still growing). **No robust change in the low window (one point so far) and none in the high window (0.08, 0.10 both -).** The sign differs between -0.08 (+) and 0.08 (-), across the unscanned gap that holds macm3's threshold root near +0.040 (a sign difference across the gap, not a located root; its printed orientation here is '+ to -', not compared across states). Pending: 0.12, -0.10, -0.06 (round 2), -0.04 and the repeat of -0.06 (round 3). `yield.log` is empty (no i1088a unit has been active).
- 2026-11-26 11:51:45 UTC: **round 2 landed (6 of 8 evaluations; PARTIAL, from the driver's files, no reader run on the whole):** hybrid signs **-0.10 +, -0.08 +, -0.06 + | 0.08 -, 0.10 -, 0.12 -**, all six noise-robust, the float64 sign equals the hybrid at all six; ln|det| -0.10 -3561.8584, -0.08 -3564.1702, -0.06 -3566.5098, 0.08 -3582.5805, 0.10 -3584.3264, 0.12 -3586.1948 (falling by -2.31 to -2.34 per 0.02 below and -1.75, -1.87 per 0.02 above: smooth, no dip); points 9112 to 9278 s. **No robust change in the low window so far (three + points) and none in the high window (three - points).** The sign changes once across the unscanned gap (-0.06 +, 0.08 -). Pending: -0.04 and the repeat of -0.06 (round 3, two processes, expected end about 13:40 UTC). `yield.log` is empty.


## Result (2026-11-26 13:26:43 UTC)
**No robust change in either scanned window of the k_c 119 state at D 23.0, and no second root in -0.10 to 0.12.** `read_lower.py` (`read_lower.txt`, three reads): **low window -0.10 to -0.04: hybrid signs -0.10+ -0.08+ -0.06+ -0.04+, robust changes 0; high window 0.08 to 0.12: 0.08- 0.10- 0.12-, robust changes 0**; all 8 evaluations (7 grid points and the repeat of -0.06) are noise-robust, the float64 sign equals the hybrid at all of them, no ln|det| minimum without a sign change in either window; every process printed the record system (|F| 3.2180583182e-10, 3914 steps = the record's); `read_lower.py` selftest exit 0 and its mutations `shift` and `round2` exit 1; **the repeat of -0.06 (process 2 against process 1) is bit-identical** in every field but its wall time and process (hybrid +, ln|det| -3566.5098298916, float64 +, noise [1.0, 1.0]), `repeat_check.py` PASS. `SCAN_DONE.txt` 13:24:50 UTC.
**The whole-window read of my 8 points** brackets the unscanned gap: robust change (-0.040, 0.080), '+ to -', det-linear 0.080000, range [-0.037578, 0.080000]: **a sign difference across the 0.12-wide gap, not a located root** (the det-linear estimate sits at the edge because a straight line through two ln|det| values 0.12 apart says nothing about the position). The gap holds macm3's threshold root.
**With macm3's points** (his scan, `I1025-macm3/kc87_leg_lambda/23.0_kc119/scan/`, raw origin/main 0f2e34391, blobs ecc16185 and ebcec073 in `macm3_blobs.txt`, copies in `macm3_scan/`; his 6 evaluations: -0.02, 0.00, 0.02, 0.04 twice, 0.06; his reading in `macm3_scan/macm3_read_lower.txt`) the 12 points of -0.10 to 0.12 read (`read_lower_with_macm3.txt`, `combined/`): hybrid signs -0.10+ -0.08+ -0.06+ -0.04+ -0.02+ 0.00+ 0.02+ 0.04+ 0.06- 0.08- 0.10- 0.12-; **one robust change, bracket (0.040, 0.060), '+ to -', det-linear 0.046539, estimator range [0.040232, 0.046539]** (macm3's point 0.04 has float64 -, hybrid +; both his repeat of 0.04 and my repeat of -0.06 agree); no second root at the 0.02 grid of -0.10 to 0.12, no ln|det| minimum without a sign change.

| lambda | hybrid sign | ln\|det\| (hybrid) | float64 sign | point wall (s) |
|---|---|---|---|---|
| -0.10 | + | -3561.8584 | + | 9142 |
| -0.08 | + | -3564.1702 | + | 9278 |
| -0.06 | + | -3566.5098 | + | 5605 |
| -0.06 | + | -3566.5098 | + | 9112 |
| -0.04 | + | -3568.8895 | + | 5606 |
| +0.08 | - | -3582.5805 | - | 9254 |
| +0.10 | - | -3584.3264 | - | 9236 |
| +0.12 | - | -3586.1948 | - | 9155 |

| lambda | -0.10 | -0.08 | -0.06 | -0.04 | -0.02 | +0.00 | +0.02 | +0.04 | +0.06 | +0.08 | +0.10 | +0.12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hybrid sign | + | + | + | + | + | + | + | + | - | - | - | - |
| ln\|det\| | -3561.86 | -3564.17 | -3566.51 | -3568.89 | -3571.33 | -3573.89 | -3576.72 | -3581.86 | -3581.14 | -3582.58 | -3584.33 | -3586.19 |
| scan | mine | mine | mine | mine | macm3's | macm3's | macm3's | macm3's | macm3's | mine | mine | mine |

ln|det| per 0.02 (the 12 points): -2.312, -2.340, -2.380, -2.443, -2.556, -2.827, -5.148, +0.722, -1.439, -1.746, -1.868: it falls smoothly, then falls by -5.148 into 0.04 and rises +0.722 at 0.06 (the dip at the root, as at the other k_c), then falls again; no other feature. This root is the threshold root macm3 is refining; its position here is his scan's, 0.046539 (range 0.040232 to 0.046539), +0.0073 from my k_c 111 scan estimate (0.039279; macm3's secant on k_c 111: 0.0355). I give no ruling on k_c convergence (t5's).

**Time and memory.** The scan 06:44:27 to 13:24:50 UTC = 6.67 h (process walls 6:40:21, 6:39:50, 5:06:37): the six points of rounds 1 and 2 took 9112 to 9278 s (three processes on 4 cores), round 3's two points 5605 and 5606 s (two processes). **Peak RSS of a scan process (time -v): 5.09, 5.10 and 5.03 GiB** (macm3's estimate was 7 GiB); the largest total of the three at one sample (once a minute) 12.28 GiB, lowest MemAvailable 15.3 GiB; nothing was killed on memory and there is no `alert.log`. **Yield rule:** no `i1088a` unit was active at any 20 s check, so `yield.log` was never written and no process was reniced (the watcher was tested before the run with a dummy unit).

## Predictions against the result
| prediction | result |
|---|---|
| t5's: no robust change in these 7 values (60%); if one, most likely in (0.06, 0.10) or below -0.06 | **met**: none in the low window (4 points) or the high window (3 points); the only change in the whole read is the threshold root, located by macm3's scan in (0.040, 0.060) |
| mine: the state accepted here with all controls firing and the k_c 111 check refusing (85%); the four check runs under 5 min (80%) | yes (steps 3914 = the record's); yes, 12 s |
| every point noise-robust (65%); no robust change in the 7 distinct values (55%); the repeat of -0.06 bit-identical (90%) | yes, 8 of 8; yes; yes |
| the hybrid signs at -0.04 and 0.08 differ (85%) | yes: + and - |
| the float64 sign differs from the hybrid at more than half of the points (30%) | no: at none of my 8 (and at macm3's 0.04, in both of his evaluations of it) |
| each scan point 8000 to 13000 s with three processes (60%); the three rounds end 6 to 9.5 h after the start (65%) | yes (9112 to 9278 s; round 3 faster with two processes, 5605 s); yes, 6.67 h |
| peak RSS of a scan process 4.5 to 7.5 GiB (70%); lowest MemAvailable above 6 GiB (85%) | yes, 5.03 to 5.10 GiB; yes, 15.3 GiB |
No miss. **Not known:** anything outside -0.10 to 0.12, and any structure finer than the 0.02 grid between the points (a close pair of roots would show as a ln|det| dip; none is flagged).

- 2026-11-26 13:26:43 UTC: scan ended 13:24:50 UTC; result written (this section); the yield watcher unit is stopped; nothing of mine is running.
