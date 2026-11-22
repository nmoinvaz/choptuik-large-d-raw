# fu021: #1021's record leftovers (11 unresolved cells at xi1 0.17) valued again from other starts and seeds (xfchecks' driver run_fu021.sh), then recounted

Part of `I1021-rpi5`. Machine: rpi5, Raspberry Pi 5, aarch64, 4 cores, 8 GB, Linux 6.17.0-1021-raspi, agent claude-me2.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1021. Started 2026-11-21 21:09:37 UTC on the coordinator's word
(hc of 21 Nov: "Your next task, now, #1021 fu021: the record's leftovers at xi1 0.17, with xfchecks' driver at raw f3018a8e").

## Plan and criteria (xfchecks', fixed before the run)
`I1021-mac/rpi5_fu021/` (raw f3018a8e) holds the driver `run_fu021.sh`, its README (the leftovers, the passes, criteria
1 to 6, the Mac's pilot), `fu_value.py` (dh610's, sha256 b36fb3e9..., unchanged), `select_points.py`, `prefix_keys.py`,
`SHA256SUMS` and `in/` (`SHA256SUMS_record`, `cells_unresolved11.jsonl`, `select_dry.txt`). The record is
`I1021-mac/final/record/` (raw 7dac2e32; 3229-line 0.17 cache, 1151-line 0.2 seed file). In short:
- 20 points: the record's 16 named blockers (7 without value, 9 guard-blocked at 4.65 to 9.86 sigma) and 4 guard-blocked
  points inside cell 25's unresolved leaf. Each is valued again in 6 variants (default, rhs1e7, s0.2, seed2, seed3,
  s0.2seed2; 3600 s each), 120 runs per pass, 4 processes at nice 10, 12 h cap. A row is accepted only by fu_value.py's
  tests (valued, max|Y| <= 100, |R| >= 10 sigma, |dF3| to the nearest valued neighbour <= 0.1), and the first accepted
  row of a point is appended to the cache with `"fu": variant`.
- Each pass: value step, retests (`--mutate=f3` must fire in a pass that accepted a row, `--mutate=lowguard` where the
  guard alone blocked a row, else vacuous), end if nothing accepted, then the recount of the 11 cells (`--M=3 --r1=0.17
  --r1b=0.2 --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4 --retry`, 16 h cap), end at 0 unresolved
  leaves. At most 2 passes; pass 2 values only the points without value that pass 1 had not run.
- At the end `prefix_keys.py` record -> fu021 (must exit 0) and `argcount_samebits.py` (reported only: it exits 1
  whenever a guard-blocked point is lifted, as in recount4).
- Criteria: (1) argcount selftest and 5 mutations `0 1 1 1 1 1`; fu_value selftest, `--break`, `prefix_keys.py
  --mutate=edit` `0 1 1`; (2) acceptance only by those tests; (3) the retests as above; (4) prefix_keys exit 0 (the record's
  3229 lines are the first lines byte for byte, every later record of an old key is an accepted fu row or a `--retry`
  record); (5) counts on hold until xfchecks' sheet check of fu021's new points; (6) accepted at 0 unresolved leaves, or
  each unresolved leaf named with its blocking points and each variant's cause (`../../I1021-mac/final/leftovers/leftovers.py`
  on fu021's cache and last leaves).

## Command and setup
From the live raw clone's root (`$PWD` as RAW), in the background:
`bash I1021-mac/rpi5_fu021/run_fu021.sh ~/Source/cl-1013fix ~/Source/venv-choptuik/bin/python "$PWD" > I1021-rpi5/fu021_driver.out 2>&1`
(`I1021-rpi5/fu021_driver.start` has the start and `driver exit` lines).
- Code: worktree `~/Source/cl-1013fix` at `wip/argcount-m3-bounds` 6da7da7b, no local changes (the driver checks).
  Python 3.13.7, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0.
