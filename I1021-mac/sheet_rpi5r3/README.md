# I1021-mac/sheet_rpi5r3: the sheet check of rpi5's #1013 recount3 (the upper box's 13 cells at xi1 0.18, 6da7da7b)

Machine: the Mac, helper session xfchecks, nice 19. For https://github.com/nmoinvaz/choptuik-large-d/issues/1013, on the
coordinator's order of 20 Nov 2026. Written before recount3's results landed. Inputs: `I1013-rpi5-cap/recount3/m3/` at
the raw commit named below, and `I1013-rpi5-cap/sheetfix/m3/points_M3_r0.17.jsonl` (the sheetfix's 0.17 cache, whose
sheet check passed, `../sheet_rpi5fix/`). sha256 in `in/SHA256SUMS`; the files are not copied.

`run.sh RP PY` runs `../diag/sheet_check.py` and `../diag/nearest_f3.py` (bar |dF_3| 0.1). Criteria:

- along grid lines, 0 pairs flagged in the 0.18 cache, and in the pool of the sheetfix's 0.17 cache with the 0.18 cache
  after it. On a sheet F_3 does not depend on xi1, so a 0.18 value replaces its 0.17 twin and must sit on its
  neighbours' sheet;
- on recount3's leaves, with `--count`, 0 cells across a switch, in both files. argcount writes the leaves only at the
  end, so a run stopped at its cap has none, and only the points are checked;
- every valued 0.18 record, and every 0.17 record of recount3's own 0.17 file, within 0.1 in F_3 of its nearest valued
  point of the sheetfix's 0.17 cache.

Controls, which must fail: `--mutate=switch` on the pool, and `nearest_f3.py` on step 2's 11 removed off-sheet records
(`recount3/removed_11_points.jsonl`). Dry run on rpi5's plan commit 41f18b75 (the cache before the run, 58 lines; in
the scratchpad): all checks pass (0 of 37 and 0 of 1117 pairs flagged, |dF_3| to the sheetfix at most 0.0399), and
both controls fail (the 11 removed records |dF_3| 0.35 to 0.433).

## Result (rpi5's raw 8dafdc05; run 2026-11-21 00:18 UTC)

recount3 ended 2026-11-21 00:13:02 UTC with exit 0. Every check passes, and both controls fail.

| check | valued points | pairs | largest \|dF_3\| | flagged |
|---|---|---|---|---|
| 0.18 cache, grid lines | 712 | 1201 | 0.0447 | 0 |
| pool (sheetfix 0.17, then 0.18), grid lines | 1241 | 2243 | 0.0447 | 0 |
| 0.18 cache, recount3's 214 leaves | 712 | 757 | 0.0241 | 0, 0 of 214 cells across a switch |
| pool, recount3's 214 leaves | 1241 | 766 | 0.024 | 0, 0 of 214 cells across a switch |

- `nearest_f3.py`: each of the 712 valued 0.18 records is within \|dF_3\| 0.0552 of its nearest sheetfix 0.17 point.
  recount3's 0.17 file is the sheetfix's file (the same sha256), so its 619 valued records give distance 0 and
  \|dF_3\| 0.
- This check is weak here: 622 of the 712 valued 0.18 points have no sheetfix point at the same place. For 342 of them,
  the nearest is more than 0.1 away in (A, 2.5 w/w_inf), and up to 0.354. The grid-line checks of the pool compare
  neighbours directly.
- Controls: `--mutate=switch` flags 2 pairs, exit 1; the 11 removed records give \|dF_3\| 0.35 to 0.433, exit 1.

So recount3's count passes the sheet check on all 214 leaves. The check does not decide its 13 unresolved cells.
