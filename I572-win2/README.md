# I572-win2: does the best last-node position depend on D? x_last 0.95 to 0.99 at D 237.13

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/572 (follows from #566).
Start: crawlI's state `I461-win2/crawlI/anm_pin3_D237.1312.npz`, nodes 0.3, 0.4, 0.5, 0.6, 0.7. #566's commands: `renode_o.py ... --nodes 0.3,0.4,0.5,0.6,<x>` for x = 0.95, 0.97, 0.98, 0.99, the control `--mutate sign` once (at 0.98), then `near_null.py --k=4` and `near_null_eq.py --plant=7` on each. Two lanes of 2 threads (`lane_572_a.sh`, `lane_572_b.sh`, `layout_lib.sh` with the source state set to crawlI's). `renode_o.py` and `near_null.py` from `D:\choptuik-i446g/hp` at main 14dc386, `near_null_eq.py` from `D:\choptuik-i505/hp` at 0cce81e. D 242.36's values (#566, #559) are beside them in the analysis. Exit codes in `exits.txt`. Results follow in this README.

## Results (2026-11-12 06:59:07 to 07:33:35 UTC)

Two lanes of 2 threads beside #558 and #566 (`lane_572_a.sh`, `lane_572_b.sh`; `exits.txt` has every start and exit). No Traceback, every exit as expected, no renode refusal, 9 to 13 min a layout.

**Checks.**

| step | result |
|---|---|
| `renode_o.py` for x_last = 0.95, 0.97, 0.98, 0.99 on crawlI's D 237.1312 | exit 0, check pass at each |
| `renode_o.py` x_last = 0.98, control `--mutate sign` | exit 1 as it must: rows 2.13e-16 -> 4.25e-16, check FAIL |
| `near_null.py --k=4` on the four | exit 0, check pass at each, ||J v_1|| / sigma_1 = 1.000000 |
| `near_null_eq.py --plant=7` on the four | exit 0, check pass at each, planted column scaling recovered to 2.1e-13, 7.1e-13, 8.8e-13, 3.4e-13 (bound 1e-3) |

**The weakest sigma at each layout, D 237.13** (`table_572.py` -> `results_table_572.txt`; its selftest, a planted peak located and a parabola recovering its vertex, was ok):

| x_last | raw sigma_1..4 (modes) | equilibrated sigma_1..4 | weakest equilibrated sigma | its mode (top scaled component) | largest abs J_ij |
|---|---|---|---|---|---|
| 0.95 | 1.850e-37 (D), 7.429e-35, 7.444e-35 (H3), 1.852e-34 (H1) | 2.953e-39, 8.030e-38, 8.481e-38, 1.010e-36 | 2.9529e-39 | Dz m_h k1 | 3.3e+05 |
| 0.97 | 1.937e-37 (D), 7.415e-35, 7.429e-35 (H3), 1.843e-34 (H1) | 4.092e-38, 9.658e-37, 1.057e-36, 6.866e-36 | **4.0924e-38** | Dz node4.m k1 | 2.5e+03 |
| 0.98 | 1.992e-37 (D), 7.408e-35, 7.422e-35 (H3), 1.838e-34 (H1) | 4.038e-38, 9.452e-37, 1.035e-36, 6.612e-36 | 4.0376e-38 | Dz node4.m k1 | 2.2e+02 |
| 0.99 | 2.039e-37 (D), 7.401e-35, 7.416e-35 (H3), 1.833e-34 (H1) | 3.526e-38, 8.229e-37, 9.063e-37, 5.734e-36 | 3.5255e-38 | Dz node4.m k1 | 1.9e+01 |

For comparison, D 242.36 (#559, #566): 1.246e-38 (0.96, Dz m_h k1), 3.008e-38 (0.97), 3.013e-38 (0.98), 2.612e-38 (0.99), 2.133e-38 (0.995), all Dz node4.m k1 from 0.97.

**Acceptance: the maximum at D 237.13 lies between 0.95 and 0.98 and is at about 0.974, 0.001 from D 242.36's 0.975.** The weakest equilibrated sigma is largest at x_last = 0.97 (4.0924e-38); it is 1.3% lower at 0.98 (4.0376e-38), 13.9% lower at 0.99 (3.5255e-38) and 14 times lower at 0.95 (2.9529e-39). A parabola in ln sigma through 0.95, 0.97, 0.98 has its vertex at 0.9748 (the script's), and one through 0.97, 0.98, 0.99 at 0.9739. The strict bracket of the maximum is the two neighbours 0.95 and 0.98 (0.03 wide, since there is no layout between 0.95 and 0.97), so "located to within 0.01" holds by the parabola and not by bracketing; the distance of the tabulated maximum from 0.975 is 0.005 and of the vertex 0.001 to 0.002, below the 0.02 of the check. The weakest direction's top scaled component is m_h k1 at 0.95 and node4.m k1 from 0.97 on, the same change as at D 242.36 (between 0.96 and 0.97). The raw weakest sigma (the Delta direction) rises slowly, 1.850e-37 at 0.95 to 2.039e-37 at 0.99, and the largest entry of J falls from 3.3e+05 to 19. So the peak does not move with D between 237.13 and 242.36 by more than the 0.01 spacing, and 0.975 is a good layout for both.