- Deviations: (a) the live clone is not sparse and cannot pull, so I copied `I1021-mac/final/record/` and
  `I1021-mac/rpi5_fu021/` from the push worktree (`~/Source/choptuik-large-d-raw-964`, f3018a8e is an ancestor of its HEAD
  d99383d1) with `cp -a`, `diff -r` identical, the driver's sha256 checks pass; (b) the coordinator's command wrote the
  driver's stdout to `I1021-rpi5_fu021_driver.out` in the raw root, which I put inside `I1021-rpi5/` so no stray file
  sits at the repository root.
- Pushes during the run come only from the push worktree (rsync of `I1021-rpi5/`), never from the live clone.
- The `running` label on #1021 was already set when I started; I leave it as it is.

## Runs
Handover: the first agent (claude-me2) hit its weekly limit on 2026-11-22 ~06:20 UTC during pass 1's recount; a new session
(claude-me, same machine) took over at 06:25 UTC and changed nothing in the run (the driver, pid 1236273, and the recount
were already running as its children).

### Pass 1
- Value step 2026-11-21 21:09:44 to 2026-11-22 00:24:55 (3 h 15 min, exit 2): 13 of 20 points accepted, cache 3229 -> 3242
  lines. Retests `--mutate=f3` and `--mutate=lowguard` exit 1 (fired). Posted on #1021, comment 7071556113.
