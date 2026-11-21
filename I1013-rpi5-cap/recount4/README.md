# recount4: #1013's 13 unresolved cells of recount3 valued again from other starts and seeds at xi1 0.18 (xfchecks' driver run_fu018.sh), then recounted

Part of `I1013-rpi5-cap` (rpi5, Raspberry Pi 5, aarch64, 4 cores, 8 GB, Linux 6.17.0-1021-raspi, agent claude-me2; issue https://github.com/nmoinvaz/choptuik-large-d/issues/1013). Started 2026-11-21 00:33:05 UTC on the coordinator's word (message of 21 Nov, "GO for #1013's next step, recount4 by the start-and-seed-variant (fu) route on all 13 unresolved cells").

## Plan and criteria (xfchecks', fixed before the run)
`I1021-mac/rpi5_fu018/` of the raw repository at 9d64a727 holds the driver (`run_fu018.sh`, blob 5f6dcec6), its README (blob 270d440b, the 13 cells, the 5 variants, the pass loop, the criteria), `fu_value.py` (dh610's, raw 18338ce4, sha256 b36fb3e9...) and `fu_value018.py` (sha256 2b4a1bf5...). In short:
- 9 points without value in recount3's unresolved leaves (7 at w/w_inf 1.0065-1.3065, 2 at the guard: (4.063517475, 0.51904321) at |R|/sigma 9.18 and (4.2685956, 0.54404321) at 9.8) are valued again in 5 variants (default, s0.25, seed2, seed3, s0.25seed2), each run capped at 3600 s, 45 runs per pass at 4 processes. A row is accepted only by fu_value.py's tests: valued (|r3| < 1e-8 or the continuation's fix ok), max|Y| <= 100, |R| >= 10 sigma, |dF3| to the nearest valued neighbour <= 0.1.
- Each pass: value step (10 h cap) -> retests `--mutate=f3` (must fire in a pass that accepted a row) and `--mutate=lowguard` (must fire where the guard alone blocked a row) -> if nothing accepted, end -> recount of the 13 cells with recount3's arguments (16 h cap) -> if 0 unresolved cells, end. At most 3 passes. At the end `argcount_samebits.py` compares recount3's 735-line cache with recount4's (must exit 0).
- Criteria 1 to 6 as in the driver's README: (1) argcount selftest and five mutations `0 1 1 1 1 1`, `fu_value018.py --selftest` 0 and with `--break` 1; (2) acceptance only by those tests; (3) the retests as above, else reported vacuous; (4) samebits exit 0; (5) counts reported as printed and held until xfchecks' sheet check of recount4 passes; (6) the step is accepted at 0 unresolved cells, or when each unresolved leaf is named with its blocking points and each variant's cause.

## Command and setup
From the live raw clone `~/Source/choptuik-large-d-raw` (the root, `$PWD` as RAW):
`bash I1021-mac/rpi5_fu018/run_fu018.sh ~/Source/cl-1013fix ~/Source/venv-choptuik/bin/python "$PWD" > I1013-rpi5-cap/recount4_driver.out 2>&1` (run in the background by the tool; `I1013-rpi5-cap/recount4_driver.start` has the start and `driver exit` lines).
- Code: worktree `~/Source/cl-1013fix` at `wip/argcount-m3-bounds` 6da7da7b, no local changes (the driver checks). Python 3.13.7, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0.
- Deviation from the driver's README: the live clone is not sparse, is 886 commits behind and holds my folders untracked, so a pull would refuse. I copied `I1021-mac/rpi5_fu018/` from the push worktree (`~/Source/choptuik-large-d-raw-964`, raw 9d64a727 or later) with `cp -a`, checked it with `diff -r` (identical) and the driver's own `SHA256SUMS` check. No pull in the live clone. Recount3's four inputs in this clone match `in/SHA256SUMS_recount3` (the driver checks again).
- Pushes during the run come only from the push worktree (rsync of this folder), never from the live clone.
- Beside it nothing else runs; the driver uses 4 processes at nice 10.

## Runs
Driver: start 2026-11-21 00:33:05 UTC, `driver exit 0` 14:01:48 UTC (13 h 28 min), `end` line in `logs/exits.txt`. It ended on pass 2, which accepted no point. Counts below are as printed and are **on hold until xfchecks' sheet check of recount4's points**.

| step | time (UTC) | length | result |
|---|---|---|---|
| selftests | 00:33 | | argcount selftest and 5 mutations `0 1 1 1 1 1`; `fu_value018.py` selftest and `--break` `0 1` |
| pass 1 value | 00:33:12-05:29:58 | 4 h 57 min | exit 2 (some not accepted): 3 of 9 points accepted, appended (cache 735 -> 738 lines) |
| pass 1 retests | | | `--mutate=f3` exit 1 (fired), `--mutate=lowguard` exit 1 (fired) |
| pass 1 recount | 05:30-09:29:16 | 14357 s | exit 0: 232 leaves after 73 splits, 777 points, 12 unresolved cells, zeros none, boundary winding nan; cache 801 lines |
| pass 2 value | 09:29:16-14:01:48 | 4 h 32 min | exit 2: **0 of 7 points accepted**, nothing appended |
| pass 2 retests | | | `--mutate=f3` exit 0 (vacuous: nothing was accepted, so no row for it to change), `--mutate=lowguard` exit 1 (fired: plain accepts 0, mutated accepts 10) |
| end | 14:01:48 | | `pass 2 accepted no point: end`; no pass 2 recount, so the final count is pass 1's; samebits exit **1** (below) |

### Pass 1 value step: the 9 points, 5 variants each (default, s0.25, seed2, seed3, s0.25seed2)

| point (A, w/w_inf) | before | result per variant | outcome |
|---|---|---|---|
| 4.063517475, 0.51904321 | guard, 9.18 | accepted in default, seed2, s0.25seed2 (\|R\|/sigma 18.3, 18.4, 18.3); s0.25 7.0 and seed3 7.1 under 10 | accepted, default's row (fu "default") |
| 4.3623456, 1.13779321 | S3 lost | accepted in all 5 (2.4e4-2.7e4); s0.25 and s0.25seed2 flag noise3 above the 1e7 cap (3.4e8, 4.7e13) and are still accepted by fu_value's tests | accepted, default's row |
| 3.7373456, 1.10654321 | 1e7 RHS | seed3 accepted (3.99e5, dF3 0.021); default, s0.25: S3 lost; seed2, s0.25seed2: noise3 7.1e9 above the cap | accepted, seed3's row |
| 4.2685956, 0.54404321 | guard, 9.8 | valued, not accepted: 4.57, 5.06, 5.74, 9.48, 9.46 | not accepted |
| 3.6123456, 1.30654321 | S3 lost | S3 lost (default, seed2, seed3, s0.25seed2); noise3 2.6e9 above the cap (s0.25) | not accepted |
| 3.8623456, 1.20654321 | step size | step size error (default, s0.25); 1e7 RHS calls (seed2, s0.25seed2); S3 lost (seed3) | not accepted |
| 4.1123456, 1.30654321 | 1e7 RHS | wall 3600 s (default, s0.25); S3 lost (seed2, s0.25seed2); 1e7 RHS calls (seed3) | not accepted |
| 4.2373456, 1.20654321 | wall | S3 lost (default, s0.25, seed2, s0.25seed2); wall 3600 s (seed3) | not accepted |
| 4.3623456, 1.30654321 | 1e7 RHS | 1e7 RHS calls (default, s0.25 at xi1 0.2, seed2, s0.25seed2 at xi1 0.2); noise3 2.2e13 above the cap (seed3) | not accepted |

### Pass 2 value step: 7 points (the 6 not accepted of pass 1 plus a new one)
The 6 repeated points gave the same cause or the same \|R\|/sigma per variant as in pass 1 to the printed digits: a rerun of a deterministic run, so pass 2 learned nothing at them. The new point:

| point | result per variant (\|R\|/sigma) | outcome |
|---|---|---|
| 4.0625409125, 0.51904321 (bisection of the edge between the guard point and its neighbour; \|R\| 1.2e4 and sigma 5.1e3 in argcount's own row) | default 5.61, s0.25 2.43, seed2 3.50, seed3 5.44, s0.25seed2 4.15 | all valued, none reaches 10 sigma; not accepted |

### Unresolved cells at the end (pass 1's recount, 12), each with its blocking points
| cell or leaf (A x w/w_inf) | blocking point(s) without value (the causes per variant are in the tables above) |
|---|---|
| 3.6123-3.8623 x 1.1065-1.2065 | (3.8623456, 1.20654321) |
| 3.6123-3.8623 x 1.2065-1.3065 | (3.8623456, 1.20654321); (3.6123456, 1.30654321) |
| 3.8623-4.1123 x 1.1065-1.2065 | (3.8623456, 1.20654321) |
| 3.8623-4.1123 x 1.2065-1.3065 | (3.8623456, 1.20654321); (4.1123456, 1.30654321) |
| 4.1123-4.3623 x 1.1065-1.2065 | (4.2373456, 1.20654321) |
| 4.1123-4.3623 x 1.2065-1.3065 | (4.1123456, 1.30654321); (4.2373456, 1.20654321); (4.3623456, 1.30654321) |
| U1, 2 leaves A 4.0498-4.0811 x 0.5065-0.5190 and 0.5190-0.5315 (box winding +1) | (4.0625409, 0.51904321), on the leaves' shared edge |
| U2, 4 leaves A 4.2373-4.2998 x 0.5315-0.5565 (box winding -1) | (4.2685956, 0.54404321), the leaves' common corner |

The 13th cell of recount3, A 3.6123-3.8623 x 1.0065-1.1065, resolved in pass 1 with W 0 (accepted point (3.7373456, 1.10654321)). The upper cells' status was read from the recount's `unresolved` list and the points without value on each boundary; whether each is blocked only by those points was not checked cell by cell.

### Criteria
| # | criterion | result |
|---|---|---|
| 1 | selftests `0 1 1 1 1 1`, `0 1` | met |
| 2 | a row accepted only by fu_value.py's tests | met: 3 rows, each with valued, max\|Y\| <= 100, \|R\| >= 10 sigma, \|dF3\| <= 0.1 (`rows_pass1.jsonl` fields `ok_guard`, `ok_sheet`) |
| 3 | `--mutate=f3` fires in every pass that accepted a row; `--mutate=lowguard` where the guard alone blocked a row | met: pass 1 both exit 1; pass 2 accepted no row (f3 vacuous, reported), lowguard exit 1 |
| 4 | samebits recount3 -> recount4 exit 0 | **not met: exit 1**, cause below |
| 5 | counts as printed, on hold | met (above); the sheet check of recount4 is xfchecks' |
| 6 | 0 unresolved, or each unresolved leaf named with blocking points and each variant's cause | met by naming: 12 unresolved cells, tables above |

### Discrepancy: samebits exit 1 (reported, not fixed)
`logs/samebits.log`: valued points in recount3's file 712; the same record in recount4's file 711; old points without value 8, of which valued now 2; the old file's 735 lines are the new file's first lines unchanged: True (sha256 of recount4's first 735 lines equals recount3's file, a996b964...); `bit check: FAIL`.
The one differing key is (4.063517475, 0.51904321). Its recount3 record (line 324, \|R\| 4.4e4, sigma 4719, 9.2 sigma) counts as valued for `argcount_samebits.py` (`valued()` tests info < 1e-8 or fix ok, with no 10 sigma guard), but argcount treated it as without value because of the guard. The accepted fu row for the same key (line 737: re 30312.77, im -29096.19, sigma 2292, info 0.871, fu "default") is a new last record with different bits, so the check sees a changed valued record. So criterion 4 cannot pass whenever a guard-blocked point whose old record satisfies fix ok is lifted. The other 711 valued records are bit-identical, and no old line changed. The mismatch is in the check's definition of "valued", not in a computed value; xfchecks decides whether to change it.

Other notes: pass 2's value step repeated 30 of its 35 runs of pass 1 (same points, same variants, same results), about 4.5 h of 4 cores. The wrapper's `driver exit 0` (`../recount4_driver.start`) is the driver's exit status.
