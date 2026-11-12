# I585-win2: the double-double noise of det M(lambda) at five points of kf 27, and a planted zero with and without that noise

Issue https://github.com/nmoinvaz/choptuik-large-d/issues/585 (assigned by the coordinator at 09:12 UTC, 2026-11-12). Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB). Code: worktree `D:\choptuik-i573` at main 80b5056 (`hp/modecount_circle.py`, `hp/modecount_common.py` `setup`), the same build as `I574-win2/README.md` (`modecount_cx.cp312-win_amd64.pyd` sha256 7ab672ea9a17b239eb77897aaf5ec32de00580b70c3522707785b3bec4e722c3, rustc 1.96.0, Python 3.12.8 in venv-t126).
State `hp/data/modecount_state_D61.0264_M48_kf27.npz` sha256 1fd892fcd0e326276b1885f10fc42421d917590f298e585867adb3fc352e8ac1, seed `hp/data/seeds/local/up23_D61.0264.npz` sha256 c3393ce849de0f11406a02c5227a32cbb41795d29f5d8c2856fb2093a463a948. Every evaluation is `setup(..., M=48, threads=1, kf=27, fmax=1e-15).det(re, im)`, one thread per process.
Pre-registered before any evaluation of this task: `points_585.json` (the five points) and `predictions_585.json` (the design, seven criteria P1 to P7 and the controls), committed to the raw-data repository before the run. Results follow in this README.

## Results (2026-11-12 09:16 to 10:16 UTC)

**Summary.** Under single-ulp moves of λ, ln|det M| and arg det M change by 1e-4 to 4e-3 (std) at the five points, 8 to 10 orders more than the analytic change over 25 ulps, and identical arguments repeat bit for bit. The noise is larger near a zero (std 2.1e-3 to 4.2e-3 at 0.02 from a zero) than far from one (1.4e-4 to 4.2e-4). A zero planted on the cached determinants of the two kf 27 R 0.06 circles is recovered within the circle's own estimate when the cached values are used as they are (8 of 8), and with extra noise of the measured size its position scatters by 1.2e-4 to 1.7e-4 (rms), above the own estimate for circle A and about equal to it for circle B. The prediction P3 failed. The predictions were fixed and committed before any evaluation (`predictions_585.json`, raw 300133ad).

### 1. Spread under ulp moves (5 points, 515 evaluations)

16 worker processes (one thread each), 851 s (`noise_585.py`, `noise_585.log`, `evals_585.jsonl`); the table is `results_585_spread.txt` (`analyze_585.py`, whose `--selftest` recovers a known sigma within 15% and reports below 1e-12 on a smooth function, and whose `--mutate=repeat` makes P4 fail). Each point: the reference, 25 moves of Re by j ulp, 25 moves of Im, 50 repeats at the identical argument (separate tasks over 15 worker processes), two points at Re ± 1e-3. The std is over the 51 values; the "smooth change" is |d ln det / dλ| × 25 ulp from the points at Re ± 1e-3.

| point | kind | values | std ln\|det\| | std arg | max \|dev\| ln | max \|dev\| arg | median \|dev\| j<=5 | j>=21 | \|dlnf/dlam\| | smooth change over 25 ulp | spread / smooth | distinct ln values | 50 repeats bit equal | workers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| N1 | near | 51 | 2.16e-03 | 2.09e-03 | 7.56e-03 | 9.66e-03 | 3.35e-03 | 1.78e-03 | 92.5 | 5.14e-13 | 5.85e+09 | 51 | yes (50) | 15 |
| N2 | near | 51 | 4.19e-03 | 3.57e-03 | 9.28e-03 | 8.15e-03 | 3.04e-03 | 2.32e-03 | 72.8 | 8.08e-13 | 6.80e+09 | 51 | yes (50) | 15 |
| F1 | far | 51 | 3.62e-04 | 3.58e-04 | 1.23e-03 | 1.68e-03 | 5.89e-04 | 4.94e-04 | 49 | 5.44e-13 | 9.36e+08 | 51 | yes (50) | 15 |
| F2 | far | 51 | 2.60e-04 | 4.16e-04 | 8.10e-04 | 1.15e-03 | 2.58e-04 | 1.83e-04 | 54.4 | 6.04e-13 | 8.12e+08 | 51 | yes (50) | 15 |
| F3 | far | 51 | 1.67e-04 | 1.42e-04 | 6.18e-04 | 3.72e-04 | 2.67e-04 | 2.62e-04 | 54.2 | 1.20e-12 | 1.82e+08 | 51 | yes (50) | 15 |

