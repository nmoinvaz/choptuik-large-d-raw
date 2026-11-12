# I544-win2: which nodes the weak directions feel, each interior node moved by 0.02 at D 242.36

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/544 (follows from #537).
Start: crawlJ's state `I461-win2/crawlJ/anm_pin3_D242.3642.npz`, nodes 0.3, 0.4, 0.5, 0.6, 0.7; the baseline is #537's (`I537-win2/`, the same build). `renode_o.py` to nodes 0.3,0.42,0.5,0.6,0.7; 0.3,0.4,0.52,0.6,0.7; 0.3,0.4,0.5,0.62,0.7 and 0.25,0.4,0.5,0.6,0.7, then `near_null.py --k=4` and `near_null_eq.py --plant=7` on each. Two lanes of 2 threads shared with #543 (`I543-win2/lane_543_544_a.sh`, `lane_543_544_b.sh`, `layout_lib.sh`, copied here).
`renode_o.py` and `near_null.py` from `D:\choptuik-i446g/hp` at main 14dc386, `near_null_eq.py` from `D:\choptuik-i505/hp` at 0cce81e. Exit codes in `exits.txt`. Results follow in this README.

## Results (2026-11-12 03:37:43 to 04:02:56 UTC)

The lanes ran as planned (`lane_543_544_a.sh`, `lane_543_544_b.sh`, shared with #543; `exits.txt` has every start and exit). No Traceback, every exit as expected, every step under 6 minutes (the machine also ran #535 at 16 threads).

**Checks.**

| step | result |
|---|---|
| `renode_o.py` to 0.3,0.42,0.5,0.6,0.7; 0.3,0.4,0.52,0.6,0.7; 0.3,0.4,0.5,0.62,0.7; 0.25,0.4,0.5,0.6,0.7 | exit 0, check pass at each |
| `renode_o.py` to 0.25,0.4,0.5,0.6,0.7, control `--mutate sign` | exit 1 as it must: node 0.25 refined by block 0 (centre series), rows 1.06e-16 -> 2.12e-16, check FAIL |
| `near_null.py --k=4` on the four starts | exit 0, check pass at each, ||J v_1|| / sigma_1 = 0.999576, 0.999501, 0.999478, 0.999499 |
| `near_null.py --mutate=sigma` on the 0.25 start | exit 1 as it must: ratio 0.951904, check FAIL |
| `near_null_eq.py --plant=7` on the four starts | exit 0, check pass at each, planted column scaling recovered to 3.9e-15, 1.8e-15, 2.3e-15, 2.2e-15 (bound 1e-3) |

The baseline is #537's (`I537-win2/`, the same two builds, main 14dc386 and 0cce81e). The null test of `nodes_544.py` was checked on planted shifts first (`--selftest`, ok).

**Raw and equilibrated sigma_1..4** (`nodes_544.py` -> `results_nodes_544.txt`):

| layout | raw sigma_1 | raw sigma_2 | raw sigma_3 | raw sigma_4 | equilibrated sigma_1 | sigma_2 | sigma_3 | sigma_4 |
|---|---|---|---|---|---|---|---|---|
| baseline 0.3, 0.4, 0.5, 0.6, 0.7 (#537) | 2.5510e-27 | 2.5300e-27 | 4.3920e-26 | 7.9300e-26 | 1.8825e-61 | 9.3856e-61 | 2.6498e-59 | 2.4555e-57 |
| second node 0.4 -> 0.42 | 2.5460e-27 | 2.5190e-27 | 4.3880e-26 | 7.9130e-26 | 1.8826e-61 | 9.3861e-61 | 2.6501e-59 | 2.4558e-57 |
| third node 0.5 -> 0.52 | 2.5440e-27 | 2.5190e-27 | 4.3870e-26 | 7.9090e-26 | 1.8825e-61 | 9.3857e-61 | 2.6499e-59 | 2.4556e-57 |
| fourth node 0.6 -> 0.62 | 2.5430e-27 | 2.5200e-27 | 4.3870e-26 | 7.9060e-26 | 1.8825e-61 | 9.3855e-61 | 2.6497e-59 | 2.4554e-57 |
| first node 0.3 -> 0.25 | 2.5690e-27 | 2.5440e-27 | 4.3990e-26 | 7.9600e-26 | 1.8818e-61 | 9.3815e-61 | 2.6469e-59 | 2.4527e-57 |
| last node 0.7 -> 0.72 (#537) | 3.2650e-31 | 3.2330e-31 | 5.6530e-30 | 1.0130e-29 | 2.0276e-62 | 1.0212e-61 | 2.9314e-60 | 2.7134e-58 |

**Shifts of ln sigma_3 from the baseline** (the equilibrated column is the one the issue asks for; the shifts of the other three sigma are in `results_nodes_544.txt` and agree):

| node move | equilibrated shift of ln sigma_3 | raw shift | per unit of node displacement (equilibrated) |
|---|---|---|---|
| second node 0.4 -> 0.42 | +0.000 | -0.001 | +0.0 |
| third node 0.5 -> 0.52 | +0.000 | -0.001 | +0.0 |
| fourth node 0.6 -> 0.62 | -0.000 | -0.001 | -0.0 |
| first node 0.3 -> 0.25 | -0.001 | +0.002 | +0.0 |
| last node 0.7 -> 0.72 (#537, for scale) | -2.202 | -8.958 | -110.1 |

Acceptance: the table is above; **the 0.25 move reproduces the null** (shift of ln sigma_3 +0.0016 raw, -0.0011 equilibrated, both under 0.01, as the 0.35 move of #537 gave -0.00 and +0.00); all check lines pass and both controls exit 1.

**What this says.** No node but the last one moves any of the four sigma: the three interior nodes, each moved by 0.02, and the first node, moved by 0.05 each way, change ln sigma_1..4 by 0.001 or less (equilibrated) and under 0.01 (raw), against 2.2 (equilibrated) and 9.0 (raw) for the last node moved by the same 0.02. The fourth node 0.6 -> 0.62 also shortens the gap to the last node (0.1 -> 0.08) and changes nothing, so the sensitivity is not the last gap; with #543 (the five-node 0.3, 0.4, 0.5, 0.6, 0.8 layout reproduces #502's six-node 0.3-0.8 layout) it is the position of the last node.
