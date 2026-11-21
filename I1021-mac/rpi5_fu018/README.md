# I1021-mac/rpi5_fu018: the driver of rpi5's #1013 recount4 (recount3's 13 unresolved cells, start and seed variants at xi1 0.18)

Written on the Mac by the helper session xfchecks for rpi5, on the coordinator's request of 21 Nov 2026, before the
run. rpi5 runs it only on the coordinator's word. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1013.

## The 13 cells

From recount3 (`I1013-rpi5-cap/recount3`, raw 8dafdc05). Its sheet check passed (`../sheet_rpi5r3/`, 342b938b).

- **7 depth-0 cells at w/w_inf 1.0065-1.3065.** Each is blocked by points without value on its boundary:

  | point (A, w/w_inf) | cause in recount3 |
  |---|---|
  | (3.6123456, 1.30654321) | continuation lost S3's zero |
  | (4.3623456, 1.13779321) | continuation lost S3's zero |
  | (3.8623456, 1.20654321) | inner solve: step size below the spacing of doubles |
  | (3.7373456, 1.10654321) | 1e7 right-hand-side calls at xi1 0.25 (the second start) |
  | (4.1123456, 1.30654321) | 1e7 right-hand-side calls at xi1 0.25 |
  | (4.3623456, 1.30654321) | 1e7 right-hand-side calls at xi1 0.25 |
  | (4.2373456, 1.20654321) | wall bound 3600 s at xi1 0.25 |

- **2 cells at w/w_inf 0.5065-0.6065.** A 3.8623-4.1123 has boundary winding +1, and A 4.1123-4.3623 has −1. In
  each, the resolved leaves sum to 0. So the unresolved leaves carry the cell's winding together: +1 in
  A 4.0498-4.0811 × 0.5065-0.5315 (2 leaves) and −1 in A 4.2373-4.2998 × 0.5315-0.5565 (4 leaves). Each set of leaves
  meets at one valued point that the 10 sigma guard blocks: (4.063517475, 0.51904321) at |R|/sigma 9.18 and
  (4.2685956, 0.54404321) at 9.8.

## Command

On rpi5, from the raw clone's root, after `git sparse-checkout add I1021-mac/rpi5_fu018` and a pull:

    nohup bash I1021-mac/rpi5_fu018/run_fu018.sh ~/Source/cl-1013fix ~/Source/venv-choptuik/bin/python "$PWD" > I1013-rpi5-cap/recount4_driver.out 2>&1 &

`run_fu018.sh CODE PY RAW` checks these, and stops if any fails:

- CODE is at 6da7da7b with no changes;
- `I1013-rpi5-cap/recount4` does not exist;
- recount3's four inputs match `in/SHA256SUMS_recount3`;
- `fu_value.py` and `fu_value018.py` match `SHA256SUMS`.

It then runs argcount's selftest and its five mutations (must exit `0 1 1 1 1 1`), and `fu_value018.py --selftest`
and `--selftest --break` (must exit `0 1`). It copies recount3's 0.18 cache (735 lines) and 0.17 seed file (630 lines)
into `recount4/m3/`. Then each pass, at most 3:

1. `fu_value018.py --auto LEAVES --procs 4 --append`, at nice 10, with a 10 h cap. It values each point without value
   in the unresolved leaves, in the 5 variants below. Each point's first accepted row goes into the cache as one line
   with `"fu": variant`. In pass 1, LEAVES is recount3's leaves file, and the step selects the 9 points above.
   Later passes take the previous recount's leaves file.
2. `--retest` of the pass's rows with `--mutate=f3` and with `--mutate=lowguard`.
3. If the pass accepted no point, the run ends.
4. The recount of the 13 cells with recount3's arguments, at nice 10, with a 16 h cap:
   `--M=3 --recount=recount3/m3/leaves_M3_upper_r0.17.jsonl --r1=0.18 --r1b=0.17 --seed=recount4/m3/points_M3_r0.17.jsonl
   --m3fix --m3starts=0.2,0.25 --m3maxrhs=1e7 --m3wall=3600 --m3noisecap=1e7 --procs=4 --retry`, tag
   `M3_recount4_passN_r0.18`. With `--retry` it reads the appended lines and computes only the points without value
   and the new ones.
5. If the count has 0 unresolved cells, the run ends.

At the end, `argcount_samebits.py` compares recount3's cache with recount4's. `recount4/logs/exits.txt` gets one line
per step.

## Changes from dh610's fu_value.py

`fu_value.py` here is `I1021-dh610/b21-25-fu/fu_value.py` at raw 18338ce4, byte for byte (sha256 b36fb3e9...).
`fu_value018.py` imports it and changes two things only: R1 0.17 → 0.18, and the variants, which follow recount3's
settings (starts 0.2 then 0.25, bound 1e7). The tests, the selection of points, the appending and the retests are
dh610's.

