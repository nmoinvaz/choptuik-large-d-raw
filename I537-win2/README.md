# I537-win2: which exponential is the wall, one node moved at D 242.36

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/537 (depends on #489 and #502).
Start: crawlJ's state `I461-win2/crawlJ/anm_pin3_D242.3642.npz` (layout 0.3, 0.4, 0.5, 0.6, 0.7). Two lanes of 2 threads each, Python only, venv-t126.
Lane A (`lane_a.sh`): `renode_o.py` to first node 0.35 (nodes 0.35,0.4,0.5,0.6,0.7), then `near_null.py --k=4` and `near_null_eq.py --plant=7` on that start, then both on crawlJ's own state (the baseline).
Lane B (`lane_b.sh`): `renode_o.py` to last node 0.72 (nodes 0.3,0.4,0.5,0.6,0.72), its control `--mutate sign`, then `near_null.py` and `near_null_eq.py` on that start, and the control `near_null.py --mutate=sigma`.
`renode_o.py` and `near_null.py` from `D:\choptuik-i446g/hp` at main 14dc386, `near_null_eq.py` from `D:\choptuik-i505/hp` at 0cce81e. Exit codes in `exits.txt`. Results follow in this README.

## Results (2026-11-12 02:50:08 to 03:04:21 UTC)

Both lanes ran as the issue wrote them (`lane_a.sh`, `lane_b.sh`; `exits.txt` has every start and exit). No Traceback, and every step took under 5 minutes (the two renodes 2 s each, `near_null.py` 3.4 to 3.7 min, `near_null_eq.py` 3.7 to 4.1 min; the whole task 14 min with two lanes of 2 threads).

**Checks.**

| step | result |
|---|---|
| `renode_o.py` first node 0.35 | exit 0, check pass: node 0.35 refined by block 0 (centre series), its rows 2.37e-31 -> 0.00e+00 |
| `renode_o.py` last node 0.72 | exit 0, check pass: node 0.72 refined by block 5 (horizon series), its rows 5.48e+02 -> 1.07e-128 |
| `renode_o.py` last node 0.72, control `--mutate sign` | exit 1 as it must: rows 5.48e+02 -> 1.10e+03, check FAIL |
| `near_null.py --k=4` on crawlJ's state, the first-node start, the last-node start | exit 0, check pass at each: sigma_1 converged to 2e-04, 2e-04, 1e-04 and ||J v_1|| / sigma_1 = 0.999424, 0.999373, 0.999518 |
| `near_null.py --mutate=sigma` on the last-node start | exit 1 as it must: ||J v_1|| / sigma_1 = 0.951922, check FAIL |
| `near_null_eq.py --plant=7` on the same three | exit 0, check pass at each: planted column scaling recovered to 1.1e-15, 3.0e-15, 2.0e-15 (bound 1e-3), ||J_eq v_1|| / sigma_1 = 1.000000 |

The re-noded starts are read without a polish, as the issue says: their pinned max|F| is 5.57e-34 (first node) and 1.62e-34 (last node) against 7.99e-38 at crawlJ's state. The pivot range of the octo-double LU is 3.5e-25 to 3.3e+34 for the baseline and the first-node start, and 4.4e-29 to 4.0e+31 for the last-node start.

**Raw and equilibrated sigma_1..4** (`near_null.py` main 14dc386, `near_null_eq.py` 0cce81e, Curtis-Reid + Ruiz; `table_537.py` -> `results_table_537.txt`):

| layout | raw sigma_1 | raw sigma_2 | raw sigma_3 | raw sigma_4 | equilibrated sigma_1 | sigma_2 | sigma_3 | sigma_4 |
|---|---|---|---|---|---|---|---|---|
| baseline (0.3 ... 0.7) | 2.5510e-27 | 2.5300e-27 | 4.3920e-26 | 7.9300e-26 | 1.8825e-61 | 9.3856e-61 | 2.6498e-59 | 2.4555e-57 |
| first node 0.35 (0.35 ... 0.7) | 2.5320e-27 | 2.5140e-27 | 4.3830e-26 | 7.8960e-26 | 1.8832e-61 | 9.3894e-61 | 2.6525e-59 | 2.4581e-57 |
| last node 0.72 (0.3 ... 0.72) | 3.2650e-31 | 3.2330e-31 | 5.6530e-30 | 1.0130e-29 | 2.0276e-62 | 1.0212e-61 | 2.9314e-60 | 2.7134e-58 |

**Shifts of ln sigma from the baseline** (new layout minus baseline):

| change | reading | ln sigma_1 | ln sigma_2 | ln sigma_3 | ln sigma_4 |
|---|---|---|---|---|---|
| first node 0.3 -> 0.35 | raw | -0.01 | -0.01 | -0.00 | -0.00 |
| first node 0.3 -> 0.35 | equilibrated | +0.00 | +0.00 | +0.00 | +0.00 |
| last node 0.7 -> 0.72 | raw | -8.96 | -8.97 | -8.96 | -8.97 |
| last node 0.7 -> 0.72 | equilibrated | -2.23 | -2.22 | -2.20 | -2.20 |

**Verdict by the issue's rule** (the rule applied by `table_537.py`; its verdict function was checked on eight planted shift pairs first, `results_table_537_selftest.txt`, ok):

| reading | first shift of ln sigma_3 | last shift | fast mode (+41, -13.7 within 20%) | G^p (first below 8.2 in size, last positive) |
|---|---|---|---|---|
| raw | -0.00 (0% of +41) | -8.96 (65% of -13.7) | excluded | excluded |
| equilibrated | +0.00 (0% of +41) | -2.20 (16% of -13.7) | excluded | excluded |

**Neither model holds.** The first-node move leaves every sigma unchanged to under 1% (raw) and 0.1% (equilibrated), which excludes the fast mode's +41 and is what G^p predicts (0). The last-node move shifts all four sigma down, by 8.96 (raw) and 2.20 (equilibrated) in ln, which is the wrong sign for G^p (it needs a positive shift) and 65% and 16% of the fast mode's -13.7. In the issue's parametrisation the last shift would be p = -1.34 (raw) or p = -0.33 (equilibrated), a negative exponent, which the rule does not count as G^p. The raw and equilibrated readings agree on the verdict (neither model) and differ in size by a factor 4 (-8.96 against -2.20), as raw sigma are not comparable across layouts (#502); the last node's move changes the row and column scales, and equilibration removes about three quarters of the shift.
All four sigma move together: the four shifts agree to 0.01 (raw) and 0.03 (equilibrated). What the last-node move changes is a common scale of the weak directions and not sigma_3 against the others.
