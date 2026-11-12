# I553-win2: a finer last-node ladder across the Delta crossing, 0.73 to 0.79, with mode tracking

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/553 (follows from #543).
Start: crawlJ's state `I461-win2/crawlJ/anm_pin3_D242.3642.npz`, nodes 0.3, 0.4, 0.5, 0.6, 0.7. `renode_o.py ... --nodes 0.3,0.4,0.5,0.6,<x>` for x = 0.73, 0.75, 0.77, 0.78, 0.79, then `near_null_vec.py --k=4` and `near_null_eq.py --plant=7` on each. `near_null_vec.py` is `near_null.py` of main 14dc386 with two additions (`--vec=` saves the four vectors, and the norm of J's Delta column is printed); it is also run on the existing layouts 0.72 (`I537-win2`), 0.74, 0.76 and 0.80 (`I543-win2`), where its sigma must equal the logged ones (a reproducibility control). Mode identity between neighbouring layouts by the overlap of the weakest vectors' layout-independent blocks (p1, c0, m_h, a_h, Delta).
One lane of 2 threads (`lane_553.sh`, `layout_lib.sh`, `layout_lib_vec.sh`). `renode_o.py` from `D:\choptuik-i446g/hp` at main 14dc386, `near_null_eq.py` from `D:\choptuik-i505/hp` at 0cce81e. Exit codes in `exits.txt`. Results follow in this README.

## Results (2026-11-12 04:10:23 to 05:09:53 UTC)

One lane of 2 threads beside #535 and #554 (`lane_553.sh`; `exits.txt` has every start and exit). No Traceback, every exit as expected, 9 min a layout. `near_null.py` saves no vectors, so the raw sigma and the vectors come from `near_null_vec.py`, which is `near_null.py` of main 14dc386 with three added lines (`--vec=` saves the four vectors and the sigma, and the norm of J's Delta column is printed; `diff --strip-trailing-cr` against the original shows only those and the sys.path line).

**Checks.**

| step | result |
|---|---|
| `renode_o.py` for x_last = 0.73, 0.75, 0.77, 0.78, 0.79 | exit 0, check pass at each |
| `renode_o.py` x_last = 0.77, control `--mutate sign` | exit 1 as it must (check FAIL) |
| `near_null_vec.py --k=4` on the five new layouts and on 0.72, 0.74, 0.76, 0.80 | exit 0, check pass at each |
| `near_null_eq.py --plant=7` on the five new layouts | exit 0, check pass at each |
| reproducibility control: `near_null_vec.py` sigma against the logged `near_null.py` ones at 0.72, 0.74, 0.76, 0.80 | equal to 4.6e-04, 1.3e-04, 4.5e-05, 4.7e-05 relative (bound 1e-3), reproduced |

`crossing_553.py` was checked on planted vectors first (`results_crossing_553_selftest.txt`, ok: a known permutation with sign flips and noise matched, a planted crossing located at 0.7258, the 5% test passing at 4% and failing at 6%).

**Mode tracking** (`crossing_553.py` -> `results_crossing_553.txt`). Overlaps of the weakest vectors' layout-independent blocks (p1, c0, m_h, a_h, Delta; 129 entries) between neighbouring layouts are 1.00 for every mode from 0.75 to 0.80 and from 0.72 to 0.73, and 0.94 to 0.99 from 0.73 to 0.74. From 0.74 to 0.75 two modes exchange their order: vector 1 at 0.74 becomes vector 3 at 0.75 (overlap 0.99) and vector 3 becomes vector 1 (0.96), vector 2 stays (0.99) and vector 4 stays (0.80, flagged ambiguous since a second overlap exceeds half the best). The exchange is a crossing and not an avoided crossing: the Delta share of the Delta-bearing mode goes 0.70 (0.72, 0.73), 0.83 (0.74), 1.00 (0.75 onwards).

| x_last | Delta mode: index at that layout, raw sigma, delta share | harmonic-3 pair (geometric mean) | ln(sigma_D / sigma_H3) | \|\|J e_Delta\|\| | sigma_D / \|\|J e_Delta\|\| |
|---|---|---|---|---|---|
| 0.72 | 3, 5.653e-30, 0.70 | sigma_1, sigma_2 (3.249e-31) | +2.86 | 1.304e+29 | 4e-59 |
| 0.73 | 3, 5.032e-32, 0.70 | sigma_1, sigma_2 (2.907e-33) | +2.85 | 4.805e+27 | 1e-59 |
| 0.74 | 3, 3.670e-34, 0.83 | sigma_1, sigma_2 (8.453e-35) | +1.47 | 1.851e+26 | 2e-60 |
| 0.75 | 1, 1.691e-36, 1.00 | sigma_2, sigma_3 (7.635e-35) | -3.81 | 7.446e+24 | 2e-61 |
| 0.76 | 1, 6.725e-38, 1.00 | sigma_2, sigma_3 (7.618e-35) | -7.03 | 3.126e+23 | 2e-61 |
| 0.77 | 1, 8.113e-38, 1.00 | sigma_2, sigma_3 (7.606e-35) | -6.84 | 1.368e+22 | 6e-60 |
| 0.78 | 1, 8.246e-38, 1.00 | sigma_2, sigma_3 (7.594e-35) | -6.83 | 6.233e+20 | 1e-58 |
| 0.79 | 1, 8.533e-38, 1.00 | sigma_2, sigma_3 (7.582e-35) | -6.79 | 2.954e+19 | 3e-57 |
| 0.80 | 1, 8.736e-38, 1.00 | sigma_2, sigma_3 (7.571e-35) | -6.76 | 1.455e+18 | 6e-56 |

**Acceptance 1, the crossing to within 0.01: met.** The Delta mode's raw sigma meets the harmonic-3 pair's at **x_last = 0.7428**, bracketed by the layouts 0.74 (ln ratio +1.47) and 0.75 (-3.81), 0.01 apart (linear interpolation in ln). The Delta mode falls from 5.653e-30 at 0.72 to 1.691e-36 at 0.75 (a factor 3e6 in 0.03) and then stops: 6.7e-38 at 0.76, 8.7e-38 at 0.80. The harmonic-3 pair is nearly flat from 0.74 (8.45e-35) to 0.80 (7.57e-35).

**Acceptance 2, the Delta mode's raw sigma equals the norm of J's Delta column within 5%: FAILS, by tens of orders.** At 0.76 to 0.80 sigma_D is 6.7e-38 to 8.7e-38 and ||J e_Delta|| is 3.1e+23 to 1.5e+18, a ratio of 2e-61 to 6e-56. The control `--mutate` (the norm scaled by 1.1) also fails, so it adds nothing here; the 5% test itself passes at 4% and fails at 6% on planted numbers (selftest). The hypothesis of #543's summary, that the floor of about 8e-38 ("Delta alone, 8.43e-38", #493) is the norm of the Delta column, is refuted. My reading, which I did not check against the Jacobian: the weakest vector at 0.75 and above is e_Delta plus a correction of the order ||J e_Delta|| / ||J|| (1e-16 or smaller, invisible in the delta share 1.00), chosen so that J times it nearly cancels, so sigma_D would be the part of the Delta column that lies outside the range of the other columns and not the column's size. That part is nearly independent of x_last (+30% over 0.76 to 0.80, +85% to 0.92 in #554) while the column's norm falls by 11 orders over the same range, and I did not find what sets the number 1e-37.

**Acceptance 3, renode checks and the control:** pass at all five, the sign control exits 1 once.
