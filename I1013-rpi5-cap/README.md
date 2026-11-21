# I1013-rpi5-cap: #1013 step 4 rerun, the M = 3 argument-principle count of the upper box A 3.6 to 4.35 with argcount's bounds (998fd290)

Machine: rpi5 (Raspberry Pi 5, aarch64, 4 cores, 8 GB, Linux 6.17.0-1021-raspi), agent claude-me2. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1013 (step 4 of its commands; #995's runner step). Task named by the coordinator by message, 2026-11-19 (the box cut to A <= 4.35, noise cap 1e7 and commit 998fd290 after #1021's measurements). The earlier folder `I1013-rpi5/` (the stopped `--m3fix` run at 068913b4, no count) stays as it is.

Code: `wip/argcount-m3-bounds` at 998fd290 ("argcount: set the M = 3 noise cap's default from measured noise (#1021)"), worktree `~/Source/cl-1013cap7`, `solver/inner_stokes/argcount.py`. Python 3.13.7 (venv-choptuik), numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, python-flint 0.9.0 / FLINT 3.6.0 (the exact versions the run prints are in `logs/exits.txt`).

## Written down before the run (the coordinator's message and the issue's rule)

Driver: `run_rpi5_upper.sh` (copy of `I1021-mac/split/run_rpi5_upper.sh` at choptuik-large-d-raw 205dadd8, read before running), `bash run_rpi5_upper.sh ~/Source/cl-1013cap7 ~/Source/venv-choptuik/bin/python <RAW>/I1013-rpi5-cap`. It refuses unless HEAD is 998fd290 and `m3/` does not exist (a fresh folder), then:

1. the selftest and four mutations (`nocap`, `starts`, `norecount`, `lowcap`): required exits `0 1 1 1 1` (the script stops otherwise);
2. step 1: `argcount.py --M=3 --A=3.6,4.35 --wf=0.5,1.3 --nA=3 --nwf=8 --r1=0.17 --r1b=0.18 --m3fix --m3starts=0.2,0.25 --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4`, at nice 10, 12 h cap: the base grid is A 3.6123 to 4.3623 (step 0.25) by w/w_inf 0.5065 to 1.3065 (step 0.1), 4 x 9 = 36 points, counted at xi1 0.17 (the 0.2 start first; at 0.2 these points have no start);
3. step 2: the recount rung at xi1 0.18 (`--recount` of step 1's leaves, seeded with its points), 6 h cap.

Each point writes one record and one log line (a point stopped by the wall or the call bound is recorded without value, with `fix.bound`; it is reported, not retried). Per-point progress is posted on #1013 every 3 h. The persistence rule is the issue's (an M = 1 zero persists if an M = 3 zero of the same sign lies within |dA| <= 0.2 and |d omega/omega_inf| <= 0.25; each M = 3 zero serves its nearest M = 1 zero); it is applied to the leaves file by the issue's analysis, not by this run. Stop by the coordinator's word or by a failed selftest exit; no per-point cap beyond the script's.

Above A 4.5 real points' noise reaches the fault level (#1021), so that part of the box waits for a different fault test; it is not run here.

## Runs

Driver started 2026-11-19 20:29:09 UTC at 998fd290 (`logs/driver.start`, `logs/driver.out`, `logs/exits.txt`). Selftest and the four mutations exited `0 1 1 1 1`, as required. The driver exited 0 at 2026-11-20 12:05:21 UTC.

| Step | Ended (UTC) | Exit | Time | Points | Result |
|---|---|---|---|---|---|
| 1, count at xi1 0.17 (`m3/count_M3_upper_r0.17.json`) | 2026-11-20 07:33:49 | 0 | 39875 s (11 h 4 min) | 627 (614 valued, 13 no value) | 198 leaves after 58 splits, 185 resolved (winding 0), 13 unresolved cells, zeros [], boundary winding NaN |
| 2, recount of the 13 cells at xi1 0.18 (`m3/count_M3_upper_r0.18.json`) | 2026-11-20 12:05:21 | 0 | 16291 s (4 h 32 min) | 69 (53 valued, 16 no value) | 13 leaves, all unresolved, 0 splits, leaf sum 0, zeros [], boundary winding NaN |

Step 2's seed file `points_M3_r0.17.jsonl` is unchanged by it (627 lines, sha256 starts 944d2329b137d619). Each point is one record and one log line (627 and 69). Step 1's no-value points are in `logs/m3_upper_r0.17.log`.

The 16 no-value points of step 2: 11 lost S3's zero in the continuation, and 5 stopped at the 2.4e6 right-hand-side call bound (xi1 0.2 or 0.25 start). No point reached the wall (3600 s) or the noise cap. A cell with a no-value corner stays unresolved, and every one of the 13 has at least one. Corners with a value, and the corners without, by cell (A range, w/w_inf range):

| A | w/w_inf | Valued corners of 4 | Corners without value at 0.18 |
|---|---|---|---|
| 3.6123-3.8623 | 0.5065-0.6065 | 2 | (3.6123, 0.5065) RHS bound; (3.8623, 0.6065) S3 zero lost |
| 3.6123-3.8623 | 0.6065-0.7065 | 2 | (3.6123, 0.7065) RHS bound; (3.8623, 0.6065) S3 zero lost |
| 3.6123-3.8623 | 0.7065-0.8065 | 3 | (3.6123, 0.7065) RHS bound |
| 3.6123-3.8623 | 1.0065-1.1065 | 2 | (3.6123, 1.1065) and (3.8623, 1.1065) S3 zero lost |
| 3.6123-3.8623 | 1.1065-1.2065 | 1 | (3.6123, 1.1065), (3.8623, 1.1065), (3.8623, 1.2065) S3 zero lost |
| 3.6123-3.8623 | 1.2065-1.3065 | 2 | (3.6123, 1.3065) and (3.8623, 1.2065) S3 zero lost |
| 3.8623-4.1123 | 0.5065-0.6065 | 1 | (3.8623, 0.6065), (4.1123, 0.5065), (4.1123, 0.6065) S3 zero lost |
| 3.8623-4.1123 | 1.1065-1.2065 | 1 | (3.8623, 1.1065), (3.8623, 1.2065) S3 zero lost; (4.1123, 1.2065) RHS bound |
| 3.8623-4.1123 | 1.2065-1.3065 | 1 | (3.8623, 1.2065) S3 zero lost; (4.1123, 1.2065), (4.1123, 1.3065) RHS bound |
| 4.1123-4.3623 | 0.5065-0.6065 | 2 | (4.1123, 0.5065) and (4.1123, 0.6065) S3 zero lost |
| 4.1123-4.3623 | 0.6065-0.7065 | 2 | (4.1123, 0.6065) and (4.1123, 0.7065) S3 zero lost |
| 4.1123-4.3623 | 1.1065-1.2065 | 3 | (4.1123, 1.2065) RHS bound |
| 4.1123-4.3623 | 1.2065-1.3065 | 1 | (4.1123, 1.2065), (4.1123, 1.3065), (4.3623, 1.3065) RHS bound |

Result for box A (3.6-4.35 x 0.5-1.3): no zero is counted at either rung, and the box's boundary winding is NaN because 13 cells (the same 13 at 0.17 and at 0.18) are unresolved. This run therefore gives no M = 3 zero that an M = 1 zero could persist to, and no statement that there is none either.

Sheet check (xfchecks, #1013 comment 7034395925, raw d4231ed6) of step 1: the 185 resolved leaves and 11 of the 13 unresolved cells pass; 2 unresolved cells (A 4.1123-4.3623 x 0.5065-0.6065 and 0.6065-0.7065) fail, four points of column A 4.3623456 being on other sheets of S3 = 0. The fix attempt is `sheetfix/` (6da7da7b, raw e12701e3): both cells stay unresolved. Step 2 gives no winding, so there is nothing of it for a sheet check. The counts of step 1 stay on hold as the coordinator's note below says.

Recount3 (coordinator task, 2026-11-20 12:31:26 to 2026-11-21 00:13:02 UTC, exit 0, 42096 s; folder `recount3/`, README there): the 13 unresolved cells recounted at xi1 0.18 at 6da7da7b with `--retry`, `--m3maxrhs=1e7` and the sheetfix seeds, from step 2's cache without its 11 off-sheet records. Count as printed: 214 leaves after 67 splits, 719 points, 13 unresolved cells, zeros none, boundary winding nan (6 of the 13 boxes have a boundary corner without value; two boxes show +1 and -1 with unresolved leaves inside). 4 of step 1's cells are now resolved with W 0, the 2 cells at w/w_inf 0.5065-0.6065 were split to depth 3, the 7 cells at 1.0065-1.3065 stay unresolved. The counts stay on hold until xfchecks' sheet check passes on `recount3/m3/points_M3_r0.18.jsonl`.

## Note from the coordinator, 2026-11-19 (about 00:30 UTC)

The run stays as it is, but its counts are not used until xfchecks' sheet check passes on them: the start radius can put a point on a different root of S3 = 0 (F3 on another sheet), and a winding across such a switch is invalid. The run changes nothing for this; the next #1013 post says so.
