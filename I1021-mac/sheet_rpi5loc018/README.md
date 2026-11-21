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

## Result (raw c24c9b06; run 2026-11-21 20:59 UTC, file time; `sheet_check.log`, `sheet_check_mutate.log`)

Every check passes, and the three controls fail.

| check | valued points | pairs | largest \|dF_3\| | flagged |
|---|---|---|---|---|
| 0.18 cache, grid lines | 1108 | 1501 | 0.0447 | 0 |
| pool (sheetfix 0.17, then loc018's 0.18), grid lines | 1637 | 2543 | 0.0447 | 0 |
| 0.18 cache, stage 2's plain leaves | 1108 | 62 | 0.00357 | 0 |
| pool, stage 2's plain leaves | 1637 | 62 | 0.00357 | 0 |

- On the leaves, each zero's cell is on one sheet: B1's +1 (not located) and B2's −1 at (4.270004, 0.544503).
- `nearest_f3.py`: the 0.18 records are within \|dF_3\| 0.0552 of the sheetfix's, and the 0.17 records within 0.04.
  Exit 0. It counts 1109 valued 0.18 points where sheet_check counts 1108; the two scripts' tests of a value differ
  slightly.
- `prefix_keys.py` recount3 → loc018: PASS.
- Controls: `--mutate=switch` exits 1; the 11 removed records are NOT on the sheet, exit 1; `prefix_keys.py
  --mutate=edit` exits 1.

So loc018's new points pass the sheet check, and its result can be used (criterion 5 of `../rpi5_loc018/`).
Note: `prefix_keys.py` prints "recount4's first lines" by its fixed wording; here it compares recount3 with loc018.
