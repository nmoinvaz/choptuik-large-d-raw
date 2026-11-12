# I529-win2: order-2 assumptions at the D 242.5 starts, sigma_5 against sigma_4 and Q at small h

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/529 (parts (a) and the Q half of (c); (b) and the mixed block need code and follow).
Code: worktree `D:\choptuik-i529` at main 810396b (`hp/dz0_weak.py`), Python only, venv-t126. Inputs from the raw clone at 52c091a5 (copied to the same paths here): BASE = `I461-win2/probeG03125a/anm_pin3_D242.5146.npz`, ACC = `I461-win2/probeG0078/dz0_pin3_D242.5225_a0.007812.npz` (accepted attempt), REF = `I461-win2/probeG03125b/dz0_pin3_D242.5459_a0.031250.npz` (refused attempt).
Four jobs of 2 threads (`run_i529.sh`): `dz0_weak.py RAW <attempt> BASE --k=5 --its=16` and `--k=5 --its=24 --reduced=1 --h=1e-31`, for ACC and REF, then the control `--mutate=D` on REF's reduced job (its rebuild check must FAIL, exit 1). Exit codes in `exits.txt`. Results follow in this README.

## Results (2026-11-12 05:19:40 to 05:29:52 UTC)

Four jobs of 2 threads at once (`run_i529.sh`), the control, and two supplementary jobs at h = 1e-32 (`run_i529_h32.sh`); `exits.txt` has every start and exit. No Traceback, every exit as expected. The jobs ran in 3.9 to 4.6 minutes each (the octo-double LU 98 to 108 s, the rebuild check 104 to 111 s, the reduced block 38 to 41 s).

**(a) sigma_1..5 and the gap** (job 2, the reduced job, `--its=24`; the iteration of job 1, `--its=16`, in brackets for sigma_5):

| attempt | D, a | sigma_1 | sigma_2 | sigma_3 | sigma_4 | sigma_5 (its 24; its 16) | gap sigma_5 / sigma_4 | sigma_5's convergence, relative to its 24 value; to its 16 value |
|---|---|---|---|---|---|---|---|---|
| ACC (accepted) | 242.522462, 0.0078125 | 2.1841e-27 | 2.1898e-27 | 3.3268e-26 | 7.1880e-26 | 1.2327e-19 (2.2688e-19) | 1.715e+06 | 0.84; 0.46 |
| REF (refused) | 242.545900, 0.03125 | 2.1352e-27 | 2.1425e-27 | 3.1943e-26 | 7.0800e-26 | 8.4794e-20 (2.6295e-19) | 1.198e+06 | 2.10; 0.68 |

sigma_1 to sigma_4 are the same in both iteration counts to the digits that matter (sigma_1 and sigma_2, a nearly degenerate pair, differ by 0.2% between 16 and 24 iterations: 2.1882e-27, 2.1856e-27 against 2.1841e-27, 2.1898e-27 for ACC); **sigma_5 has not converged**: it fell by a factor 1.8 (ACC) and 3.1 (REF) between 16 and 24 iterations and is still falling, so the gap sigma_5 / sigma_4 of 1.7e6 and 1.2e6 is the value at 24 iterations and I cannot say what it converges to. What the runs show is that sigma_5 is more than 6 orders above sigma_4 at 24 iterations in both attempts.

