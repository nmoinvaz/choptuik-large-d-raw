# recount3: #1013's upper box, the 13 unresolved cells recounted at xi1 0.18 at 6da7da7b with --retry and --m3maxrhs=1e7

Part of `I1013-rpi5-cap` (rpi5, Raspberry Pi 5, aarch64, 4 cores, 8 GB, agent claude-me2; issue https://github.com/nmoinvaz/choptuik-large-d/issues/1013). Written 2026-11-20 before the run.

## The task and how I read it
Coordinator, 2026-11-20 (after xfchecks' sheet check of the sheetfix passed, #1013 comment 7034829136): recount the 10 cells with a lost-S3-zero corner at 6da7da7b, seeded from their on-sheet neighbours, from step 1's cache plus the sheetfix records, and revalue the 5 points at the call bound with `--m3maxrhs=1e7`. Same box flags otherwise, `--retry`, 4 processes, nice 10, a 12 h cap. Selftest and `--mutate=seedfix` first, and the cache-reuse check in the first minutes. The counts still need a sheet check after.

My reading (sent to the coordinator before the start): the 10 cells and the 5 points are step 2's xi1 0.18 result (16 points without value: 11 lost S3's zero, 5 stopped at the 2.4e6 call bound), so the run is at xi1 0.18.
- cache (`m3/points_M3_r0.18.jsonl`): step 2's 69 points minus 11 off-sheet records (below), 58 lines; `--retry` skips the 16 without value on loading and computes them again;
- seeds (`--seed`, `m3/points_M3_r0.17.jsonl`): the sheetfix's 0.17 file, i.e. step 1's cache without the 5 contaminated records plus the 8 sheetfix records, 630 lines (its first 622 lines are step 1's minus the 5, sha256 45856355359aabcb...);
- cells: all 13 unresolved cells of step 1 (`m3/leaves_M3_upper_r0.17.jsonl`, as in step 2). The 5 call-bound points have 4 of their cells outside the 10, so a recount of the 10 alone would not request them.

## 11 records removed from step 2's cache (`removed_11_points.jsonl`, byte for byte)
Found before the run (`sheet_precheck.py`, `make_cache.py`): on one sheet of S3 = 0, F3 does not depend on xi1, so a valued 0.18 point must have the F3 of its 0.17 twin on the sheetfix's sheet (which xfchecks' check passed). 11 of step 2's 53 valued points are off it by |dF3| 0.35 to 0.43 (xfchecks' bound is 0.1). The coordinator's rule (sheetfix, 2026-11-20): a record on another sheet is removed, with the reason beside the removed lines. The 7 of them that have a 0.17 twin have it with info 3e-3 to 2e3 and fix.ok, so at 998fd290, where a seed copied from another file lost its `fix`, they did not seed the 0.18 points; the 0.18 points were seeded from farther records. This is the seed fix's case (6da7da7b), not verified further.

| Line of step 2's file | A | w/w_inf | F3 at 0.18 | F3 on the 0.17 sheet | taken from | abs dF3 |
|---|---|---|---|---|---|---|
| 1 | 3.8623456 | 0.50654321 | +0.1780-0.0707i | +0.0049-0.3748i | same point | 0.350 |
| 2 | 3.6123456 | 0.60654321 | +0.1557+0.0573i | +0.0067-0.2837i | same point | 0.372 |
| 5 | 3.8623456 | 0.70654321 | +0.1259+0.0973i | +0.0058-0.2749i | same point | 0.391 |
| 13 | 3.8623456 | 0.73154321 | -0.0318+0.1331i | +0.0058-0.2645i | same point | 0.399 |
| 17 | 3.8623456 | 0.71904321 | +0.0673+0.1179i | +0.0058-0.2645i | nearest (3.8623, 0.73154) | 0.387 |
| 20 | 3.8623456 | 0.72529321 | +0.0267+0.1268i | +0.0058-0.2645i | nearest (3.8623, 0.73154) | 0.392 |
| 42 | 4.3623456 | 0.60654321 | +0.0899+0.0009i | +0.0034-0.3986i | same point | 0.409 |
| 43 | 4.3623456 | 0.50654321 | +0.1976-0.0935i | +0.0021-0.4549i | same point | 0.411 |
| 44 | 4.3623456 | 0.55654321 | +0.1631-0.0532i | +0.0021-0.4549i | nearest (4.3623, 0.50654) | 0.433 |
| 45 | 4.3623456 | 0.53154321 | +0.1837-0.0748i | +0.0021-0.4549i | nearest (4.3623, 0.50654) | 0.421 |
| 46 | 4.3623456 | 0.70654321 | +0.2482-0.0225i | +0.0040-0.3477i | same point | 0.407 |

The 42 valued points that stay all lie within 0.04 of the 0.17 sheet (`logs/sheet_precheck.log`). Step 2's count (winding NaN) used none of this, and its counts stay on hold as before.

## Command and code
- code: `wip/argcount-m3-bounds` 6da7da7b, worktree `~/Source/cl-1013fix`; python 3.13.7, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0.
- `run_recount3.sh CODE PY OUT` checks HEAD, the cache (58 lines) and the seed file (630 lines, first 622 sha256 45856355359aabcb), runs the selftest and its five mutations (required exits `0 1 1 1 1 1`, the sixth is `--mutate=seedfix`), the sheet pre-check with its control, and `check_retry_reuse.py --selftest`, then `argcount.py --M=3 --recount=m3/leaves_M3_upper_r0.17.jsonl --r1=0.18 --r1b=0.17 --seed=m3/points_M3_r0.17.jsonl --m3fix --m3starts=0.2,0.25 --m3maxrhs=1e7 --m3wall=3600 --m3noisecap=1e7 --procs=4 --retry --out=m3 --tag=M3_recount3_r0.18`, nice 10, `timeout 12h`.
- A new point is seeded from the nearest valued record among the cache, the seed file and the points computed before it in its batch (`Multiplier.seed`); the retried and removed points have their 0.17 twin as the nearest seed. The leaves file and the count are written only at the end, so a kill at the cap leaves the points file only.
- `check_retry_reuse.py` is `../check_cache_reuse.py` with the repeats `--retry` makes by design allowed: a key may occur twice only if its first record is one without value (not `valued3`), and the log may name only such cached points.

## Criteria (fixed before the run)
1. Selftest exit 0 and the five mutations exit 1 each; `sheet_precheck.py` on the cache exit 0 (no off-sheet valued point), its control exit 0, `check_retry_reuse.py --selftest` exit 0.
2. In the first minutes and at the end: `check_retry_reuse.py POINTS LOG 58 SHA256` exit 0 (the cache's 58 lines unchanged, no valued key repeated, no log line naming a valued cached point). The first log lines must be the retried or removed points, not the 42 valued ones.
3. At the end: every new valued 0.18 record has its F3 within 0.1 of the 0.17 sheet (`sheet_precheck.py` on the final file, new records only; printed here. The sheet verdict on the counts is xfchecks').
4. The counts are reported as printed (winding, leaves, unresolved cells, zeros). A cell that stays unresolved is reported unresolved. The counts stay on hold until xfchecks' sheet check passes on them.

## Runs
(filled in as the run goes)
