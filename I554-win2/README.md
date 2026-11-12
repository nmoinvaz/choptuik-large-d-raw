# I554-win2: the last-node ladder above 0.80, where the weakest equilibrated sigma peaks

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/554 (follows from #543).
Start: crawlJ's state `I461-win2/crawlJ/anm_pin3_D242.3642.npz`, nodes 0.3, 0.4, 0.5, 0.6, 0.7. `renode_o.py ... --nodes 0.3,0.4,0.5,0.6,<x>` (`--last horizon`) for x = 0.82, 0.84, 0.86, 0.88, 0.90, 0.92, then `near_null.py --k=4` and `near_null_eq.py --plant=7` on each, beside #543's 0.80 and #537's 0.70. One lane of 2 threads (`lane_554.sh`, `layout_lib.sh`).
`renode_o.py` and `near_null.py` from `D:\choptuik-i446g/hp` at main 14dc386, `near_null_eq.py` from `D:\choptuik-i505/hp` at 0cce81e. Exit codes in `exits.txt`. Results follow in this README.

## Results (2026-11-12 04:10:23 to 05:09:57 UTC)

One lane of 2 threads beside #535 and #553 (`lane_554.sh`; `exits.txt` has every start and exit). No Traceback, every exit as expected, 9 min a layout.

**Checks.**

| step | result |
|---|---|
| `renode_o.py` for x_last = 0.82, 0.84, 0.86, 0.88, 0.90, 0.92 | exit 0, check pass at each (new node refined by block 5, horizon series; the gap between the horizon series and the Taylor steps is 4e-36 to 5e-36 in p and m at all six; the start's pinned max|F| is 1.62e-34 at all six) |
| `renode_o.py` x_last = 0.86, control `--mutate sign` | exit 1 as it must: rows 2.14e-16 -> 4.29e-16, check FAIL |
| `near_null.py --k=4` on the six | exit 0, check pass at each, ||J v_1|| / sigma_1 = 1.000000 |
| `near_null_eq.py --plant=7` on the six | exit 0, check pass at each, planted column scaling recovered to 4.0e-15, 1.4e-14, 7.9e-15, 9.0e-14, 5.7e-14, 1.7e-13 (bound 1e-3) |

The layouts 0.70 and 0.72 are #537's, 0.74, 0.76, 0.80 #543's, 0.73, 0.75, 0.77, 0.78, 0.79 #553's (the same two builds, main 14dc386 and 0cce81e). The analysis `ladder_554.py` was checked on planted series first (`results_ladder_554_selftest.txt`, ok: an interior peak located, a monotonic series reported at the end of the range, planted log lines parsed).

**The weakest sigma at each layout** (`ladder_554.py` -> `results_ladder_554.txt`, every sigma and mode is there):

| x_last | weakest raw sigma (mode) | weakest equilibrated sigma | its mode (top scaled component; Dz: delta share 0.9 or more in z) | largest \|J_ij\| | ln of the equilibrated one |
|---|---|---|---|---|---|
| 0.70 | 2.530e-27 (H3) | 1.882e-61 | m_h k3 | 2.4e+37 | -139.83 |
| 0.72 | 3.233e-31 (H3) | 2.028e-62 | m_h k3 | 2.8e+34 | -142.05 |
| 0.74 | 8.405e-35 (H3) | 3.969e-63 | m_h k3 | 4.0e+31 | -143.68 |
| 0.76 | 6.725e-38 (D) | 4.616e-62 | Dz m_h k1 | 6.8e+28 | -141.23 |
| 0.80 | 8.736e-38 (D) | 1.477e-56 | Dz m_h k1 | 3.1e+23 | -128.55 |
| 0.82 | 9.119e-38 (D) | 5.932e-54 | Dz m_h k1 | | -122.56 |
| 0.84 | 1.020e-37 (D) | 2.551e-51 | Dz m_h k1 | 2.7e+18 | -116.50 |
| 0.86 | 1.051e-37 (D) | 1.194e-48 | Dz m_h k1 | | -110.35 |
| 0.88 | 1.110e-37 (D) | 2.513e-46 | Dz m_h k1 | 3.9e+13 | -105.00 |
| 0.90 | 1.157e-37 (D) | 3.156e-44 | Dz m_h k1 | | -100.16 |
| 0.92 | 1.246e-37 (D) | 2.037e-42 | Dz m_h k1 | 9.3e+08 | -96.00 |

**Acceptance: the weakest equilibrated sigma is largest at the end of the range, x_last = 0.92 (2.037e-42), and does not peak there.** It rises from 1.9e-61 at 0.70, passing the minimum 4.0e-63 at 0.74, to 2.0e-42 at 0.92, 19 orders above the 0.70 layout. The rise slows: the increase of ln per 0.02 of x_last is 6.0, 6.1, 6.2 (0.80 to 0.86), then 5.4, 4.8, 4.2 (0.86 to 0.92); with second differences of about -0.5 to -0.8 per step over the last three steps it would reach zero slope past x_last = 1, so no interior peak is expected within the range of a node. The weakest direction is the pure Delta direction (raw delta share 1.00) at every layout from 0.75 on. Its raw sigma is nearly flat, 6.7e-38 at 0.76 and 1.2e-37 at 0.92 (+85% over 0.16 of x_last, while the matrix scale falls by 28 orders), and the harmonic-3 pair falls slowly (7.63e-35 at 0.75, 7.44e-35 at 0.92). The equilibrated rise therefore comes from the scale: the largest entry of J falls as x_last^-(D-3) (2.4e+37 at 0.70, 9.3e+08 at 0.92, a ratio 2.6e+28 = (0.92/0.70)^240, with D - 3 = 239.4), and the scale-free ratio of the weakest raw sigma to the largest entry goes from 1.1e-64 at 0.70 to 2.8e-61 at 0.80 and 1.3e-46 at 0.92. I read the table, not a layout rule, from this: the issue asks where the sigma peaks and the answer is that it does not within 0.92.