**(c) Q at small h** (`dz0_weak.py --reduced=1`; the block prints Q's largest entry at h and the largest difference of Q at h and at h/10, relative to it). The h = 1e-32 jobs give Q's largest entry at 1e-32:

| attempt | max abs Q at h = 1e-31 | max abs Q at h = 1e-32 | Q(1e-31) against Q(1e-32), relative | Q(1e-32) against Q(1e-33), relative | truncation c h^2 at 1e-31, 1e-32 | dz0_weak's line |
|---|---|---|---|---|---|---|
| ACC | 5.4e+04 | 5.4e+04 | 1.3e-06 | 1.3e-08 | 6.3e-02, 6.3e-04 | reduced system: ... Q at h against h/10 1.3e-6 (bound 1e-2): pass; check: pass |
| REF | 2.75e+04 | 2.75e+04 | 2.3e-06 | 2.3e-08 | 6.3e-02, 6.3e-04 | reduced system: ... Q at h against h/10 2.3e-6 (bound 1e-2): pass; check: pass |

By the issue's rule (Q(h) and Q(h/10) agree to 1e-2, or c h^2 stays below 1e3): **both clauses are met** at both attempts. Q's size against 1e3: its largest entry is 5.4e+04 (ACC) and 2.75e+04 (REF), above 1e3 by factors 54 and 27.5 (the 1e3 bound is on the truncation constant, not on Q). The relative differences fall by 100 for each factor 10 of h (1.3e-6 -> 1.3e-8), as a second-order truncation does, and dz0_weak's own check line is pass in both, not the FAIL that a truncation difference alone would give. The reduced system's other numbers: |B a| = 7.95e-37 (ACC) and 1.36e-36 (REF), the root scale sqrt(|B a| / |Q|) 3.84e-21 and 7.02e-21; roots of g(c) = B (c - a) + 1/2 Q(c, c) from 25 starts: 6 (ACC) and 5 (REF) real ones at h = 1e-31 (4 and 5 at 1e-32), the nearest to c = 0 with |c| 1.26e-29 (ACC) and 8.32e-30 (REF), equal to the attempt's own dz0 coefficients on the refined basis, the others at |c| 3e-24 to 9e-22 (ACC) and 3e-24 to 3e-22 (REF), the smallest |g| reached 2.6e-49 and 1.6e-47 of |B a|.

**The share on span(V) and the rebuild check** (job 2, its 24; job 1 gives the same to the digits shown):

| attempt | \|dz0\| 2-norm | on span(V) | the rest | rebuild check (J (dz0 - dz_bare) on the held rows, elsewhere; bound 1e-6 of the first) |
|---|---|---|---|---|
| ACC | 1.265e-29 | 1.265e-29 (share 1.0) | 1.124e-32 (share 0.000889) | 0.000816, elsewhere 2.03e-99: pass |
| REF | 8.325e-30 | 8.325e-30 (share 1.0) | 6.624e-33 (share 0.000796) | 0.000816, elsewhere 2.01e-99: pass |

**Control:** `--mutate=D` (the kernel rebuilt at D + 1e-6) on REF's reduced job exited 1: the rebuild check reads 1.08e+59 on the held rows and 5.97e+57 elsewhere, **FAIL**, as it must (`ref_k5_red_ctl_D.log`; with the wrong D the share on span(V) falls to 0.683).

**Supplement: sigma_5 against the number of iterations** (`run_i529_its.sh`, `--k=5 --its=N`, no reduced block, 05:31 to 05:37 UTC; the same four rows of `exits.txt`):

| attempt | its 16 | its 24 | its 64 | its 256 | sigma_5 / sigma_4 at its 16, 24, 64, 256 |
|---|---|---|---|---|---|
| ACC | 2.2688e-19 | 1.2327e-19 | 1.7235e-19 | 7.1199e-19 | 3.16e+06, 1.71e+06, 2.40e+06, 9.91e+06 |
| REF | 2.6295e-19 | 8.4794e-20 | 1.2611e-19 | 8.5614e-20 | 3.71e+06, 1.20e+06, 1.78e+06, 1.21e+06 |

The estimate of sigma_5 does not converge: it falls from 16 to 24 iterations, rises again at 64, and at 256 iterations is 7.1e-19 for ACC (the largest of the four) and 8.6e-20 for REF (near its minimum). It wanders between 1.2e-19 and 7.1e-19 (ACC) and 8.5e-20 and 2.6e-19 (REF), so the fifth direction is not one well-determined number in these runs (a cluster of nearby singular values near 1e-19 would give this); sigma_1 to sigma_4 are stable (sigma_3 and sigma_4 identical to the five digits at every iteration count; sigma_1 and sigma_2, the near-degenerate pair, drift together from 2.1882e-27, 2.1856e-27 at 16 to 2.1703e-27, 2.2041e-27 at 256 for ACC). What every estimate says is that the fifth direction lies at least 1.2e6 times above sigma_4; I cannot give its gap more closely.
