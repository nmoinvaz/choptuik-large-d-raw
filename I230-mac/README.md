# I230-mac: positions of the extra zeros of det M at D 61.03, M 48 (kf 21 and kf 23), and small circles around them

Machine: mac (Apple M5, 10 cores, macOS 27, shared with #208's two CAPD processes), venv-314 (Python 3.14.7 by uv,
hpkernel and multidouble NEON, python-flint 0.9.0, modecount_cx cp314 build of 2026-11-08 16:26 from the main
checkout). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/230. Code: branch wip/i230 of the main
repository (hp/modecount_moment.py, hp/modecount_moment_planted.py, hp/modecount_circle.py,
hp/modecount_circle_planted.py). Inputs, read from the raw-data repository at 6e2e394 (git archive into a scratch
directory, nothing pulled here): I212-macm3/data (kf 23 count, 776 determinants), I212-macm3/reeval159/data (#159's
kf 21 count re-evaluated, 707 determinants), the saved states I212-macm3/hp_data_after/ (kf 23) and
I159-macm3/hp_data_after_kf21/ (kf 21, byte-identical to reeval159's copy), copied into the worktree's hp/data for the
circles and not committed. All runs single-threaded under nice 10, at most two at a time. From 10:30 UTC they ran
under caffeinate -i: the Mac went into maintenance sleep at 09:55 UTC and stalled them, and nothing was lost.
351 new determinants: 347 in data/ and 4 in the two checks.

## Files

- planted/: the planted tests' logs, each named by the commit it ran at, each with its controls. The moment test:
  v1 and v2 failed, v3 passed, v4 failed in B0, v5 (B0 printed, not tested) passed. The circle test: v1 passed, v2
  failed at n0 = 16 in one case, v3 (n0 = 20, the real circles' setting) passed. The reasons are in the tests'
  docstrings (History).
- moments.jsonl, moments_kf23.log, moments_kf21.log: hp/modecount_moment.py on the two caches, B1b and B1c (no new
  determinant).
- repro_check.py, .log, .jsonl: two of #212's determinants recomputed here. Its criterion of 1e-8, fixed before the
  run, failed: 1.3e-8 in ln|det M| at lam 3, and 2.6e-9 at a point of V2 (arg 8.6e-10).
- noise_check.py, .log, .jsonl: lam 3 through hpkernel's LU (Solver.mode_det) against the crate's. They are 1.5e-5
  apart, so the cross-machine difference is within this machine's own rounding noise of the determinant. The run's
  log line "hpkernel 1.000000000000" is the sign. The first version read the wrong element of the returned tuple. The
  tuple it printed holds ln|det| 273.2516217710863, against the crate's 273.251606743652. The script is corrected.
- data/: the circles' determinants (modecount_<tag>_evals.jsonl), logs (modecount_<tag>.log) and records
  (circles_kf23_A, _B, circles_kf21_C, _D, _E .jsonl). Also t_check.jsonl and the T stretch's determinants
  (modecount_D61.0264_M48_kf23_T_evals.jsonl). Run D was stopped after its first circle; its second circle ran as E.
- circles_*.log: the circle runs' output (exit codes on the last line).
- t_check.py, t_check.log: the stretch of #212's kf 23 edge T (Im = 3 omega / 2, Re 1.157 to 0.300) that the count
  left at the initial spacing, re-sampled with the count's rules.
- alias_scan.py, alias_scan.log: every interval of every edge of both counts' records, its step against its
  neighbours' rates. A flag is a reason to re-sample, not a proof. Its control, the two T intervals at kf 23, is
  flagged. The one other flag (kf 21, V2 from Im 0 to 0.29) lies next to zero 3, 0.046 from V2, with smooth ln|g|.

## Results

Circles: n0 20, R 0.2, tol pi/4, 0 verification mismatches in every one. The estimate is the distance to the
n0/2-point value; it was conservative in the planted test.

| cut | circle centre | winding of det M | points | max step | zero(s) inside | estimate |
|---|---|---|---|---|---|---|
| kf 23 | lam_phys 2.043532530673195 (control) | +1 | 28 + 2 | 0.376 | 2.0435328121 - 1.4e-7 i | 5.5e-7 |
| kf 23 | 1.30641 + 1.41644i | +1 | 27 + 2 | 0.389 | 1.3064778 + 1.4157830i | 9.3e-7 |
| kf 23 | 2.00728 + 0.97347i | +1 | 29 + 2 | 0.363 | 2.0072792 + 0.9727203i | 4.9e-7 |
| kf 23 | 2.55894 + 0.58224i | +1 | 29 + 2 | 0.368 | 2.5583853 + 0.5824738i | 5.0e-7 |
| kf 23 | 3.01943 (real axis) | +2 | 42 + 2 | 0.401 | 3.0195705 +- 0.0958190i | 7e-6 |
| kf 21 | lam_phys (control) | +1 | 28 + 2 | 0.382 | 2.0435324951 + 1.9e-8 i | 1.2e-7 |
| kf 21 | 1.34903 + 1.43084i | +1 | 28 + 2 | 0.373 | 1.3559634 + 1.4385362i | 1.0e-6 |
| kf 21 | 2.09255 + 1.01680i | +1 | 28 + 2 | 0.368 | 2.0868804 + 0.9897338i | 2.3e-7 |
| kf 21 | 2.69136 + 0.45650i | +1 | 28 + 2 | 0.370 | 2.6897138 + 0.4760982i | 6.2e-8 |

Shifts from kf 21 to kf 23 (circle positions): zero 1 0.0545, zero 2 0.0814, zero 3 0.1690 (from B1c into B1b
across Re = a2). Zero 4 is new at kf 23. lam_phys shifts by 3.2e-7, within the estimates.

Moment positions against the circles: at kf 23 within 6e-4 to 1.9e-3, at kf 21 within 1.0e-2 to 2.8e-2. At kf 21
the spread was below the error for zeros 2 and 3, by up to 2.2 times; every error is below the planted test's 0.05.

T stretch at kf 23: the phase change of g is +19.119 rad, where the count's two steps gave +0.270, so 3.0000 turns
were hidden. U wind(g) goes from +8 to +11 and full from +24 to +30. B1b, B1c and B1 are unchanged, since they do
not use T.
