# I1021-mac/sheet_rpi5loc018: the sheet check of rpi5's #1013 loc018 (criterion 5 of ../rpi5_loc018/)

Machine: the Mac, helper session xfchecks, nice 19. For https://github.com/nmoinvaz/choptuik-large-d/issues/1013,
2026-11-21. Inputs: `I1013-rpi5-cap/loc018/` at raw c24c9b06:
- the 0.18 cache (1132 lines: recount3's 735, then stage 1's Newton points and stage 2's plain and planted points);
- the 0.17 file (813 lines);
- stage 2's plain leaves and count (B1, B2, C0);
- recount3's 0.18 cache and the sheetfix's 0.17 cache.

The sha256 of each is in `in/SHA256SUMS`.

## Checks (written before the run; `run.sh RP PY`, the checks of `../sheet_rpi5r4/` on loc018's files)

1. `diag/sheet_check.py` along grid lines of loc018's 0.18 cache, and of the pool of the sheetfix's 0.17 cache with it.
2. `sheet_check.py` on stage 2's plain leaves with `--count`, on the cache and on the pool.
3. `diag/nearest_f3.py` of loc018's 0.18 and 0.17 records against the sheetfix's 0.17 cache.
4. `prefix_keys.py RECOUNT3 LOC018`: recount3's 735 lines must be loc018's first lines byte for byte, and every later
   record of an old key must be an argcount `--retry` record of a point that recount3 had not valued3. No fu rows
   are expected here.

Each must exit 0. The controls must exit 1: `--mutate=switch`, `nearest_f3.py` on recount3's 11 removed off-sheet
records, and `prefix_keys.py --mutate=edit`.

## Result

(below, after the run)
