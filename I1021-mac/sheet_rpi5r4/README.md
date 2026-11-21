# I1021-mac/sheet_rpi5r4: the sheet check of rpi5's #1013 recount4, and its samebits failure

Machine: the Mac, helper session xfchecks, nice 19. For https://github.com/nmoinvaz/choptuik-large-d/issues/1013,
2026-11-21. Inputs: `I1013-rpi5-cap/recount4/` at raw 7e0e9c22 (the 0.18 cache, 801 lines; the 0.17 file, 630 lines,
the same sha256 as recount3's; pass 1's leaves and count), `recount3/m3/points_M3_r0.18.jsonl` and the sheetfix's 0.17
cache. sha256 of each in `in/SHA256SUMS`. This is criterion 5 of `../rpi5_fu018/README.md`: recount4's counts are held
until it passes.

## Checks (written before the run; `run.sh RP PY`)

The checks of `../sheet_rpi5r3/`, on recount4's files:
1. `diag/sheet_check.py` along grid lines of recount4's 0.18 cache, and of the pool of the sheetfix's 0.17 cache
   with recount4's 0.18 cache after it;
2. `sheet_check.py` on pass 1's 232 leaves with `--count`, on the cache and on the pool;
3. `diag/nearest_f3.py` of recount4's 0.18 and 0.17 records against the sheetfix's 0.17 cache.

Each must exit 0. The controls, `--mutate=switch` and `nearest_f3.py` on recount3's 11 removed off-sheet records, must
exit 1.

4. **Criterion 4 (samebits) read independently.** `argcount_samebits.py` exited 1 on rpi5. The question is whether
   that is the check's definition or a real difference. `prefix_keys.py RECOUNT3 RECOUNT4` does not share samebits'
   code. It passes when:
   - (a) recount3's 735 lines are recount4's first 735 lines, byte for byte;
   - (b) every later record of an old key is either an accepted fu row, for a point that recount3 had without a
     usable value (not valued3, or guard-blocked), or an argcount `--retry` record, for a point that recount3 had not
     valued3.

   `--mutate=edit` changes one digit of an old line in memory and must fail. `argcount_samebits.py` itself is not
   changed.

   The first form of (b) allowed accepted fu rows only. It flagged the 5 `--retry` records of the points without value
   (lines 796 to 801), which argcount appends by design (`--retry` computes again the points without value). That case
   was added before this README was written, and the first form's output is kept (`prefix_keys_firstform.txt`).

## Result (rpi5's raw 7e0e9c22; run 2026-11-21 14:07 UTC (file time), logs `sheet_check.log`, `sheet_check_mutate.log`)

Every check passes, and the three controls fail.

| check | valued points | pairs | largest \|dF_3\| | flagged |
|---|---|---|---|---|
| 0.18 cache, grid lines | 772 | 1311 | 0.0447 | 0 |
| pool (sheetfix 0.17, then recount4's 0.18), grid lines | 1299 | 2353 | 0.0447 | 0 |
| 0.18 cache, pass 1's 232 leaves | 772 | 816 | 0.0241 | 0 |
| pool, pass 1's 232 leaves | 1299 | 823 | 0.024 | 0 |

- `nearest_f3.py`: the 772 valued 0.18 records are within \|dF_3\| 0.0552 of their nearest sheetfix 0.17 point (the
  nearest is 0 to 0.354 away, so this check is weak, as for recount3). The 619 valued 0.17 records are the sheetfix's
  (distance 0, \|dF_3\| 0). Exit 0.
- `prefix_keys.py` (criterion 4 read as prefix and keys): PASS, exit 0.
  - recount3's 735 lines are recount4's first 735 lines.
  - Of the old keys, 8 have later records. 3 are the accepted fu rows (lines 736 to 738), among them the guard point
    (4.063517475, 0.51904321): its recount3 record is valued3 and guard-blocked at 9.18 sigma, and its fu default row
    is at 18.3 sigma. The other 5 are `--retry` records of points without value, still without value (lines 796 to
    801).
- Controls:
  - `--mutate=switch` flags 2 pairs (\|dF_3\| 0.297), exit 1;
  - the 11 removed records give \|dF_3\| 0.35 to 0.433, exit 1;
  - `prefix_keys.py --mutate=edit` exits 1.

**samebits: the check's definition, not a real difference.** `argcount_samebits.py` counts a record as valued by info
or fix ok, without the 10 sigma guard. So it compares recount3's guard-blocked row of (4.063517475, 0.51904321), which
argcount itself treats as without value, with the fu row that lifted it. That is the change pass 1 was run to make. No
old line changed, and every other later record is of the kinds above. Criterion 4 as written in `../rpi5_fu018/` is not
met: it is reported as is, and samebits is not changed. The criterion was mine. Since the step existed to lift
guard-blocked points, it should have exempted their accepted rows.

**The counts can be read.** Criterion 5 is met. recount4's final count is pass 1's: 12 unresolved cells, 232 leaves,
zeros none, with the blocking points named in its README (criterion 6). loc018's samebits (recount3 against loc018's
copy) does not meet this case unless an argcount run appends a record for a valued3 key. Its runs append new Newton
points and `--retry` records of points without value.

**Retest controls, recomputed from the rows** (`../merge_fu/fu_controls.py` on `rows_pass1.jsonl` and `rows_pass2.jsonl`
renamed to its pattern; `fu_controls_recount4.txt`, exit 0; `--mutate=exits` exits 1):
- pass 1: f3 changes 9 rows and lowguard 7; both exit 1, as reported;
- pass 2: f3 changes 0 rows (vacuous: no row was accepted), exit 0 as reported; lowguard changes 10, exit 1 as
  reported.
