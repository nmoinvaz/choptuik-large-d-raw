# diag: what the first planted truth P showed (not frozen, not a check)

Exploratory runs on control plants only, after the first P fired (2026-11-18 00:25-00:34 UTC, rpi5, `nice -n 10`, the
scripts here, against `solver/inner_amp/pade_far_poles.py` at 10b90d9b). The outputs below are transcribed from the
terminal. Each script inserts the absolute path of the `wip/i747` worktree's `solver/inner_amp` into `sys.path`, to be
edited to run elsewhere.

`diag_P.py` (chord2, ω∞): three pure point masses with no main are found exactly (d_8, d_9, d_10 = 0). With the main and
equal masses, d_8, d_9, d_10 at η_P = 1, 3, 10, 30, 100, 1e3, 1e4, 1e6 are 0.127, 0.077, 0.022 / 0.113, 0.076, 0.022 /
0.102, 0.079, 0.021 / 0.348, 0.193, 0.026 / 0.472, 0.264, 0.026 / 0.766, 0.449, 0.026 / 0.642, 0.711, 0.026 / 1.079,
0.977, 0.026, with fit_resid 3.4e-4, 1.0e-3, 3.5e-3, 2.1e-4 (M 8), 7.2e-4, 7.2e-3, 7.2e-2, 13. One mass alone, the
distance of the nearest [8/8], [9/9], [10/10] pole to it: at REF541[8] 0.145, 0.145, 0.083 for η = 0.01 and 0.054, 0.032,
0.022 for η = 1; at REF541[9] 0.200, 0.089, 0.049 and 0.058, 0.035, 0.023; at REF541[10] 0.190, 0.074, 0.038 and 0.062,
0.037, 0.022.

`diag_P2.py` (chord2): the three weights' ratios solved by Levenberg-Marquardt over the three nodes at η = 1, φ = 0 from
equal weights at scales 1, 10, 100 reach a largest |pole − REF541| of 0.0313 each time, the same plant (share of σ₂₂
0.659, of σ₁₂ 0.060, fit_resid 4.1e-4); the three starts took 8.8 min.

`diag_P3.py` (chord2): the same with η and φ free, solved at ω∞ only: it stalls at 0.086 (η = 28, φ = 342°, share of σ₁₂
1.7), and at the other nodes d_8, d_9, d_10 are 0.365, 0.186, 0.031 (ω 0.99) and 0.081, 0.075, 0.020 (1.01).
