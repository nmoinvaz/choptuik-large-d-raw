| bar | wanted | result |
|---|---|---|
| sweep exit | 0 (sanity: u0 0.04 at N 408 reproduces the record system's F bit for bit) | **0**, 935 s, peak RSS 176 MiB |
| control `--mutate=steps` exit | 1 | **1**, 18 s |
| \|F\| at u0 0.04, N 408 | 3.188e-10 within 1% | **3.1822e-10** (-0.18%; the record's field F is 3.1834e-10, +0.04% from this) |

**dF_last** (norm of the last block's change against u0 0.04 at the same N), `results_1105.md` has the bands and seconds:

| u0 | N 408 | N 544 | N 816 | N 1088 |
|---|---|---|---|---|
| 0.010 | 7.626e-06 | 6.995e-06 | 6.341e-06 | 1.022e-05 |
| 0.015 | 2.225e-07 | 2.153e-07 | 1.988e-07 | 4.849e-06 |
| 0.020 | 1.725e-08 | 1.698e-08 | 1.616e-08 | 4.985e-06 |
| 0.030 | 4.478e-10 | 4.368e-10 | 6.381e-10 | 4.977e-06 |
| 0.040 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0.000e+00 |
| 0.050 | 1.662e-10 | 1.660e-10 | 2.851e-08 | 4.091e-04 |
| 0.060 | 3.846e-08 | 3.843e-08 | 1.056e-06 | 1.455e-02 |

**|F_last|** (the last block's own residual):

| u0 | N 408 | N 544 | N 816 | N 1088 |
|---|---|---|---|---|
| 0.010 | 7.626e-06 | 6.995e-06 | 6.340e-06 | 7.727e-06 |
| 0.015 | 2.225e-07 | 2.154e-07 | 1.990e-07 | 2.242e-07 |
| 0.020 | 1.723e-08 | 1.695e-08 | 1.633e-08 | 1.778e-08 |
| 0.030 | 4.463e-10 | 4.389e-10 | 4.271e-10 | 1.617e-08 |
| 0.040 | 2.249e-10 | 2.248e-10 | 4.243e-10 | 4.978e-06 |
| 0.050 | 2.734e-10 | 2.734e-10 | 2.854e-08 | 4.101e-04 |
| 0.060 | 3.846e-08 | 3.843e-08 | 1.056e-06 | 1.455e-02 |

**Readings, as measured** (t5's rules, stated before the run; `read_1105.py`, selftest exit 0, `--mutate=ref` exit 1):
- **N:** dF_last at u0 0.02 is 1.725e-8, 1.698e-8, 1.616e-8 and 4.985e-6 at N 408, 544, 816, 1088. The rule read literally (change 816 to 1088 below 20%): **not met** (3.1e4 %). The cause is the reference: the u0 0.04 evaluation at N 1088 has a last-block residual of 4.98e-6 (2.2e-10 at N 408 and 544, 4.2e-10 at N 816), so every dF at N 1088 is that reference. The rule is therefore **not settled** by N 816 to 1088. Read as |F_last| at u0 0.02, a different quantity chosen after the run: 1.633e-8 (816) and 1.778e-8 (1088), +8.9%.
- **Horizon RK:** hz2 (3508 horizon steps) gives dF_last 1.700e-8 against 1.725e-8 (**1.5%**, below 10%): the horizon segment's RK is **not** a cause. The series to order 45 gives 1.724e-8 (0.1%): not the series cut at u0 0.02.
- **Shape in u0:** the points do not follow one power law. On the low side the neighbour slope of dF_last is -8.7 (u0 0.01 to 0.015), -8.9 (0.015 to 0.02) and **-9.0** (0.02 to 0.03) at N 408 (-9.0 at N 544, -8.0 at N 816): dF_last grows as u0 shrinks, about u0^-9; there e(0.04) is negligible against dF (2.2e-10 against 1.7e-8 at 0.02), so the slope is p. On the high side the slope between 0.05 and 0.06 is **+29.9** (N 408, 544; +19.8 at 816, +19.6 at 1088); it is p only if e(0.04) is negligible, and it is not (dF at 0.05 is 1.7e-10 against the reference's 2.2e-10), so +29.9 is consistent with the series cut's 30 and not established as it. Model (b), a single p over the four points, fits badly (rms of ln|dF| 1.98 at N 408 and 544, p = 0.53 and 0.59), so its p is not a reading; at N 1088 the fit is good (rms 0.01, p = 19.7) only because dF is the reference's.
- **Bands:** at u0 0.02 the 0-10 band is the largest at every N (norm 1.64e-8 of the total 1.725e-8 at N 408), with 101+ next (5.4e-9). At u0 0.06 and N 408, 544 the 101+ band holds it (3.8e-8); at N 816, 1088 the 0-10 band does.

| N | u0 | 0-10 | 11-50 | 51-100 | 101+ |
|---|---|---|---|---|---|
| 408 | 0.02 | 1.64e-08 | 2.74e-10 | 1.75e-10 | 5.41e-09 |
| 408 | 0.06 | 3.30e-11 | 2.70e-13 | 3.09e-12 | 3.85e-08 |
| 816 | 0.02 | 1.52e-08 | 3.81e-10 | 1.52e-10 | 5.41e-09 |
| 816 | 0.06 | 9.93e-07 | 3.51e-07 | 6.60e-08 | 3.96e-08 |

**What disagrees or stands out (reported, not reconciled):**
- #1105's body quotes dF_last at u0 0.02 of 2.0e-8, 1.6e-8 and 1.4e-8 at N 408, 544, 816 (#1103). Here, at the same state and settings, it is 1.725e-8, 1.698e-8 and 1.616e-8: 14% lower at N 408 and falling 6% from 408 to 816, not 30%. The last block's whole |F_last| (all five fields) is 1.723e-8 at N 408, so the p-field alone cannot be 2.0e-8 against this run's. #1103's hz2 (2.0e-8 to 1.75e-8, 12%) differs from this run's 1.5% too.
- For u0 at or above 0.04 the last block's residual grows with N: at u0 0.05, 2.7e-10 (N 408, 544), 2.9e-8 (816), 4.1e-4 (1088); at 0.06, 3.8e-8, 3.8e-8, 1.1e-6, 1.5e-2. The u0 0.04 reference follows (2.2e-10, 2.2e-10, 4.2e-10, 5.0e-6). The record's N is 408.
- At N 408 the last block's own residual has its minimum between u0 0.03 and 0.05 (4.5e-10, 2.2e-10, 2.7e-10 at 0.03, 0.04, 0.05), so the record's u0 0.04 sits near the bottom of a V: dF_last about u0^-9 on the low side, rising again above 0.05 (slope +29.9 at N 408, with the caveat above).
