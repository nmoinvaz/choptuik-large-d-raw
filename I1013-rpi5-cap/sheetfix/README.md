# sheetfix: the 2 cells of #1013's upper box that failed the sheet check, recounted at 6da7da7b

Part of `I1013-rpi5-cap` (rpi5, issue #1013). Written 2026-11-20 before the run.

## Why
xfchecks' sheet check of step 1 (#1013 comment 7034395925, raw d4231ed6) passes on 185 resolved leaves and 11 unresolved cells and fails
on 2 unresolved cells, A 4.1123-4.3623 x w/w_inf 0.5065-0.6065 and 0.6065-0.7065. Four points of column A 4.3623456 are on other sheets
of S3 = 0: w/w_inf 0.50654321, 0.55654321, 0.58154321, 0.60654321 (F3 +0.1985-0.1122i, -0.2117-0.0325i, -0.1837-0.0107i, -0.1379+0.0126i;
the box's sheet reads about +0.004-0.35i to -0.40i there).

## The 5 removed records (`removed_5_points.jsonl`, byte for byte from step 1's points file, raw 35affed8)
The four off-sheet points above, and the fifth, (4.3623456, 0.65654321), the shared edge point of the two cells. It is cached without value
(continuation lost S3's zero after []) and its F3 (-0.1379+0.0126i) equals the off-sheet 0.60654321 point's, so it was seeded from that
point: its record is as contaminated as the four (coordinator, 2026-11-20 about 08:30 UTC: remove all 5).

## Inputs and command
- `m3/points_M3_r0.17.jsonl`: step 1's points file (627 lines) minus the 5 records: 622 lines.
- `m3/leaves_2cells.jsonl`: the 2 failing cells' lines of step 1's `leaves_M3_upper_r0.17.jsonl`, byte for byte.
- code: `wip/argcount-m3-bounds` 6da7da7b (998fd290 plus the seed fix: --seed and --r1b copies keep 'fix'), worktree `~/Source/cl-1013fix`.
- `run_sheetfix.sh CODE PY OUT` runs the selftest and its five mutations (required exits `0 1 1 1 1 1`, the sixth is `--mutate=seedfix`),
  then `argcount.py --M=3 --recount=m3/leaves_2cells.jsonl --r1=0.17 --r1b=0.18 --m3fix --m3starts=0.2,0.25 --m3maxrhs=2.4e6
  --m3wall=3600 --m3noisecap=1e7 --procs=2` (step 1's flags, --procs 2 on the two idle cores beside step 2), nice 10, 12 h cap.
  The recount takes each cell as its own box (corners and edges from the cache), so it recomputes the removed points it needs, each
  seeded from its nearest valued record in the cache (`Multiplier.seed`) and from the points recomputed before it.

## Criteria (fixed before the run)
1. Selftest exit 0 and the five mutations exit 1 each.
2. The cache is only appended to: its first 622 lines keep their sha256 (`logs/exits.txt`), no key occurs twice, and no log line names a
   point of those 622 lines (`../check_cache_reuse.py POINTS LOG 622 SHA256`, exit 0).
3. Each recomputed one of the 5 points has F3 within |dF3| 0.1 of its valued neighbours in the cache (xfchecks' bound: a larger step
   between adjacent valued points marks another sheet); printed here, and the sheet verdict is xfchecks'.
4. The counts of the two cells are reported as printed (winding, leaves, unresolved cells) and stay on hold until xfchecks' sheet
   check passes on them. A cell that stays unresolved is reported as unresolved.

## Known before the run
Cell 1 (wf 0.5065-0.6065) has a sixth cached no-value point on its edge, its corner (4.1123456, 0.50654321) (continuation lost S3's zero
after [0.2, 0.195]; its F3 +0.0049-0.3108i equals that of (4.1123456, 0.70654321), on the box's sheet). It is not removed (not from an
off-sheet seed; `--retry` would also recompute the other 12 no-value points), so cell 1 may stay unresolved.

## Runs
Started 2026-11-20 08:32:01 UTC, ended 08:47:51 UTC (recount 944 s wall, 2 procs, nice 10), exit 0. Code 6da7da7b, python 3.13.7,
numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0 (`logs/exits.txt`). Files: `logs/m3_sheetfix_r0.17.log`, `logs/selftest.log`,
`m3/points_M3_r0.17.jsonl` (630 lines: the 622 cached plus 8 new), `m3/count_M3_sheetfix_r0.17.json`, `m3/leaves_M3_sheetfix_r0.17.jsonl`.

| Criterion | Verdict |
|---|---|
| 1 selftest and 5 mutations | exits 0 1 1 1 1 1 |
| 2 cache only appended | pass: 622 lines unchanged (sha256 45856355...), 0 duplicate keys, 0 log lines naming a cached point (`check_cache_reuse.py` exit 0; 8 new records, 8 log lines) |
| 3 F3 of the recomputed points | pass: column A 4.3623456 runs from +0.0021-0.4549i (w/w_inf 0.5065) to +0.0042-0.3247i (0.7565) with every step between adjacent points below 0.06 (largest 0.056, from 0.5065 to 0.6065; xfchecks' bound is 0.1) |
| 4 counts | both cells stay UNRESOLVED: boundary winding nan, 0 splits, leaf sum 0, no zero |

Of the 5 removed points the recount recomputed 3 (it did not request the other 2):

| w/w_inf | F3 | R | against 10 sigma | value |
|---|---|---|---|---|
| 0.50654321 | +0.0021-0.4549i | 1.14e8 | 1.2e8 | no (guard) |
| 0.55654321 | not requested | | | |
| 0.58154321 | not requested | | | |
| 0.60654321 | +0.0034-0.3986i | 5.28e7 | 2.18e7 | yes |
| 0.65654321 | +0.0037-0.3724i | 3.82e8 | 1.45e7 | yes |

The recount asked for 8 points: the 3 above, and 5 new points on the same edge, w/w_inf 0.63154321, 0.61904321, 0.61279321, 0.60966821
and 0.61591821. Points 0.55654321 and 0.58154321 were not requested by this recount.
The new edge points 0.60966821 (|R| 4.1e7, 10 sigma 5.6e7) and 0.61591821 (3.87e7, 4.34e7) fall under the 10 sigma guard, so the edge
A 4.3623456 between 0.6065 and 0.6565 has two points without value, near a minimum of |R| (3.4e7 at 0.6128): that cell (wf 0.6065-0.7065)
stays unresolved. Cell 1 (wf 0.5065-0.6065) has two corners without value: (4.3623456, 0.50654321) above and the cached
(4.1123456, 0.50654321).

## Not done
No sheet check of this recount (xfchecks'). The counts stay on hold.
