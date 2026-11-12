# I559-win2: the last-node ladder to 0.98 at D 242.36

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/559 (follows from #554).
Start: crawlJ's state `I461-win2/crawlJ/anm_pin3_D242.3642.npz`, nodes 0.3, 0.4, 0.5, 0.6, 0.7. #554's commands (`I554-win2/lane_554.sh`): `renode_o.py ... --nodes 0.3,0.4,0.5,0.6,<x>` for x = 0.94, 0.96, 0.98, then `near_null.py --k=4` and `near_null_eq.py --plant=7` on each; the control `--mutate sign` once (at 0.96). One lane of 2 threads (`lane_559.sh`, `layout_lib.sh`).
`renode_o.py` and `near_null.py` from `D:\choptuik-i446g/hp` at main 14dc386, `near_null_eq.py` from `D:\choptuik-i505/hp` at 0cce81e. Exit codes in `exits.txt`. Results follow in this README.

## Results (2026-11-12 05:19:58 to 05:59:42 UTC)

One lane of 2 threads beside #529, #557, #558, #560 and others (`lane_559.sh`; `exits.txt` has every start and exit). No Traceback, every exit as expected, 10 to 13 min a layout (the machine was busy).

**Checks.**

| step | result |
|---|---|
| `renode_o.py` for x_last = 0.94, 0.96, 0.98 | exit 0, check pass at each (the gap between the horizon series and the Taylor steps 4.9e-36 in p and 4.8e-36 in m at 0.98; node 0.98 refined by block 5, rows 1.94e-16 -> 0.00) |
| `renode_o.py` x_last = 0.96, control `--mutate sign` | exit 1 as it must: rows 1.81e-16 -> 3.63e-16, check FAIL |
| `near_null.py --k=4` on the three | exit 0, check pass at each, ||J v_1|| / sigma_1 = 1.000000 |
| `near_null_eq.py --plant=7` on the three | exit 0, check pass at each, planted column scaling recovered to 1.6e-13, 2.6e-13, 3.6e-13 (bound 1e-3) |

No renode refusal. The analysis is `ladder_559.py` (`ladder_554.py` with the three new layouts added; selftest ok), `results_ladder_559.txt` has every sigma and mode for 0.70 to 0.98.

**The weakest sigma at each layout** (the layouts 0.82 to 0.92 are #554's):

| x_last | weakest raw sigma (mode) | weakest equilibrated sigma | its mode (top scaled component; Dz: delta share 0.9 or more in z) | largest \|J_ij\| | ln of the equilibrated one |
|---|---|---|---|---|---|
| 0.90 | 1.157e-37 (D) | 3.156e-44 | Dz m_h k1 | | -100.16 |
| 0.92 | 1.246e-37 (D) | 2.037e-42 | Dz m_h k1 | 9.3e+08 | -96.00 |
| 0.94 | 1.264e-37 (D) | 1.650e-40 | Dz m_h k1 | 5.4e+06 | -91.60 |
| 0.96 | 1.305e-37 (D) | 1.246e-38 | Dz m_h k1 | | -87.28 |
| 0.98 | 1.365e-37 (D) | **3.013e-38** | Dz node4.m k1 | 2.5e+02 | -86.40 |

Equilibrated sigma_1..4 at 0.98: 3.013e-38, 1.007e-36, 1.099e-36, 7.014e-36 (modes: Dz node4.m k1, node4.m k3, Dz node4.m k3, Dz node4.a k2); at 0.96: 1.246e-38, 4.552e-37, 4.472e-37, 3.988e-36.

**Acceptance: the weakest equilibrated sigma is largest at the end of the range, x_last = 0.98 (3.013e-38), and the rise has nearly stopped there.** The increase of ln per 0.02 of x_last was 4.4 (0.92 to 0.94) and 4.3 (0.94 to 0.96) and is **0.9 (0.96 to 0.98)**, 3.4 below the 4.3 that the earlier steps (6.0, 6.1, 6.2, 5.4, 4.8, 4.2, 4.4, 4.3) would continue to; the value at 0.98 is about 30 times (e^3.4) below that extrapolation. The mode of the weakest direction also changes at 0.98: its top scaled component is the last node's field (node4.m k1) and not m_h k1 as at every layout from 0.75 to 0.96, and the whole spectrum's top components are node4's (node4.m k3, node4.a k2). The largest entry of J has fallen to 2.5e+02 at 0.98 (it was 2.4e+37 at 0.70), so the gain x_last^-(D-3) is nearly gone and the last node sits at u0 = 0.02 from the horizon. The raw weakest sigma stays the Delta direction (delta share 1.00), 1.246e-37 at 0.92 and 1.365e-37 at 0.98. So the maximum lies at 0.96 to 0.98 or beyond, and I cannot locate it closer with three layouts above 0.92: it is at the end of the range as sampled, with a change of regime between 0.96 and 0.98.
