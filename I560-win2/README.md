# I560-win2: does the Delta direction's raw sigma floor depend on D? Layout 0.80 at D 232.63, 237.13 and 242.36

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/560 (follows from #553 and #554).
States: crawlG D 232.6312 (`I461-win2/crawlG/anm_pin3_D232.6312.npz`), crawlI D 237.1312 (`I461-win2/crawlI/anm_pin3_D237.1312.npz`) and crawlJ D 242.3642, each with nodes 0.3, 0.4, 0.5, 0.6, 0.7, re-noded by `renode_o.py ... --nodes 0.3,0.4,0.5,0.6,0.8` and read by `near_null.py --k=4`. At D 242.36 the same renode is #543's (`I543-win2/renode_last080_D242.3642.npz`, whose `nn_last080.log` is the issue's 8.7e-38); here `near_null.py` is run on it again as a reproducibility control. The controls `--mutate sign` (renode, on D 237.13) and `--mutate=sigma` (near_null, on D 232.63) once each. One lane of 2 threads (`lane_560.sh`, `layout_lib.sh`).
`renode_o.py` and `near_null.py` from `D:\choptuik-i446g/hp` at main 14dc386. Exit codes in `exits.txt`. Results follow in this README.

## Results (2026-11-12 05:20:02 to 05:36:44 UTC)

One lane of 2 threads (`lane_560.sh`; `exits.txt` has every start and exit). No Traceback, every exit as expected, 4 min a `near_null.py` (the octo-double LU 113 to 128 s).

**Checks.**

| step | result |
|---|---|
| `renode_o.py` crawlG D 232.6312 and crawlI D 237.1312 to nodes 0.3,0.4,0.5,0.6,0.8 | exit 0, check pass (node 0.8 refined by block 5, horizon series, rows 5.65e-10 -> 0.00 and 1.46e-09 -> 0.00) |
| `renode_o.py` D 237.13, control `--mutate sign` | exit 1 as it must: rows 1.46e-09 -> 2.92e-09, check FAIL |
| `near_null.py --k=4` at D 232.63, D 237.13 and on #543's D 242.36 layout | exit 0, check pass at each, ||J v_1|| / sigma_1 = 1.000000 |
| `near_null.py --mutate=sigma` at D 232.63 | exit 1 as it must: ratio 0.952381, check FAIL |

**The weakest raw sigma, the Delta direction, and the others, at layout 0.3, 0.4, 0.5, 0.6, 0.8** (`nn_D232.log`, `nn_D237.log`, `nn_D242.log`):

| D | sigma_1 (delta share) | sigma_2 | sigma_3 | sigma_4 |
|---|---|---|---|---|
| 232.6312 | **1.593e-37** (1.00) | 7.575e-35 (3.2e-04) | 7.598e-35 (2.4e-05) | 1.919e-34 (7.2e-04) |
| 237.1312 | **1.240e-37** (1.00) | 7.569e-35 (1.1e-04) | 7.588e-35 (4.2e-06) | 1.922e-34 (6.7e-04) |
| 242.3642 | **8.736e-38** (1.00) | 7.563e-35 (1.1e-04) | 7.579e-35 (4.1e-06) | 1.924e-34 (6.3e-04) |

At D 242.36 the value is #553's and #543's 8.736e-38 to the four digits printed: the reproducibility run agrees. **The Delta direction's raw sigma falls from 1.593e-37 at D 232.63 to 8.736e-38 at D 242.36, by 45.2% (a factor 0.548), more than the 20% the issue asks about.** It falls smoothly, about 6% per unit of D (ln sigma changes by -0.0557 per unit between 232.63 and 237.13 and -0.0669 between 237.13 and 242.36). The other three sigma do not move: the harmonic-3 pair stays at 7.57e-35 to 7.60e-35 (0.3% over the same range) and sigma_4 at 1.92e-34 (0.3%). So the floor of about 1e-37 is not a fixed number: it depends on D, smoothly and by more than any rounding would, while the rest of the weak spectrum does not. That excludes a roundoff constant; whether the dependence is the physical one of the Delta direction I did not test beyond these three D.
