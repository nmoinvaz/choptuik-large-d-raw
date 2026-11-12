# I546-win: the pole constant C of QUAD_DOUBLE 13.6 at 130 and 160 series orders, D 50, 55 and 60

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/546 (the run part; the check_numbers check is the coordinator's; the coordinator's message `choptuik-large-d/2026-11-12/060901Z-coordinator-e804.md`). Worktree `choptuik-i546` at main e295b495 (it has `hp/pole_bc.py`), venv-t151's hpkernel and python-flint 0.9.0, two jobs of one thread each at BelowNormal, each under `I462-win/run_capped.py` with a cap of 14400 s.

| name | command (from `choptuik-i546/hp`, RAW = the raw clone) |
|---|---|
| ks130 | `python pole_bc.py RAW/I546-win/pole_bc_ks130.jsonl data/states/up8_D50.0075.npz data/states/up10_D55.0351.npz data/states/up13_D60.0020.npz --ks 130 --threads 1` |
| ks160 | the same with `--ks 160` and `pole_bc_ks160.jsonl` |

Then `python pole_bc.py summary pole_bc_ks130.jsonl > pole_bc_ks130_summary.log` and the same for ks160. #538 did D 40.02 and 45.05 at 130 and 160 orders (raw I538-mac) and all five states at 100 orders (`I538-mac/pole_bc_summary.log`); this folder is D 50, 55 and 60 at 130 and 160. The report gives C(a) and C(R136) at each D and order count beside #538's 100-order values.

## Results (2026-11-12)

Both jobs started at 06:10:27 UTC and ended at 06:10:34 and 06:10:36 UTC (7 and 9 s), exit 0 each, no Traceback: far under the 1 to 2 h estimate. `pole_bc_ks130.jsonl` and `pole_bc_ks160.jsonl` hold 27 records each (3 states x 9 deltas), the logs `pole_bc_ks*.log` the per-delta table and the fits, and `pole_bc_ks*_summary.log` the output of `pole_bc.py summary` (run with PYTHONUTF8=1 so that the file is UTF-8).

**C at three order counts, from 13.6's grid fit C = b (n - 1).** The 100-order values are #538's (`I538-mac/pole_bc_summary.log`), the 130- and 160-order values at D 40.02 and 45.05 are #538's (`pole_bc_ks130_D40_45_summary.log`, `pole_bc_ks160_D40_45_summary.log`), the other six are this folder's:

| D | C(R136) 100 orders | 130 | 160 | range | C(a) 100 orders | 130 | 160 | range | from |
|---|---|---|---|---|---|---|---|---|---|
| 40.0201 | 0.918 | 0.935 | 0.942 | 0.918 to 0.942 | 0.972 | 0.920 | 0.928 | 0.920 to 0.972 | #538 |
| 45.0507 | 0.914 | 0.935 | 0.943 | 0.914 to 0.943 | 0.966 | 0.919 | 0.933 | 0.919 to 0.966 | #538 |
| 50.0075 | 0.895 | 0.926 | 0.938 | 0.895 to 0.938 | 0.934 | 0.906 | 0.934 | 0.906 to 0.934 | this folder |
| 55.0351 | 0.874 | 0.913 | 0.933 | 0.874 to 0.933 | 0.900 | 0.912 | 0.924 | 0.900 to 0.924 | this folder |
| 60.0020 | 0.869 | 0.907 | 0.926 | 0.869 to 0.926 | 0.877 | 0.917 | 0.906 | 0.877 to 0.917 | this folder |

C(R136) rises with the order count at every state, and the rise from 130 to 160 orders is larger than the one at D 40: +0.007 at D 40.02, +0.008 at 45.05, +0.012 at 50.01, +0.020 at 55.04, +0.019 at 60.00 (from 100 to 130: +0.017, +0.021, +0.031, +0.039, +0.038). The range over 100 to 160 orders widens with D, from 0.024 at D 40.02 to 0.057 at D 60.00, and C(R136) is still rising at 160 orders at all five states (by 0.007 to 0.020 from 130 orders), so these are ranges and not limits. C(a) is not monotone in the order count (D 60.00: 0.877, 0.917, 0.906). 13.6's 0.88 lies inside the C(R136) range at D 55.04 (0.874 to 0.933) and D 60.00 (0.869 to 0.926) and below the range at D 40.02 (0.918 to 0.942), 45.05 (0.914 to 0.943) and 50.01 (0.895 to 0.938).