- Recount of the 11 cells `M3_fu021_pass1_r0.17` 2026-11-22 00:25 to 07:15:46 UTC (exit 0, 24650 s, 6 h 51 min of the 16 h
  cap; 53040 CPU s summed from the log's `CPU s` fields, about 2.15 cores on average beside another project's
  `winding2.py`): 512 leaves after 167 splits, 23 unresolved leaves (was 33 in the record), 1 zero counted (+1, cell A 3.4436-3.4592,
  wf 0.3440-0.3503), boundary winding nan. Cache 3242 -> 3369 lines at xi1 0.17 (the 61 later points are xi1 0.2 points in
  `m3/points_M3_r0.2.jsonl`). The zero is counted, not located (the rule of #1013's loc018): argcount's Newton point at xi1 0.17 is
  (3.446204, 0.347602), Jacobian sign +1, with |R| 16.8 against a noise floor of 36.1 (below it); at xi1 0.2 (3.446218, 0.347607), |R| 0.0423 against a floor of 0.0411 (at it).
- Sheet check of pass 1 (xfchecks, raw `I1021-dh370/sheet_fu021p1` 929dceca, #1021 comment 7075944014, inputs verified against
  c31e459b): leaves 0 flagged (largest |dF3| 0.0394), lines 0 flagged (0.056), switch controls fail, prefix_keys passes
  (13 accepted fu rows, 1 `--retry` record). Pass 1's counts can be read. The same check covers pass 2's new points.
- Boxes (the record's 11 unresolved cells), from `m3/count_M3_fu021_pass1_r0.17.json`:

  | box A x wf | unresolved leaves, record -> pass 1 | boundary winding, record -> pass 1 | leaf sum |
  |---|---|---|---|
  | 3.1623-3.4123 x 0.2065-0.3065 | 2 -> 2 | -1 -> -1 | 0 |
  | 3.1623-3.4123 x 0.9065-1.0065 | 1 -> 0 | nan -> 0 | 0 |
  | 3.1623-3.4123 x 1.0065-1.1065 | 1 -> 2 | nan -> 0 | 0 |
  | 3.4123-3.6623 x 0.2065-0.3065 | 2 -> 2 | +1 -> +1 | 0 |
  | 3.4123-3.6623 x 0.3065-0.4065 | 4 -> 2 | 0 -> 0 | 1 (the counted +1) |
  | 3.4123-3.6623 x 0.4065-0.5065 | 4 -> 4 | -1 -> -1 | 0 |
  | 3.6623-3.9123 x 0.2065-0.3065 | 1 -> 1 | nan -> nan | 0 |
  | 3.6623-3.9123 x 0.3065-0.4065 | 2 -> 2 | +1 -> +1 | 0 |
  | 3.6623-3.9123 x 0.4065-0.5065 | 5 -> 4 | 0 -> 0 | 0 |
  | 3.6623-3.9123 x 0.9065-1.0065 | 7 -> 0 | 0 -> 0 | 0 |
  | 3.6623-3.9123 x 1.0065-1.1065 | 4 -> 4 | 0 -> 0 | 0 |

  Two boxes are resolved with W 0. In the box A 3.4123-3.6623 x 0.3065-0.4065 the counted +1 sits against a boundary winding
  of 0, with 2 leaves unresolved. Zeros of the record outside these 11 cells are not part of this recount.
- Named blockers (`logs/leftovers_pass1.log`, `leftovers.py` sha256 71966928..., exit 0 PASS, run on the first 3369 lines of
  the cache): 23 of 23 unresolved leaves have a named point; 16 blocked by the guard alone (|R|/sigma 0.415 to 9.24);
  4 `noise3` above the cap 1e7 at xi1 0.25, 2 and 1 lost S3's zero.
- The driver then started pass 2 on its own (07:15:46): 10 points without value in the 23 leaves, 7 already run, 3 to run
  (3.3498456, 1.05654321), (3.527579975, 0.21279321), (3.7248456, 1.08154321); 18 runs, 12 h cap.

### Pass 2
- Value step 2026-11-22 07:15:46 to 08:20:52 UTC (1 h 05 min, exit 0): 3 of 3 points accepted, cache 3369 -> 3372 lines;
  11912 CPU s summed from the log. Retests: `--mutate=f3` exit 1 (plain accepts 6, mutated 0); `--mutate=lowguard` exit 1
  (plain 6, mutated 11). Rows `rows_pass2.jsonl`, log `logs/value_pass2.log`.

  | point (A, wf) | record's blocker | variants accepted (of 6) | result |
  |---|---|---|---|
  | (3.3498456, 1.05654321) | S3's zero lost | 2: s0.2, s0.2seed2 (\|R\|/sigma 2.19e6, dF3 0.0092) | lost in default, rhs1e7, seed2 (after [0.25, 0.24]), seed3 |
  | (3.527579975, 0.21279321) | guard, 6.85 sigma | 1: s0.2 (16.9 sigma, dF3 0.00049) | default and rhs1e7 6.85, seed2 6.48, seed3 9.72, s0.2seed2 8.06 |
  | (3.7248456, 1.08154321) | noise3 above the cap | 3: seed2, s0.2seed2, seed3 (\|R\|/sigma 1.29e5, dF3 0.0052; seed3 past 1e7 RHS calls, accepted) | default, s0.2, rhs1e7: noise3 2.45e7 above the cap 1e7 at xi1 0.25 |
- The recount of the 11 cells (`M3_fu021_pass2_r0.17`, 16 h cap) started 08:20:52 UTC.
- Recount `M3_fu021_pass2_r0.17` 2026-11-22 08:20:52 to 10:57:18 UTC (exit 0, 9386 s, 2 h 36 min of the 16 h cap; 18554 CPU s
  summed from the log's `CPU s` fields): 518 leaves after 169 splits, 3302 points, **17 unresolved leaves (was 23 after
  pass 1 and 33 in the record)**, leaf sum 1, boundary winding nan, 1 zero counted (the same +1 as after pass 1). Cache 3372 ->
  3397 lines at xi1 0.17 (`m3/points_M3_r0.17.jsonl`, sha256 981f49fc...), 1212 lines at xi1 0.2.
- The driver stopped after pass 2 because it runs at most 2 passes; it did not test whether a pass 3 would have new points.

### End
Driver start 2026-11-21 21:09:37 UTC, `driver exit 0` 2026-11-22 10:57:19 UTC (13 h 48 min), `end` line in `logs/exits.txt`.

| step | time (UTC) | exit |
|---|---|---|
| argcount selftest, 5 mutations | 21:09 | `0 1 1 1 1 1` |
| fu_value selftest, `--break`, prefix_keys `--mutate=edit` | | `0 1 1` |
| pass 1 value, 20 points x 6 variants | 21:09:44-00:24:55 | 2 (13 of 20 accepted) |
| pass 1 retests f3, lowguard | | 1, 1 (fired) |
| pass 1 recount | 00:25-07:15:46 | 0 (23 unresolved leaves) |
| pass 2 value, 3 points x 6 variants | 07:15:46-08:20:52 | 0 (3 of 3 accepted) |
| pass 2 retests f3, lowguard | | 1, 1 (fired: f3 plain 6 / mutated 0; lowguard plain 6 / mutated 11) |
| pass 2 recount | 08:20:52-10:57:18 | 0 (17 unresolved leaves) |
| prefix_keys record -> fu021 | | 0 |
| samebits record -> fu021 | | 1 (reported only, below) |

### Boxes at the end (the record's 11 unresolved cells), from `m3/count_M3_fu021_pass2_r0.17.json`
| box A x wf | unresolved leaves, record -> pass 1 -> pass 2 | boundary winding, record -> pass 2 | leaf sum |
|---|---|---|---|
| 3.1623-3.4123 x 0.2065-0.3065 | 2 -> 2 -> 2 | -1 -> -1 | 0 |
| 3.1623-3.4123 x 0.9065-1.0065 | 1 -> 0 -> 0 | nan -> 0 | 0 |
| 3.1623-3.4123 x 1.0065-1.1065 | 1 -> 2 -> 0 | nan -> 0 | 0 |
| 3.4123-3.6623 x 0.2065-0.3065 | 2 -> 2 -> 2 | +1 -> +1 | 0 |
| 3.4123-3.6623 x 0.3065-0.4065 | 4 -> 2 -> 2 | 0 -> 0 | 1 (the counted +1) |
| 3.4123-3.6623 x 0.4065-0.5065 | 4 -> 4 -> 4 | -1 -> -1 | 0 |
| 3.6623-3.9123 x 0.2065-0.3065 | 1 -> 1 -> 1 | nan -> nan | 0 |
| 3.6623-3.9123 x 0.3065-0.4065 | 2 -> 2 -> 2 | +1 -> +1 | 0 |
| 3.6623-3.9123 x 0.4065-0.5065 | 5 -> 4 -> 4 | 0 -> 0 | 0 |
| 3.6623-3.9123 x 0.9065-1.0065 | 7 -> 0 -> 0 | 0 -> 0 | 0 |
| 3.6623-3.9123 x 1.0065-1.1065 | 4 -> 4 -> 0 | 0 -> 0 | 0 |

4 of the 11 boxes are resolved with W 0 (the two upper boxes at wf 0.9065-1.0065 and 1.0065-1.1065 of A 3.1623-3.4123, and the
two at A 3.6623-3.9123). 7 boxes keep unresolved leaves. Counts are as printed and stay on hold until xfchecks' sheet check
of the final cache.

### Unresolved leaves at the end, named (`logs/leftovers_pass2.log`, `leftovers.py` sha256 71966928..., exit 0 PASS, on the final cache)
17 of 17 unresolved leaves have a named point; 16 are blocked by the guard alone, 1 by a lost S3 zero. Controls:
`--mutate=drop` exit 1 (16 of 17 named), `--mutate=unguard` exit 1 (stops at a point not in the cache, (3.3185956,
0.22216821)).

| blocking point (A, wf) | leaves | cause at the end | variants (default, rhs1e7, s0.2, seed2, seed3, s0.2seed2) |
|---|---|---|---|
| (3.3185956, 0.22529321) | 2 | guard, 9.24 sigma | 8.66, 8.66, 8.41, 4.5, 3.44, 3.43 (all valued) |
| (3.5266034, 0.21279321) | 2 | guard, 2.26 sigma | not run: the point came from pass 2's recount (a bisection beside the accepted (3.52562685, 0.21279321)), and the driver stops at 2 passes |
| (3.6408612, 0.34404321) | 2 | guard, 6.22 sigma | 3.21, 3.21, 6.69, 6.76, 6.97, 4.8 |
| (3.5529706, 0.41279321) | 4 | guard, 4.85 sigma | 3.89, 3.89, 4.25, 3.87, 2.84, 3.94 |
| (3.8420331, 0.35029321) | 2 | guard, 0.415 sigma | 0.58, 0.58, 1.32, 0.234, 0.448, 1.37 |
| (3.7560956, 0.43154321) | 2 | guard, 7.57 sigma | 2.84, 2.84, 7.76, 8.06, 4.79, 3.71 |
| (3.8732831, 0.48779321) | 2 | guard, 6.98 sigma | 4.14, 4.14, 5.81, 7.78, 6.27, 6.94 |
| (3.9123456, 0.20654321) | 1 | continuation lost S3's zero after [0.25, 0.24875] | S3 lost in default, rhs1e7, s0.2, seed2, seed3; s0.2seed2 valued at 57.3 sigma but |dF3| to the nearest valued neighbour 0.113 above the 0.1 limit, so not accepted |

### Criteria (the driver README's)
| # | criterion | result |
|---|---|---|
| 1 | selftests `0 1 1 1 1 1`, `0 1 1` | met |
| 2 | a row accepted only by fu_value.py's tests | met: 16 rows (13 in pass 1, 3 in pass 2) |
| 3 | `--mutate=f3` fires in every pass that accepted a row, `--mutate=lowguard` where the guard alone blocked a row | met: pass 1 exits 1, 1; pass 2 exits 1, 1 (pass 2 accepted the guard point (3.527579975, 0.21279321)) |
| 4 | prefix_keys record -> fu021 exit 0 | met (exit 0; `logs/prefix_keys.log`). `argcount_samebits.py` exits 1, reported only, below |
| 5 | counts on hold until xfchecks' sheet check of fu021's new points | pass 1's cache (3369 lines) passed (#1021 comment 7075944014); the final cache (3397 lines) is pending |
| 6 | 0 unresolved leaves, or each unresolved leaf named with blocking points and each variant's cause | met by naming: 17 leaves, table above, `leftovers.py` PASS with both controls |

### Discrepancies and notes (reported, not fixed)
- `argcount_samebits.py` exit 1: `logs/samebits.log`: 3147 valued points in the record, 3140 with the same record in fu021; old
  points without value 8, of which valued now 6; the record's 3229 lines are fu021's first lines unchanged. The 7 differing keys
  are the 7 guard-blocked points that fu lifted in pass 1 ((3.44994325625, 0.35029321), (3.52562685, 0.21279321),
  (3.83812685, 0.34091821), (3.840079975, 0.34404321), (3.8498456, 0.35341821), (3.85375185, 0.35654321), (3.8654706,
  0.485058835)): their old record counts as valued for samebits' `valued()` (no guard), and the accepted fu row is a later record
  with other bits. The same cause as recount4's exit 1 in #1013; criterion 4 uses prefix_keys, which accepts them.
- The +1 zero: argcount's own count line prints "located at A 3.446204, wf 0.347602 (|R| 1.7e+01, Jacobian sign +1); at xi1 0.2:
  A 3.446218, wf 0.347607", while the earlier posts and the pass 1 section above call it "counted, not located" (the earlier
  session's reading of loc018's rule: |R| 16.8 is below the noise floor 36.1 at xi1 0.17, and at 0.2 |R| 0.0423 is at the floor
  0.0411). No loc018-style confirmation (relocation box, planted control) was run for it, so it is an unconfirmed Newton point
  inside a box of 2 unresolved leaves, not a confirmed location.
- The pass 1 and pass 2 value-step CPU in the earlier posts (34764 s and 11912 s) were summed with a narrower pattern; summed
  over every `CPU s` field of the logs they are 37419 s and 12070 s (below).
- Pass 2 ran only the 3 points that were new: the driver's selection skips points an earlier pass already ran (10 points
  without value in the 23 leaves, 7 already run).

### Cost and load
CPU summed over every `CPU s` field of the four logs: pass 1 value 37419 s (120 runs), pass 1 recount 53040 s (188 point lines),
pass 2 value 12070 s (18 runs), pass 2 recount 18554 s (25 point lines): 121083 s (33.6 h of CPU in 13 h 48 min of wall, about
2.4 cores on average; another project's `winding2.py` jobs shared the cores for part of the time). Memory, sampled with `ps`
and `free -m` (no peak recorded): main process 38-45 MB, spawn workers 81-106 MB, the system 2.1-2.5 GB used of 7.9 GB, swap 487
MB of 1 GB in use (from before the run).
