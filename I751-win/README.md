# I751-win: which plan nodes carry Delta's plan dependence at D 99.875, each of the six other interior nodes shifted by 1e-3

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/751 (the coordinator's message `1794631892984-0` on the `choptuik-large-d` channel; recommended by #741, raw `I741-win/` 86eeacdc). Worktree `choptuik-i710` at main 5249c432, venv-t151 (Python 3.10), `OPENBLAS_NUM_THREADS=1`, BelowNormal. Start: cont3's D 99.875 state `I682-win/cont3/anm_pin13_D99.8750.npz` (quad-double). Flags as the issue gives them, #727's A1c flags (as `I741-win/run_741.py`): #682's plus `--elim_switch 0 --corrector od --tol_od 1e-60 --reseed_o 3 --save_base 1 --steps 0`. **Threads: 2 while #742 runs (4 threads), 4 after it ends** (the coordinator's message; `run_751.py` reads `threads.txt` before each job). Raw output to `I751-win/`.

## Plan, written before the runs (2026-11-14 04:53 UTC)

1. **The edit** (`make_shifts_751.py`, the data edit of #741's `make_shifts_741.py`): six copies of cont3's state in `states/`, each with ONE interior node of `segs` moved by +1e-3: A `segs[0][1]` (0.3344860465553726), B `[0][2]` (0.37271682386339955), C `[1][1]` (0.4440903534255986), D `[1][2]` (0.47204517671279933), E `[2][1]` (0.55), F `[3][2]` (0.6742907958686368). Only `meta["segs"]` changes, by exactly that node; the arrays are bit-identical; every plan stays increasing; the original is untouched (`states/edit_log.txt`; `--selftest` flags a planted array change, a second meta key, two nodes, the wrong node, the wrong shift, no shift and a node moved past its neighbour). #741's S3 (`segs[3][1]`, +1e-3, Delta - root +2.580394e-27) is the seventh node of the comparison.
2. **The root** is X2c's Delta (`I727-win/X2c`, octo-double, max|F| 2.7e-93). Each node's effect is Delta(polished state) - root, Delta the exact sum of the eight parts.
3. **(a)** each polish converges to octo-double max|F| of at most 1e-60.
4. **(b) the repeat**: after the six, the node with the **largest |effect|** is polished again from a different start (the arrays of #710's A1 state with that node's shifted meta, as #741's R1; `make_repro_751.py`). Reading, fixed here: its Delta must reproduce the first run's to 1e-40 (the issue's bar); more than 1e-40 is reported as a miss.
5. **(c)** the largest single-node effect is named, and the effects at 1e-3 are listed against A1's and X2's offsets, Delta(A1 on its own plan) - root and Delta(X2 on its own plan) - root (+2.9709e-26 and -1.6580e-25, #727). **The literal test**: the sum of the six effects (and, as stated, the sum of seven with #741's S3) against each offset; "within a factor 2" means the sum has the offset's sign and lies between 0.5 and 2 times it. It can fail, since #741's node did not act linearly. **Extra, labelled as such**: each effect scaled linearly by A1's and X2's actual per-node plan shifts from cont3's (`analyze_751.py`), which assumes the linearity that #741 did not support for `segs[3][1]`.

**Expectation, written before the runs and not a criterion**: from #727 (the A1 and X2 plans differ from cont3's by 5e-4 to 9.5e-4 at several nodes, mostly in segments 0 and 1) I expect one or two nodes of segment 0 or 1 to carry most of the offsets, with single-node effects at 1e-3 of 1e-26 to 1e-25, and I do not expect the sum to land within a factor 2 for both plans, since #741's single node was not linear. About 13 min a polish at 2 threads and 7 min at 4 threads.

**Not done**: other shift sizes, other D, the shape of one node's effect (the coordinator's task 2 waits for this result), any change of the flags.

## Results (2026-11-14 05:38 UTC)

`run_751.py NA NB NC ND NE NF` (NA and NB at 2 threads, the rest at 4 after #742 ended) and `run_751.py R_F` (4 threads), all exit 0, BelowNormal. Delta - root (the root is X2c's Delta), Delta the exact sum of the eight parts; `analyze_751.py` (selftest passed), `analysis_751_out.md`, `logs/`.

| node | `segs` index | position | shift of A1's plan | shift of X2's plan | **effect of +1e-3** | first Newton step abs dz | final octo max abs F | evaluations | seconds |
|---|---|---|---|---|---|---|---|---|---|
| A | [0][1] | 0.3345 | +3.873e-04 | +7.751e-04 | +3.1390e-48 | 2.20e-37 | 2.6e-74 | 2 | 646 |
| B | [0][2] | 0.3727 | +5.370e-04 | +7.499e-04 | -4.4833e-44 | 2.74e-36 | 9.0e-70 | 2 | 516 |
| C | [1][1] | 0.4441 | +9.382e-05 | -1.211e-04 | +1.4433e-39 | 8.95e-33 | 2.5e-66 | 2 | 220 |
| D | [1][2] | 0.4720 | +4.691e-05 | -6.057e-05 | -5.3726e-36 | 2.32e-29 | 6.5e-106 | 3 | 306 |
| E | [2][1] | 0.5500 | 0 | 0 | -1.4729e-32 | 4.33e-26 | 4.9e-93 | 3 | 316 |
| S3 (#741) | [3][1] | 0.6486 | +9.406e-05 | +9.489e-04 | +2.5804e-27 | | 7.5e-66 | 3 | 806 |
| F | [3][2] | 0.6743 | +4.703e-05 | +4.744e-04 | **-3.4642e-26** | 2.06e-18 | 6.7e-64 | 3 | 306 |
| R_F (repeat of F from A1's arrays) | [3][2] | | | | Delta(R_F) - Delta(NF) = +1.6334e-56 | 4.03e-18 | 7.0e-62 | 3 | 310 |

Acceptance: **(a) met**, every polish converged to at most 7e-62. **(b) met**: the repeat of the node with the largest effect (F) from #710's A1 arrays reproduces its Delta to 1.6e-56 (bar 1e-40; the rule was fixed before the runs). **(c)**: the largest single-node effect is **F, `segs[3][2]`, -3.4642e-26**, followed by the other node of the last segment (S3, +2.5804e-27) and then E (-1.5e-32); the literal test **fails**:

| sum of the effects at +1e-3 | value | against A1's offset +2.9709e-26 (ratio, within a factor 2) | against X2's offset -1.6580e-25 (ratio, within a factor 2) |
|---|---|---|---|
| six nodes | -3.4642e-26 | -1.166, NO (opposite sign) | +0.209, NO |
| seven nodes (with S3) | -3.2061e-26 | -1.079, NO | +0.193, NO |

The extra, labelled as assuming linearity in the shift: each effect scaled by the plan's actual node shift over 1e-3 and summed gives -1.3866e-27 for A1 (ratio -0.047 to +2.97e-26, the wrong sign) and -1.3987e-26 for X2 (ratio +0.084 to -1.658e-25, a factor 12 too small), so it fails too.

What the numbers say, as observations:
- **The effect of a node grows by about 22 orders of magnitude with its position**: +3e-48 at 0.33, 4.5e-44 at 0.37, 1.4e-39 at 0.44, 5.4e-36 at 0.47, 1.5e-32 at 0.55, 2.6e-27 at 0.65 and 3.5e-26 at 0.67, about a factor 10 per 0.01 to 0.02 in position, and the signs vary (+, -, +, -, -, +, -). Segments 0 and 1 are inert (at most 5.4e-36), the two nodes of the last segment carry everything above 1e-27.
- **The first Newton step moves the state by 2.2e-37 to 2.06e-18**, again growing with the position by 18 orders, while the residual before the polish (|F| 1.1e-37 to 1.7e-35) does not track it: F, with the largest effect, starts at 1.1e-36, A, with the smallest, at 1.1e-37, and E at 1.5e-35. So the starting |F| says little about how far the root has moved; that looks like the weak direction (pivot 1.2e-18) amplifying a residual component that is tiny for the inner nodes, which is a reading and was not tested.
- **The single-node effects at +1e-3 do not reproduce the two plans' offsets**, by sign for A1 and by a factor 5 (unscaled) to 12 (scaled) for X2. X2's plan moved F by +4.7e-4 and S3 by +9.5e-4, and A1's by +4.7e-5 and +9.4e-5, so the two outer nodes are the only ones that can carry the offsets; their effects are not additive in the shifts here (nodes interacting, or the effect not linear in the shift, as #741 found for S3). Which of these it is was not measured.

Limits: one shift size (+1e-3) for each of six nodes (S3 from #741), one start state, no scan of the shift. The shift of A1's and X2's plans on every node at once, and the segment-3 nodes alone at those values, were not run.