At 130 and 160 orders the pole_bc pass line of #538 (|s(R_new)| < 0.1 s(R136)) still prints FAIL at every one of the three states, as #538 found at 100 orders: s_new/s_R136 is 0.994, 0.996, 0.994 at 130 orders and 1.009, 0.995, 0.990 at 160 orders (#538: 0.999, 1.000, 1.000 at 100 orders). The where-test ranges are in the summaries. The check_numbers check of #546 is the coordinator's part.

## Extension: 200 and 250 orders for all five states (the coordinator's message 061423Z, 2026-11-12)

| job | command (from `choptuik-i546/hp`) | started (UTC) | ended (UTC) | exit |
|---|---|---|---|---|
| ks200 | `pole_bc.py RAW/I546-win/pole_bc_ks200.jsonl data/states/up7_D40.0201.npz data/states/up7_D45.0507.npz data/states/up8_D50.0075.npz data/states/up10_D55.0351.npz data/states/up13_D60.0020.npz --ks 200 --threads 1` | 06:15:12 | 06:15:30 | 0 |
| ks250 | the same with `--ks 250` and `pole_bc_ks250.jsonl` | 06:15:12 | 06:15:34 | 0 |

The kernel accepted both order counts (no message to report): 45 records each (5 states x 9 deltas), no Traceback, 18 and 22 s. Summaries `pole_bc_ks200_summary.log`, `pole_bc_ks250_summary.log` (UTF-8). The values below are from the summaries: 100 orders and the 130- and 160-order rows of D 40.02 and 45.05 are #538's, all others this folder's.

**C(R136)**

| D | 100 | 130 | 160 | 200 | 250 | change 100 to 130 per 100 orders | 130 to 160 | 160 to 200 | 200 to 250 |
|---|---|---|---|---|---|---|---|---|---|
| 40.0201 | 0.918 | 0.935 | 0.942 | 0.946 | 0.950 | +0.057 | +0.023 | +0.010 | +0.008 |
| 45.0507 | 0.914 | 0.935 | 0.943 | 0.953 | 0.958 | +0.070 | +0.027 | +0.025 | +0.010 |
| 50.0075 | 0.895 | 0.926 | 0.938 | 0.948 | 0.955 | +0.103 | +0.040 | +0.025 | +0.014 |
| 55.0351 | 0.874 | 0.913 | 0.933 | 0.946 | 0.954 | +0.130 | +0.067 | +0.032 | +0.016 |
| 60.0020 | 0.869 | 0.907 | 0.926 | 0.938 | 0.947 | +0.127 | +0.063 | +0.030 | +0.018 |

**C(a)**

| D | 100 | 130 | 160 | 200 | 250 | change 100 to 130 per 100 orders | 130 to 160 | 160 to 200 | 200 to 250 |
|---|---|---|---|---|---|---|---|---|---|
| 40.0201 | 0.972 | 0.920 | 0.928 | 0.939 | 0.942 | -0.173 | +0.027 | +0.027 | +0.006 |
| 45.0507 | 0.966 | 0.919 | 0.933 | 0.948 | 0.954 | -0.157 | +0.047 | +0.037 | +0.012 |
| 50.0075 | 0.934 | 0.906 | 0.934 | 0.944 | 0.952 | -0.093 | +0.093 | +0.025 | +0.016 |
| 55.0351 | 0.900 | 0.912 | 0.924 | 0.928 | 0.943 | +0.040 | +0.040 | +0.010 | +0.030 |
| 60.0020 | 0.877 | 0.917 | 0.906 | 0.923 | 0.940 | +0.133 | -0.037 | +0.043 | +0.034 |

C(R136) rises with the order count at every state, and the change per added order shrinks at every state: per 100 orders it goes from +0.057 to +0.130 between 100 and 130 orders, to +0.023 to +0.067 (130 to 160), to +0.010 to +0.032 (160 to 200) and to +0.008 to +0.018 (200 to 250). It has not stopped: between 200 and 250 orders C(R136) still rises by 0.004 (D 40.02), 0.005, 0.007, 0.008 and 0.009 (D 60.00), the values being printed to three decimals. At 250 orders C(R136) is 0.950, 0.958, 0.955, 0.954 and 0.947 for D 40.02 to 60.00, 0.067 to 0.078 above 13.6's 0.88. C(a) is not monotone in the order count (it falls between 100 and 130 orders at D 40.02, 45.05 and 50.01, and between 130 and 160 at D 60.00) and its change per added order does not shrink at D 55.04 (+0.010, then +0.030 per 100 orders); at 250 orders it is 0.942, 0.954, 0.952, 0.943 and 0.940.
