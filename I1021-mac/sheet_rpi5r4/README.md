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

## Result

(below, after the run)
