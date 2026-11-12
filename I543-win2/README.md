# I543-win2: a ladder of the last node at D 242.36, sigma against x_last

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/543 (follows from #537).
Start: crawlJ's state `I461-win2/crawlJ/anm_pin3_D242.3642.npz`, nodes 0.3, 0.4, 0.5, 0.6, 0.7. `renode_o.py ... --nodes 0.3,0.4,0.5,0.6,<x>` (`--last horizon`) for x = 0.66, 0.68, 0.69, 0.71, 0.74, 0.76, 0.80, then `near_null.py --k=4` and `near_null_eq.py --plant=7` on each; the baseline 0.70 and the layout 0.72 are #537's (`I537-win2/`, the same build). Two lanes of 2 threads shared with #544 (`lane_543_544_a.sh`, `lane_543_544_b.sh`, `layout_lib.sh`).
`renode_o.py` and `near_null.py` from `D:\choptuik-i446g/hp` at main 14dc386, `near_null_eq.py` from `D:\choptuik-i505/hp` at 0cce81e. Exit codes in `exits.txt`. Results follow in this README.

## Results (2026-11-12 03:09:26 to 03:45:35 UTC)

The lanes ran as planned (`lane_543_544_a.sh`, `lane_543_544_b.sh`, shared with #544; `exits.txt` has every start and exit). No Traceback, every exit as expected, every step under 6 minutes (the machine also ran #535 at 16 threads). The prediction of the fit was posted on the issue (comment 6814107622, 04:02 UTC, from `ladder_543.py --predict`, which reads only the layouts up to 0.76) before the 0.80 results and #502's layout were compared. The 0.80 layout had finished at 03:37 UTC while the other lane ran, and I had not opened its results.

**Checks.**

| step | result |
|---|---|
| `renode_o.py` for x_last = 0.66, 0.68, 0.69, 0.71, 0.74, 0.76, 0.80 | exit 0, check pass at each |
| `renode_o.py` x_last = 0.74, control `--mutate sign` | exit 1 as it must: rows 7.78e-01 -> 1.56e+00, check FAIL |
| `near_null.py --k=4` on the seven starts | exit 0, check pass at each |
| `near_null_eq.py --plant=7` on the seven starts | exit 0, check pass at each |

The baseline 0.70 and the layout 0.72 are #537's (`I537-win2/`, the same two builds, main 14dc386 and 0cce81e). The fit machinery was checked on planted laws first (`results_ladder_543_selftest.txt`, ok: a planted log law named log and recovered to 0.5%, a planted linear law named linear, a planted law with noise 0.5 failing the 0.1 check).

**Shifts of ln sigma_i from the 0.70 layout** (`ladder_543.py` -> `results_ladder_543.txt`):

| x_last | reading | ln sigma_1 | ln sigma_2 | ln sigma_3 | ln sigma_4 |
|---|---|---|---|---|---|
| 0.66 | raw | +16.263 | +16.266 | +16.253 | +16.266 |
| 0.66 | equilibrated | +2.506 | +2.490 | +2.472 | +2.474 |
| 0.68 | raw | +8.385 | +8.387 | +8.380 | +8.387 |
| 0.68 | equilibrated | +1.521 | +1.512 | +1.502 | +1.503 |
| 0.69 | raw | +4.260 | +4.261 | +4.258 | +4.261 |
| 0.69 | equilibrated | +0.839 | +0.834 | +0.828 | +0.829 |
| 0.70 | both | 0 | 0 | 0 | 0 |
| 0.71 | raw | -4.404 | -4.405 | -4.402 | -4.405 |
| 0.71 | equilibrated | -1.017 | -1.012 | -1.004 | -1.005 |
| 0.72 | raw | -8.964 | -8.965 | -8.958 | -8.965 |
| 0.72 | equilibrated | -2.228 | -2.218 | -2.202 | -2.203 |
| 0.74 | raw | -17.217 | -17.220 | -18.600 | -18.372 |
| 0.74 | equilibrated | -3.859 | -3.878 | -5.084 | -5.251 |
| 0.76 | raw | -24.359 | -17.319 | -20.171 | -19.827 |
| 0.76 | equilibrated | -1.406 | +2.140 | -0.768 | -2.569 |
| 0.80 | raw | -24.097 | -17.326 | -20.178 | -19.837 |
| 0.80 | equilibrated | +11.270 | +14.527 | +11.558 | +9.822 |

**Acceptance 1, the fit of ln sigma_3 against x_last by a + b x and a + b ln x: fails.** Over the eight layouts up to 0.76 the better form is a + b ln x in both readings, with rms residual 1.52 (raw) and 1.41 (equilibrated), against 1.65 and 1.43 for a + b x. Over all nine layouts the residual is 4.1 raw and 4.0 equilibrated. The equilibrated residual must be at most 0.1, and neither form reaches it.

**Why no one-law fit works: the sigma stop naming one mode at x_last >= 0.74** (`modes_543.py` -> `results_modes_543.txt`, a follow-up and not an acceptance; its classification was checked on planted lines first). From the logs' delta share and top components: up to 0.72 sigma_1 and sigma_2 are the harmonic-3 pair (delta share 1e-5 to 3e-4), sigma_3 and sigma_4 the harmonic-1 modes sharing the norm with Delta (0.70 and 0.30). At 0.76 and 0.80 sigma_1 is the pure Delta direction (delta share 1.00, raw 6.725e-38 and 8.736e-38), and sigma_2, sigma_3, sigma_4 are the harmonic-3 pair (7.61e-35, 7.63e-35) and a harmonic-1 mode (1.94e-34). The mixed Delta mode (the old sigma_3) falls with x_last by 3.9, 4.1, 4.3, 4.4, 4.6, 4.8 in ln per 0.01 from 0.66 to 0.74, then stops at about 7e-38 to 9e-38 (-4.3 per 0.01 on average from 0.74 to 0.76, +0.07 from 0.76 to 0.80). The harmonic-3 pair stops falling at 0.74 too (raw ln shift -17.2, -17.3, -17.3 at 0.74, 0.76, 0.80). The floor of about 8e-38 equals #493's "Delta alone, 8.43e-38" (I did not compute the norm of the Delta column here). Over the smooth regime 0.66 to 0.72 the Delta mode's raw ln sigma is fitted by a + b x with rms 0.25, by a + b ln x with 0.37, by a quadratic in x with 0.0078 (coefficients -87.119, +515.606, -677.960): the dependence is smooth and curved, and neither of the two forms named in the issue holds it.

**Acceptance 2, the prediction for #502's 0.3-0.8 layout and the 0.80 point, written before the comparison (comment 6814107622): refuted.** The fit to x_last <= 0.76 predicts the shift of ln sigma_3 at x_last = 0.80 as -37.2 (log) or -38.9 (linear) raw and -5.5 or -5.7 equilibrated. Measured at 0.80: -20.18 raw and +11.56 equilibrated; #502's six-node layout gives -20.26 and +11.56.

**The answer to "the last node or the last gap" is the last node.** The five-node layout 0.3, 0.4, 0.5, 0.6, 0.8 reproduces #502's six-node 0.3 ... 0.7, 0.8 layout (`compare_502_543.py` -> `results_compare_502_543.txt`; #502's values are those of its closing comment):

| reading | sigma_1 here / #502 | sigma_2 | sigma_3 | sigma_4 | largest difference |
|---|---|---|---|---|---|
| raw | -24.097 / -24.133 | -17.326 / -17.410 | -20.178 / -20.262 | -19.837 / -19.923 | 0.086 |
| equilibrated | +11.270 / +11.233 | +14.527 / +14.526 | +11.558 / +11.558 | +9.822 / +9.821 | 0.037 |

The equilibrated shifts of ln sigma_1..4 agree to 0.037 (0.001 for three of the four), so a layout with the node at 0.7 and one without it have the same weak spectrum when the last node is at 0.8. The control (#502's values against the 0.76 layout of this task) differs by 12.6 and exits 1. With #544, where none of the interior nodes or the first node moves any sigma, the weak directions are set by the position of the last node alone.

**Acceptance 3, renode checks and the sign control:** pass at all seven, the control exits 1 once.
