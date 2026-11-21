# I1021-mac/final/leftovers: the unresolved leaves of #1021's recount of record and why

Machine: the Mac, helper session xfchecks, nice 19, read-only. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/1021. Inputs: `../record/` (the recount of record, exit 0 at
2026-11-21 10:20:33 UTC; raw 8eeff5a9), read from a scratch copy of its cache (sha256 ff39089e..., the same before and
after). Code: argcount at 6da7da7b (`choptuik-large-d-1021b`).

`leftovers.py CODE CACHE LEAVES 0.17` walks each unresolved leaf's boundary as argcount's count walks it (Counter,
dphi 0.5, hmin 1e-5), with argcount's Multiplier on the cache. A point missing from the cache stops it, so nothing is
computed. It names every boundary point without value with argcount's own note, and |R|/sigma for the guard. It
passes when every unresolved leaf has a named point.

Controls, each exit 1:
- `--mutate=drop` drops the first leaf's named points (`leftovers_drop.txt`);
- `--mutate=unguard` drops the 10 sigma guard. The walk then needs a point that is not in the cache,
  (3.3185956, 0.22216821), so it stops before naming (`leftovers_unguard.txt`).

Result (`leftovers.txt`, exit 0): 33 unresolved leaves, each with a named point. 19 are blocked by the guard alone.

`cells.py` → `cells.txt` gives the 32 cells: 21 are resolved and 11 have unresolved leaves. The 3 zeros:
- −1 at (2.934826, 0.285160) and +1 at (3.138598, 0.270629), in cell 5;
- −1 at (3.245478, 0.345851), in cell 8.

The 16 distinct blocking points:

| cells | point (A, w/w_inf) | cause |
|---|---|---|
| 7 | (3.3185956, 0.22529321) | guard, \|R\|/sigma 9.24 |
| 13, 14 | (3.2248456, 1.00654321) | continuation lost S3's zero after 0.25 ... 0.22625 |
| 15 | (3.5256269, 0.21279321) | guard, 4.65 |
| 16 | (3.6408612, 0.34404321) | guard, 6.22 |
| 16 | (3.4499433, 0.35029321) | guard, 6.03 |
| 17 | (3.5529706, 0.41279321) | guard, 4.85 |
| 24 | (3.9123456, 0.20654321) | continuation lost S3's zero after 0.25, 0.24875 |
| 25 | (3.8537519, 0.35654321) | guard, 8.96 |
| 26 | (3.7560956, 0.43154321) | guard, 7.57 |
| 26 | (3.8654706, 0.48505884) | guard, 9.86 |
| 26 | (3.8732831, 0.48779321) | guard, 6.98 |
| 31 | (3.7248456, 0.95654321) | 2.4e6 right-hand-side calls at xi1 0.245 |
| 31 | (3.7873456, 0.93154321) | inner solve: step size below the spacing of doubles |
| 31 | (3.8498456, 0.98154321) | inner solve: step size below the spacing of doubles |
| 32 | (3.7560956, 1.05654321) | continuation lost S3's zero after 0.25 |
| 32 | (3.8810956, 1.03154321) | continuation lost S3's zero at the first start |

Cells 7 (W −1), 15 (+1), 17 (−1) and 25 (+1) have an integer boundary winding with resolved leaves summing to 0, so
their unresolved leaves carry the cell's winding. Cells 16, 26, 31 and 32 wind 0. Cells 13, 14 and 24 have a point
without value on their own boundary.