| prediction | verdict |
|---|---|
| P1: both std between 1e-5 and 1e-2 at all five points | holds (1.4e-4 to 4.2e-3 over all five) |
| P2: median \|deviation\| for j ≤ 5 within a factor 3 of that for j ≥ 21 | holds (flat in j, not growing) |
| **P3: near/far ratio of the median std of ln\|det\| between 1 and 10** | **fails: 12.2** |
| P4: 50 repeats at the identical argument bit for bit equal | holds at all five points, 15 worker processes |
| P5: spread / smooth change above 1e6 | holds (1.8e8 to 6.8e9) |

Every one of the 51 values at each point is distinct (51 distinct ln|det| of 51). The pooled std of the near points (N1, N2) is 3.33e-3 in ln|det| and 2.92e-3 in arg, of the far points (F1 to F3) 2.75e-4 and 3.27e-4 (`sigma_585.json`). What the std is: a sample std over 51 arguments within 25 ulps, the rms of the evaluation's rounding noise there, not a bound (the largest deviation is 9.3e-3 in ln|det| and 9.7e-3 in arg, both near points).

### 2. A planted zero (8 cases, 200 noise realizations each)

`planted_585.py`: for each of the two kf 27 R 0.06 circles (A: #574's at 1.902797 + 0.916032i, zero 1.903548 + 0.910715i; B: the new one at 2.396619 + 0.547672i, winding +1, zero 2.396581 + 0.547584i, estimate 3.6e-6, `k27_z_re2.3966_im+0.5477/`) and λ₀ = centre + 0.025 e^{iφ}, φ = 0, 90, 180, 270°, the cached determinants times (λ − λ₀), W = 2, n0 20, tol π/4, `circle()` as in the real runs. Points the bisections need that are not cached (16 to 20 a case in the first run) were computed with the same state and saved (`extra_*.jsonl`); in the rerun they were preloaded, so the column 'extra points' below shows only the 6 that case B_270 still needed. The unplanted replay of each circle reproduces its stored zero exactly (difference 0.0), and noise of sigma 0 changes nothing. Selftest: an analytic determinant with two zeros recovers both to 1e-9 for the four φ; `--mutate=sign` and a moved cached value must fail it, and do. The first run died at the JSON dump of its first finished case (a numpy bool in the result record) after seven cases had computed and written truncated result files (`planted_585_failed_run.log`); the dump and the preloading were fixed and all eight cases rerun from the start, with the same seeds, so the noise realizations are the same ones.

**Registered noise (the near points' sigma), `results_585_planted.txt`:**

| case | lam0 | replay equals stored | W | recovered lam0, error | own estimate | within (P6) | sigma 0 identical | rms error, noise | rms / estimate | rms move | frac over estimate | extra points | bad realizations |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A_0 | 1.92780+0.91603i | 0.0e+00 | 2 | 1.9278002+0.9160553i, 2.35e-05 | 5.61e-05 | yes | True | 1.50e-04 | 2.67 | 1.48e-04 | 0.92 | 0 | 0 |
| A_180 | 1.87780+0.91603i | 0.0e+00 | 2 | 1.8778032+0.9160107i, 2.22e-05 | 5.30e-05 | yes | True | 1.31e-04 | 2.47 | 1.29e-04 | 0.80 | 0 | 0 |
| A_270 | 1.90280+0.89103i | 0.0e+00 | 2 | 1.9027676+0.8910285i, 2.96e-05 | 7.06e-05 | yes | True | 1.75e-04 | 2.48 | 1.72e-04 | 0.87 | 0 | 0 |
| A_90 | 1.90280+0.94103i | 0.0e+00 | 2 | 1.9028162+0.9410331i, 1.92e-05 | 4.60e-05 | yes | True | 1.20e-04 | 2.61 | 1.19e-04 | 0.85 | 0 | 0 |
| B_0 | 2.42162+0.54767i | 0.0e+00 | 2 | 2.4216362+0.5476477i, 2.98e-05 | 1.46e-04 | yes | True | 1.51e-04 | 1.04 | 1.49e-04 | 0.38 | 0 | 0 |
| B_180 | 2.37162+0.54767i | 0.0e+00 | 2 | 2.3716015+0.5476963i, 2.99e-05 | 1.46e-04 | yes | True | 1.45e-04 | 0.99 | 1.44e-04 | 0.35 | 0 | 0 |
| B_270 | 2.39662+0.52267i | 0.0e+00 | 2 | 2.3966435+0.5226893i, 3.00e-05 | 1.48e-04 | yes | True | 1.47e-04 | 0.99 | 1.45e-04 | 0.39 | 6 | 0 |
| B_90 | 2.39662+0.57267i | 0.0e+00 | 2 | 2.3965947+0.5726547i, 2.98e-05 | 1.47e-04 | yes | True | 1.50e-04 | 1.02 | 1.47e-04 | 0.41 | 0 | 0 |

| prediction | verdict |
|---|---|
| P6: noise-free, λ₀ within the circle's own estimate, 8 of 8 | holds: errors 1.9e-5 to 3.0e-5 against estimates 4.6e-5 to 1.5e-4 |
| P7: with noise, rms error between 0.3 and 3 times the own estimate, at least 6 of 8 | holds, 8 of 8: 0.99 to 1.04 (B), 2.47 to 2.67 (A) |

With the noise of the near points added, the recovered λ₀ is no longer within the circle's own estimate in 80 to 92 percent of the realizations for A and in 35 to 41 percent for B; it moves by an rms of 1.2e-4 to 1.7e-4.

### 3. Exploratory add-ons (not registered with the issue; the add-on predictions are in `predictions_585_addon.json`, raw 3071d1a6, committed before the add-on evaluations)

**The same plant at two other sigmas** (`results_585_sweep.txt`, from `sweep_table_585.py`; no new determinants):

| run | sigma ln, arg | circle | own estimate | noise-free error | rms error | rms movement | rms / estimate | realizations over the estimate |
|---|---|---|---|---|---|---|---|---|
| registered: near points | 3.33e-03, 2.92e-03 | A | 4.60e-05 to 7.06e-05 | 1.92e-05 to 2.96e-05 | 1.20e-04 to 1.75e-04 | 1.19e-04 to 1.72e-04 | 2.47 to 2.67 | 0.80 to 0.92 |
| registered: near points | 3.33e-03, 2.92e-03 | B | 1.46e-04 to 1.48e-04 | 2.98e-05 to 3.00e-05 | 1.45e-04 to 1.51e-04 | 1.44e-04 to 1.49e-04 | 0.99 to 1.04 | 0.35 to 0.41 |
| exploratory: 1e-3 | 1.00e-03, 1.00e-03 | A | 4.60e-05 to 7.06e-05 | 1.92e-05 to 2.96e-05 | 4.21e-05 to 6.27e-05 | 3.80e-05 to 5.47e-05 | 0.88 to 0.95 | 0.29 to 0.33 |
| exploratory: 1e-3 | 1.00e-03, 1.00e-03 | B | 1.46e-04 to 1.48e-04 | 2.98e-05 to 3.00e-05 | 5.28e-05 to 5.57e-05 | 4.61e-05 to 4.75e-05 | 0.36 to 0.38 | 0.00 |
| exploratory: far points | 2.75e-04, 3.27e-04 | A | 4.60e-05 to 7.06e-05 | 1.92e-05 to 2.96e-05 | 2.21e-05 to 3.41e-05 | 1.15e-05 to 1.65e-05 | 0.48 to 0.50 | 0.00 |
| exploratory: far points | 2.75e-04, 3.27e-04 | B | 1.46e-04 to 1.48e-04 | 2.98e-05 to 3.00e-05 | 3.19e-05 to 3.31e-05 | 1.39e-05 to 1.43e-05 | 0.22 to 0.23 | 0.00 |

The rms movement scales with sigma (on B 1.4e-5 for sigma 2.7e-4 and 3.3e-4, 4.7e-5 for 1e-3, 1.5e-4 for 3.3e-3 and 2.9e-3: about 0.047 times sigma). The noise-free errors (2e-5 to 3e-5) are a single draw of the cached determinants' own noise and are the same for the four φ, since the noise perturbs the power sums and not the plant.

**The noise at the circles' own points** (`circle_noise_585.py`, `results_585_circle_noise.txt`; 6 base points of the two circles t = i/20, i = 0, 7, 14, the reference and 15 ulp moves of Re each, 96 evaluations):

| point | re | im | values | std ln\|det\| | std arg | reference equals the circle's cached value |
|---|---|---|---|---|---|---|
| A0 | 1.962797 | 0.916032 | 16 | 8.45e-04 | 6.52e-04 | yes |
| A7 | 1.867530 | 0.964573 | 16 | 7.73e-04 | 7.29e-04 | yes |
| A14 | 1.884256 | 0.858969 | 16 | 1.13e-03 | 8.42e-04 | yes |
| B0 | 2.456619 | 0.547672 | 16 | 1.49e-03 | 1.13e-03 | yes |
| B7 | 2.361352 | 0.596213 | 16 | 1.03e-03 | 1.54e-03 | yes |
| B14 | 2.378078 | 0.490609 | 16 | 1.99e-03 | 1.15e-03 | yes |

sigma_circle, the pooled rms of the std, is 1.28e-3 in ln|det| and 1.05e-3 in arg, between the far points (2.7e-4) and the near points (3.3e-3), as E1 predicted (E1 holds). E2 holds: the mean noise-free error 2.68e-5 is within a factor 3 of 0.045 × sigma_circle = 5.8e-5. The circles' own references equal their cached values bit for bit (the repeat control).

### 4. What this says, and what it does not

- The evaluation of det M is deterministic and exactly conjugate-symmetric (#582), and noise-limited at 1e-4 to 4e-3 in ln|det| and arg under single-ulp moves of the argument. It is larger by a factor of about 12 within 0.02 of a zero than far from one, and 1.3e-3 at the points of an R 0.06 circle around a zero.
- A zero's position from an R 0.06 circle then has a scatter of 4e-5 to 5.5e-5 (rms movement of the planted ensemble at sigma 1e-3, 5e-5 to 7e-5 scaled to sigma_circle 1.3e-3), which is 0.4 to 1.2 of the circle's own estimate in these two circles (0.36 to 0.95 at sigma 1e-3): the estimate has the right size and is not a bound (29 to 33 percent of A's realizations exceed it at sigma 1e-3, none of B's). The position difference of B between this machine, 2.396581 + 0.547584i, and macm3's #507, 2.396619 + 0.547672i, is 9.6e-5, which is the size two independent draws of that scatter give (about 8e-5), but the machines differ in more than rounding (libm `pow`), so this is consistent with the noise and does not show it.
- The windings do not depend on it: the largest step on the real circles is 0.39 rad and the tolerance π/4, against noise of 1e-3.
- Not tested: where the noise comes from (the pivot ratio is 1e20 to 1e22, double-double); the true value at each point (the quad-double code of #584 supplies it, so whether this noise is the double-double LU's or the matrix's is open); circles other than the two at kf 27; sigma at points between 0.02 and 0.054 from a zero.
- Discrepancy with the registered predictions: P3 failed (12.2 against 1 to 10). The near points are 0.02 from a zero and the far points 0.8 to more than 2.5 away, and I did not predict the ratio from data.

**Notes.** Scripts: `noise_585.py`, `analyze_585.py`, `planted_585.py`, `circle_noise_585.py`, `sweep_table_585.py`, `drive_57x.py` (for circle B), with their results `results_585_*.txt`, `sigma_585.json`, `planted_585*.json`, `evals_585.jsonl`, `circle_evals_585.jsonl`, `extra_*.jsonl`. The determinants were computed on Windows (libm `pow` differs from macm3's).
