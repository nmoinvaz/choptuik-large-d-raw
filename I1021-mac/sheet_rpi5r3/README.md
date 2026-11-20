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
