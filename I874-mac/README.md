# I874-mac: a re-converged truth at D 240.1244 (#852's u_2)

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/874

Code: hp/truth_restep.py on wip/xf-874 (28763c87, on main 2283596e), on main 3c35f0c's hpkernel. One process at nice
10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). Source: I603-win2/chain/anm_pin3_D240.1244.npz in #837's
truth_system. Output: `anm_pin3_D240.1244_u2.npz` here, in eight parts (save_o) with the source's meta and stored plan,
and `meta["restep"]` naming the source and the steps. Runs in `queue.sh` order, after I856-mac's queue.

## Answer

The stored u_2 (`anm_pin3_D240.1244_u2.npz`), read back through `truth_system`, has its own plain step at 1.5634e-99 of
max|z_h| and pinned max|F| 5.4062e-94, inside both bounds (1e-97, 1e-92). The old truth through the same path fails
both (3.2085e-57, 1.7135e-66). The store reproduced #852's three steps bit for bit, and the file reads back equal.

The read-back system is not bit-identical to the source's. `truth_system` recomputes the held offset from the state's
own centre data, and that offset moved by 1.767418394180938e-100 (max|offset| 8.2252e-4). So the state's own step is
1.5635832413406279e-99, not #852's step 3 (1.1622976274826494e-99). Both are at the octo-double floor, and max|F| is
equal as a double.

## Criteria (posted on the issue before the runs)

| # | criterion | fails when |
| --- | --- | --- |
| C1 | `store` reproduces #852's unperturbed path: each step's max\|dz\| and max\|F\| before it equal, as doubles, those of `I852-mac/steps_D240.json` (k 1, 2, 3), and the saved parts and plan read back equal | the path or the file differs |
| C2 | `check` of the stored state, read through `truth_system` (8 of 8 parts, held values in eight parts, plan stored): its own plain step max\|dz\| / max\|z_h\| at most 1e-97, and pinned max\|F\| at most 1e-92 | either bound fails |
| C3 | the control: `check` of the old truth through the same path fails both bounds, and its step does not equal #852's step 3 | it passes a bound or the match |
| C4 | reported: the largest difference between the held offsets of the stored state's system and the source's (`--held_ref`) | (0 when the state keeps the source's held values) |

The comparison in C1 and C2 shares its machinery (`newton_o`, `od_axpy`, `truth_system`) with #852's run, so it is a
reproduction, not an independent check.

## Results

| # | verdict | numbers (logs) |
| --- | --- | --- |
| C1 | pass | `store_u2.log`: steps 1, 2, 3 equal `I852-mac/steps_D240.json`'s as doubles (max\|dz\| 3.208820662899069e-57, 2.3721775065701996e-98, 1.1622976274826494e-99; max\|F\| before 1.713463779201813e-66, 2.395587509289433e-79, 5.406159172179391e-94); saved parts and plan read back equal |
| C2 | pass | `check_u2.log`: 8 of 8 parts, held values in eight parts, plan stored; step 1.5634e-99 (≤ 1e-97), max\|F\| 5.4062e-94 (≤ 1e-92) |
| C3 | pass | `check_truth.log`: step 3.2085e-57 FAIL, max\|F\| 1.7135e-66 FAIL, match FAIL |
| C4 | reported | held offset difference 1.767418394180938e-100, max\|offset\| 8.2252e-04 |

`check_u2.json` gives the stored state's unperturbed dΔ, 5.744294532362707e-103, which #857's and #875's runs from it
take as `--ref`.

### Notes

- The held offset is the value the frozen rows hold: those rows read coefficient − held value (`PinnedO`). So at
  u_2 the source's frozen rows keep a residual equal to the offset difference, and the held values recomputed from u_2
  set it to zero. Its effect on the step is at the floor (1.5636e-99 against 1.1623e-99), far below #857's moves
  (1.7e-85 and up) and #875's (1e-96 of max|z_h| and up).
- `check_u2` exits FAIL only on `--match`, the comparison with #852's step 3, which was not a posted criterion. The
  bounds of the issue pass.

## Discrepancies

- The read-back state's step is not #852's step 3 bit for bit (1.5635832413406279e-99 against 1.1622976274826494e-99),
  because `truth_system` takes the held values from the stored state rather than its source (C4). Reported, not fixed.

## Recommended tasks

1. **A re-stepped state in its source's system, bit for bit.** What: let `truth_system` take the held values from
   `meta["restep"]["source"]` when a state carries it (or store the source's held offset in the file), so that a
   re-converged state reads in the source's system. Why: #874's state reads in a system whose held offset differs by
   1.767e-100, so its step differs from #852's path at the floor. Acceptance: `truth_restep.py check` of
   `I874-mac/anm_pin3_D240.1244_u2.npz` with `--match I852-mac/steps_D240.json --match_k 3` passes (the step equal as
   doubles); with the old behaviour it fails (1.5635832413406279e-99). Depends on #874.
