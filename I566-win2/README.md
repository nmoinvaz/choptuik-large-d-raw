# I566-win2: the last node near the horizon, x_last 0.97, 0.99 and 0.995 with mode tracking

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/566 (follows from #559).
Start: crawlJ's state `I461-win2/crawlJ/anm_pin3_D242.3642.npz`, nodes 0.3, 0.4, 0.5, 0.6, 0.7. `renode_o.py ... --nodes 0.3,0.4,0.5,0.6,<x>` for x = 0.97, 0.99, 0.995, the control `--mutate sign` once (at 0.99), then `near_null_vec.py --k=4` (`near_null.py` of main 14dc386 with `--vec=` and the norm of J's Delta column added, `I553-win2/near_null_vec.py`, copied here) and `near_null_eq_vec.py --plant=7` (`near_null_eq.py` of 0cce81e with `--vec=` added, `near_null_eq_vec.py` here) on each. Both are also run again on the existing 0.96 and 0.98 (`I559-win2`'s re-noded states) for their vectors. Modes by the overlap of the vectors' layout-independent blocks (p1, c0, m_h, a_h, Delta). Two lanes of 2 threads (`lane_566_a.sh`, `lane_566_b.sh`, `layout_lib.sh`). Exit codes in `exits.txt`. Results follow in this README.

## Results (2026-11-12 06:05:35 to 06:54:08 UTC)

Two lanes of 2 threads beside #558 (`lane_566_a.sh`, `lane_566_b.sh`; `exits.txt` has every start and exit). No Traceback, every exit as expected, no renode refusal. 8 to 10 min a vector run.

**Checks.**

| step | result |
|---|---|
| `renode_o.py` for x_last = 0.97, 0.99, 0.995 | exit 0, check pass at each (at 0.995 the gap between the horizon series and the Taylor steps is 4.9e-36 in p and m, node 0.995 refined by block 5, rows 1.63e-16 -> 0.00) |
| `renode_o.py` x_last = 0.99, control `--mutate sign` | exit 1 as it must: rows 2.04e-16 -> 4.08e-16, check FAIL |
| `near_null_vec.py --k=4` on the three new layouts and on 0.96 and 0.98 | exit 0, check pass at each, ||J v_1|| / sigma_1 = 1.000000 on the new ones |
| `near_null_eq_vec.py` (`--plant=7` on the new layouts) | exit 0, check pass at each, planted column scaling recovered to 6.3e-13, 5.4e-13, 6.1e-13 (bound 1e-3) |
| reproducibility control: `near_null_vec.py` and `near_null_eq_vec.py` on 0.96 and 0.98 against #559's `near_null.py` and `near_null_eq.py` | sigma equal, relative difference 0.0e+00 (raw and equilibrated, both layouts) |

`near_null_vec.py` is `near_null.py` of main 14dc386 and `near_null_eq_vec.py` is `near_null_eq.py` of 0cce81e, each with a few added lines that save the vectors (the diffs against the originals are those lines and the sys.path line). `modes_566.py` was checked on planted vectors first (`results_selftest_566.txt`, ok).

**The weakest sigma at each layout** (`table_566.py` -> `results_table_566.txt`):

| x_last | raw sigma_1..4 (modes) | equilibrated sigma_1..4 | weakest equilibrated sigma | its mode (top scaled component; Dz: Delta share 0.9 or more in z) | largest abs J_ij |
|---|---|---|---|---|---|
| 0.96 | 1.305e-37 (D), 7.410e-35, 7.423e-35 (H3), 1.849e-34 (H1) | 1.246e-38, 4.552e-37, 4.472e-37, 3.988e-36 | 1.2460e-38 | Dz m_h k1 | 3.5e+04 |
| 0.97 | 1.338e-37 (D), 7.402e-35, 7.415e-35 (H3), 1.844e-34 (H1) | 3.008e-38, 1.013e-36, 1.095e-36, 7.176e-36 | 3.0077e-38 | Dz node4.m k1 | 2.9e+03 |
| 0.98 | 1.365e-37 (D), 7.395e-35, 7.408e-35 (H3), 1.840e-34 (H1) | 3.013e-38, 1.007e-36, 1.099e-36, 7.014e-36 | 3.0126e-38 | Dz node4.m k1 | 2.5e+02 |
| 0.99 | 1.385e-37 (D), 7.388e-35, 7.401e-35 (H3), 1.835e-34 (H1) | 2.612e-38, 8.790e-37, 9.576e-37, 6.098e-36 | 2.6120e-38 | Dz node4.m k1 | 2.0e+01 |
| 0.995 | 1.392e-37 (D), 7.385e-35, 7.397e-35 (H3), 1.833e-34 (H1) | 2.133e-38, 7.232e-37, 7.850e-37, 5.006e-36 | 2.1332e-38 | Dz node4.m k1 | 4.6e+00 |

**Acceptance: the maximum of the weakest equilibrated sigma is located to within 0.01: it lies between x_last = 0.97 and 0.98.** The values at 0.97 and 0.98 are equal to 0.16% (3.0077e-38 and 3.0126e-38); it falls by 13.3% at 0.99 (2.612e-38) and by 29% at 0.995 (2.133e-38), and is 59% lower at 0.96. A parabola in ln sigma through 0.97, 0.98, 0.99 has its vertex at x_last = 0.9751. So the rise of #559 stops, and reverses, past 0.98. The raw weakest sigma (the Delta direction) keeps rising slowly, 1.305e-37 at 0.96 to 1.392e-37 at 0.995. The largest entry of J falls from 3.5e+04 to 4.6, as the gain x_last^-(D-3) goes.

**Do the node4 modes at 0.98 equal the m_h modes at 0.96? The statement is not made, because the overlaps do not allow it** (rule fixed in `modes_566.py` before the data: made only if every mode matches unambiguously with overlap at least 0.9 and every vector keeps at least 0.5 of its norm in the layout-independent blocks p1, c0, m_h, a_h, Delta).
- Raw modes (`near_null_vec.py`): the matches 0.96 to 0.97, 0.97 to 0.98, 0.98 to 0.99, 0.99 to 0.995 and 0.96 to 0.98 all have overlap 1.00 and are unambiguous, each mode matched to itself (the Delta mode, the harmonic-3 pair, the harmonic-1 mode); but the vectors keep only 0.36 to 0.38 of their norm in the common blocks (sigma_1, the pure Delta direction, keeps 1.00). The rule withholds the statement for the raw modes (retained norm 0.36 < 0.5), though the common parts are identical.
- Equilibrated modes in z (D_c v): every match is flagged ambiguous (all four vectors are dominated by the Delta coordinate in z, so their common parts are nearly collinear), so nothing can be said from them.
- Equilibrated modes, scaled: the overlaps of the common parts are 0.91, 0.91, 0.94, 0.78 (0.96 to 0.97) and 0.90 to 0.95 (0.97 to 0.98), 0.99 to 1.00 after, but the retained norm of the scaled vectors falls from 0.68 (sigma_1 at 0.96) to 0.16, 0.07, 0.05, 0.04 at 0.97 to 0.995, and the 0.96 to 0.98 match has overlaps 0.72, 0.76, 0.77, 0.57 (sigma_4 ambiguous).

What the blocks show, as data and not as the registered statement. The scaled weight of the weakest equilibrated mode (sigma_1) moves from the horizon block to the last node's: node4.m + node4.a = 0.313 (0.96), 0.837, 0.923, 0.949, 0.953 (0.995), while m_h + a_h = 0.680, 0.145, 0.058, 0.031, 0.027. The sum of the four, node4.m + node4.a + m_h + a_h, is 0.993, 0.982, 0.981, 0.980, 0.980 at the five layouts, and for the next two modes it is 0.985, 0.968, 0.967, 0.969, 0.972; sigma_4 also carries node0 to node3 and Delta, and its end-of-interval weight is 0.82 at 0.96 and 0.73 to 0.74 from 0.97 (the table of block weights is in `results_modes_566.txt`). So the weight stays on the m and a unknowns at the end of the interval and only moves between the horizon variables and the last node's as that node approaches the horizon.
