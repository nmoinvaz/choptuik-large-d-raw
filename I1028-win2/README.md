# I1028-win2: M = 9 seeded repeats of the centre solve, start scatter against evaluation noise in r_1

Machine win2 (Windows desktop, x86), issue https://github.com/nmoinvaz/choptuik-large-d/issues/1028 (the coordinator's hc, 2026-11-19 ~14:19 UTC; #1012's recommended task 1, widened to four starts). Depends on #1012 (raw `I1012-win2/`, closing comment 7011704554).

## Setup

Four M = 9 centre solves at (A 2.719219, w/w_inf 1.000022), seeded from Z's harmonics (`0.148977988, 0.014770713, 0.008424206, 0.001511189, 0.000474205, 0.00012168` = B3 C3 B5 C5 B7 C7, as #1012's stage 1), scaled by 1 + 1e-9 (`p1`), 1 - 1e-9 (`m1`), 1 + 3e-9 (`p3`), 1 - 3e-9 (`m3`).
Command (`chain1028.py`): `hier_nb.py 9 2.719219 1.000022 --x=<scaled harmonics> --xi1=0.15 --pretune --fixA --schur --predict --procs 2 --h3=1e-4 --h5=1e-4 --floor_max=1e-4 --verbose=2 --approach=5:0.105 --polish=5:0.11`, `INNER_NB_RTOL=1e-13`, BelowNormal, 3 h caps, all four side by side (8 processes), from `D:\choptuik-h9b` (main 299c4eb9).
Stage 1 (#1012's XI 0.11 run, seeded with the unscaled harmonics) ran from `D:\choptuik-inner` at main 23844822; `diff` of hier.py, hier_nb.py and inner_nb.py between the two extracts shows only the `--h9` plumbing (unused here), so the code is the same for these settings. Stage 1's log is `../I1012-win2/logs/hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-4_win2.log`; the unseeded `zero_repeat` is `..._outer_zero_repeat_win2.log` there.
Logs `logs/hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-4_seed_{p1,m1,p3,m3}_win2.log`, `.exit` files, driver log `logs/run1028.driver.log`.

## Checks, fixed before the runs (the issue's, and mine)

- **Driver (the issue's):** each log's starting harmonics (the `pretuned x` line, full precision) differ from Z's by the stated factor, |x/Z - 1 - eps| < 1e-14, and (A, w) = (2.719219, 1.000022); the K line says 10 residuals (`--predict`). The driver reads them back from each log as it runs and logs `PLUMBING MISMATCH` otherwise. Selftest `logs/selftest_chain1028.txt`: PASS; `--mutate=nofactor` (p1 without its factor), `--mutate=nokill` (stubs left running) and `--mutate=badreadback` (m3's stub prints unscaled harmonics) each FAIL.
- **Analysis script (`m9_seeded_std.py`, written during the runs, before any end value is read):** the statistic and the decision below; its planted-truth selftest and mutations are in `logs/selftest_m9_seeded_std.txt`.

## Reading, fixed before the data

- **The statistic.** The five seeded values are r_1 (re, im) of stage 1 and of p1, m1, p3, m3 (the FIXED-A line of each log, 4 significant digits as printed). The scatter is the sample standard deviation (ddof 1) of each component, combined in norm as sqrt(std_re^2 + std_im^2). The same definition gave the fixed-x noise 7.7e5 (`noise_analyze.py`: std over samples, norm over the two components) and the 1.5e6 and 3.0e6 of #1012's closing reading, so the numbers compare. `zero_repeat` (unseeded) is listed beside them and is NOT in the five.
- **The decision (the issue's):** std <= 1e6 means the omega error is about 7.5e-5 (that is, std / sigma_min(J) with #1012's sigma_min 1.03e10), the 1e-4 rule is not triggered, and J is refitted on the mean of the five centres (`m9_outer.py`, as a reading here, not a new run), after which one solve at the Newton-predicted zero is the coordinator's to order. std >= 2e6 means start-to-start scatter governs, the error is about 2.7e-4 and M = 9 is not reachable at this radius in double precision. Between 1e6 and 2e6: reported, the coordinator decides.
- **How far five values pin the std** (stated now so nobody reads more into the number): with 4 degrees of freedom the true std per component is within [0.65, 2.4] x the measured one at 90%. A measured 1.5e6 therefore does not distinguish 1e6 from 2e6, and I report the interval beside the number.
- **Also listed, descriptive only (not part of the decision):** each run's end r_3, r_5, r_7, r_9, and the difference of each r_1 from stage 1's, to see whether r_1 follows the end |r_3| (the rpi5 reading at M = 7, #1002/#1004) or the harmonics' perturbation.
- **A run that caps before its FIXED-A line** has no r_1. The std is then taken over the values there are (n < 5, said in the post) and the interval widens.