| variant | starts | seed | right-hand-side bound |
|---|---|---|---|
| default | 0.2, 0.25 | nearest valued neighbour | 1e7 (recount3's settings) |
| s0.25 | 0.25, 0.2 | nearest | 1e7 |
| seed2 | 0.2, 0.25 | second nearest | 1e7 |
| seed3 | 0.2, 0.25 | third nearest | 1e7 |
| s0.25seed2 | 0.25, 0.2 | second nearest | 1e7 |

Every variant keeps the wall bound 3600 s and the noise cap 1e7. dh610's `rhs1e7` equals the default here, so it is
dropped. fu_value.py's seeds are ranked over the cache's records. argcount's seed also draws on the seed file and on
the earlier points of the batch. So the default variant may start from another seed than recount3 did, and it is not a
reproduction control here.

## Criteria (fixed before the run)

1. argcount's selftest and its five mutations exit `0 1 1 1 1 1`. `fu_value018.py --selftest` exits 0, and with
   `--break` it exits 1.
2. A row is accepted only by fu_value.py's tests, unchanged:
   - the point is valued (|r_3| < 1e-8, or the continuation's fix ok);
   - max|Y| ≤ 100;
   - |R| ≥ 10 sigma;
   - |dF_3| to the nearest valued neighbour in the cache ≤ 0.1.
3. The retests:
   - `--mutate=f3` must fire (exit 1) in every pass that accepted a row;
   - `--mutate=lowguard` must fire in every pass where the guard alone blocked a row;
   - otherwise each control is reported as vacuous for that pass.

   xfchecks recomputes both from the rows files (`../merge_fu/fu_controls.py`, as for dh610).
4. `argcount_samebits.py`: every valued record of recount3's 735-line cache is unchanged in recount4's (exit 0).
5. The counts are reported as printed. They are held until xfchecks' sheet check of recount4 passes: the checks of
   `../sheet_rpi5r3/`, on recount4's cache and its last leaves file.
6. The step is accepted when recount4 leaves 0 unresolved cells, or when each unresolved leaf is named with its
   blocking points and each variant's cause.

## Cost

recount3 valued 677 new points in 11.69 h, at 132 CPU s per point on average. Its 9 points without value took 100 to
3594 CPU s each. Pass 1 makes 9 × 5 = 45 runs, each capped at 3600 s, so its value step takes at most about 11 h on
4 processes. Most of the time is in the 7 upper points. The recount's new points depend on how far the 7 upper cells
refine, so its time is unknown. The caps bound the run: 10 h per value step, 16 h per recount, 3 passes.

## What it does not do

The guard blocks the 2 lower cells' points, which sit next to the zero that each cell's winding implies. dh610's
follow-up had 6 points that the guard alone blocked, at |R|/sigma 6.2 to 9.86. Another start or seed lifted 4 of them
over 10 sigma, and the two at 6.98 and 7.66 stayed under. If the guard still holds here after the passes, the next step
is to locate each zero with argcount's Newton (`locate_many`, on the unguarded values). That step is not part of this
run.

## Dry run (the Mac, 6da7da7b, nice 19, 21 Nov; scratch copies, not in this folder)

- recount3's inputs at 8dafdc05 match `in/SHA256SUMS_recount3`.
- `fu_value018.py --selftest` exits 0, and with `--break` it exits 1.
- On recount3's leaves file, the `--auto` selection gives exactly the 9 points above (45 runs).
- The driver refuses, with exit 1, when `recount4/` exists, when an input differs from its sha256 (one line added to
  the leaves file), and when `fu_value018.py` is changed.
- One guard point, (4.2685956, 0.54404321), through `fu_value018.py --points` at xi1 0.18 (exit 2, no row accepted).
  The default row's R is within 0.099 relative of recount3's record, from the Mac's build of the same code. Every row
  has |dF_3| 0.007, so the guard is the only test that blocks:

  | variant | \|R\| | sigma | \|R\|/sigma | CPU s |
  |---|---|---|---|---|
  | default | 4e5 | 1.15e5 | 3.48 | 59 |
  | s0.25 | 3.95e5 | 1.04e5 | 3.81 | 145 |
  | seed2 | 4.08e5 | 4.26e4 | 9.58 | 57 |
  | seed3 | 4.09e5 | 4.26e4 | 9.6 | 75 |
  | s0.25seed2 | 4.01e5 | 4.26e4 | 9.42 | 149 |

  recount3's record on rpi5 has sigma 4.26e4 and |R|/sigma 9.8. So on the Mac no variant lifts this point over
  10 sigma. rpi5's numerics differ, so this does not decide its run.
