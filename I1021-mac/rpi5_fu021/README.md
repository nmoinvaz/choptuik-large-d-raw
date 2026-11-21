# I1021-mac/rpi5_fu021: the driver of rpi5's #1021 fu021 (the record's 11 unresolved cells, start and seed variants at xi1 0.17)

Written on the Mac by the helper session xfchecks for rpi5, on the coordinator's request of 2026-11-21 (rpi5 idle after
loc018), before the run. rpi5 runs it only on the coordinator's word. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/1021.

## The leftovers

The recount of record (`../final/record/`, raw 7dac2e32, posted in #1021 comment 7064991335) leaves 33 unresolved
leaves in 11 cells, each with a blocking point named by `../final/leftovers/leftovers.py`:
- 9 points that are valued but guard-blocked (4.65 to 9.86 sigma), which on their own block 19 leaves;
- 7 points without value: the continuation lost S3's zero (4), the inner-solve step size (2), and the 2.4e6 RHS cap
  (1).

`select_points.py` reproduces `fu_value.py --auto`'s selection on the record's leaves, and gives 20 points:
- those 16;
- 4 more, inside cell 25's unresolved leaf, that are valued but guard-blocked (0.4 to 9.5 sigma), from the merged
  cache.

`fu_value.py`'s selection is kept unchanged (`in/select_dry.txt`).

## Command

On rpi5, from the raw clone's root, after a pull and
`git sparse-checkout add I1021-mac/final/record I1021-mac/rpi5_fu021`:

    nohup bash I1021-mac/rpi5_fu021/run_fu021.sh ~/Source/cl-1013fix ~/Source/venv-choptuik/bin/python "$PWD" > I1021-rpi5_fu021_driver.out 2>&1 &

`run_fu021.sh CODE PY RAW` stops if any of these fails:
- CODE is at 6da7da7b with no changes;
- `I1021-rpi5/fu021` does not exist;
- the record's four inputs match `in/SHA256SUMS_record`;
- the scripts match `SHA256SUMS`.

Then:
- argcount's selftest and its five mutations must exit `0 1 1 1 1 1`;
- `fu_value.py --selftest`, `--selftest --break` and `prefix_keys.py --mutate=edit` (on the record against itself)
  must exit `0 1 1`.

It copies the record's 0.17 cache (3229 lines) and 0.2 seed file into `I1021-rpi5/fu021/m3/`. Then each pass, at
most 2:
1. `select_points.py`: the points without value in the unresolved leaves, minus those an earlier pass ran. If none
   are new, the run ends. Pass 1 uses the record's leaves; pass 2 uses pass 1's recount leaves.
2. `fu_value.py --points ... --procs 4 --append`, at nice 10 with a 12 h cap. It runs each point in dh610's 6
   variants: default (the record's settings), rhs1e7, s0.2, seed2, seed3, s0.2seed2. Each point's first accepted row
   goes into the cache, with `"fu": variant`.
3. `--retest` with `--mutate=f3` and `--mutate=lowguard`.
4. If the pass accepted no point, the run ends.
5. The recount of the 11 cells (`in/cells_unresolved11.jsonl`), with the record's arguments, at nice 10 with a 16 h
   cap: `--M=3 --r1=0.17 --r1b=0.2 --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4 --retry`, tag
   `M3_fu021_passN_r0.17`.
6. If the count has 0 unresolved leaves, the run ends.

At the end, `prefix_keys.py` record → fu021 runs, and `argcount_samebits.py` record → fu021 is reported.

## Criteria (fixed before the run)

1. argcount's selftest and five mutations exit `0 1 1 1 1 1`. fu_value's selftest and `--break`, and
   `prefix_keys.py --mutate=edit`, exit `0 1 1`.
2. A row is accepted only by fu_value.py's tests, unchanged:
   - the point is valued;
   - max|Y| ≤ 100;
   - |R| ≥ 10 sigma;
   - |dF_3| to the nearest valued neighbour ≤ 0.1.
3. The retests:
   - `--mutate=f3` must fire in every pass that accepted a row;
   - `--mutate=lowguard` must fire in every pass where the guard alone blocked a row;
   - otherwise each is reported as vacuous.

   xfchecks recomputes both from the rows (`../merge_fu/fu_controls.py`).
4. **Bits:** `prefix_keys.py` record → fu021 exits 0. The record's 3229 lines must be fu021's first lines byte for
   byte, and every later record of an old key must be an accepted fu row for a point the record had without a usable
   value, or an argcount `--retry` record of a point the record had not valued3.

   `argcount_samebits.py` is reported only. It exits 1 whenever a guard-blocked point is lifted, as it did for
   recount4, because it compares a guard-blocked row as valued (`../sheet_rpi5r4/`).
5. The counts are on hold until xfchecks' sheet check of fu021's new points passes, the checks of `../sheet_rpi5r4/`.
6. The step is accepted when the recount leaves 0 unresolved leaves, or when each unresolved leaf is named with its
   blocking points and each variant's cause (`../final/leftovers/leftovers.py` on fu021's cache and last leaves).

## Cost

The record's points without value took up to 3600 s each per variant. The 7 hard points make 42 runs, and the 13
guard points 78, and those are fast: about 60 to 300 s per run in recount4's step. So pass 1 is bounded by the 12 h
cap and expected to take several hours on 4 processes. The recount's time depends on how far the 11 cells refine.
Caps: 12 h per value step, 16 h per recount, 2 passes.

## Dry run (the Mac, 6da7da7b, nice 19, 2026-11-21; scratch copies)

- The record's four inputs on raw (7dac2e32) match `in/SHA256SUMS_record`.
- `fu_value.py --selftest` exits 0, and with `--break` it exits 1. `prefix_keys.py` on the record against itself
  exits 0, and with `--mutate=edit` it exits 1.
- `select_points.py` on the record's leaves gives the 20 points (`in/select_dry.txt`).
- The driver refuses, with exit 1, when `I1021-rpi5/fu021` exists, when an input differs from its sha256 (a line
  added to the record's count), and when a script is changed (a line added to `select_points.py`).
- Pilot, one guard point through `fu_value.py --points` (6 variants, 2 processes): pending, below.
