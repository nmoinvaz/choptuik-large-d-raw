# I571-macm3: #498's R 0.01 test at kf 29 with a double-double ulp of dh[10,11] (shift 0 and +1, part lo; D 61.03, M 48)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0). Kernel: the new modecount_cx built in the worktree ~/Source/choptuik-large-d-b80 at ecca9c53 on 2026-11-12 06:00 UTC (bit check against #473's cached determinants passed: I517-macm3/bitcheck_473.log) with the Python hpkernel of 2026-11-09; the worktree is at 7e9d5a7 (hp/modecount_ulp_circle.py, whose --selftest printed pass). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/571 (recommended by macm3 in #552's closing summary; commands: the coordinator's message of 2026-11-12 06:28 UTC).

Runs (run_571.sh NAME SHIFT, from the worktree's hp/, one thread each, nice 10, caffeinate -is, an empty data dir of its own): python3 modecount_ulp_circle.py 10 11 SHIFT lo -- data/seeds/local/up23_D61.0264.npz 3.1023,-0.0068,0.01 --M=48 --kf=29 --n0=20 --fmax=1e-15 --data=<raw>/I571-macm3/NAME --res=<raw>/I571-macm3/NAME/circles.jsonl, with NAME shift0 (SHIFT 0) and lo_p1 (SHIFT +1). The kf 29 state is the saved hp/data/modecount_state_D61.0264_M48_kf29.npz (sha256 bfe7150859d4b92c...), copied into the worktree. The cap of the issue, 150 points on the circle: the cache holds those plus 2 beta points, so run_571.sh stops a run whose cache has more than 152 lines and records "cap=yes" in exits.txt.

Written before the run (the issue's). |Delta arg| above 0.5 rad at some matched point, or windings that differ: the phase is rounding noise. All matched points within 0.01 rad and equal windings: not. Anything between is reported with the numbers. The shift-0 run must reproduce the plain module's determinants bit for bit at the points both evaluate (the plain module: I498-macm3/ulp29/plain, the old modecount_cx of 2026-11-06 with the same wrapper at shift 0).

## Results


(2026-11-12 07:49 UTC, macm3) Both runs were stopped by me at the coordinator's instruction (message of 07:48 UTC: the criterion fires on any matched point above 0.5 rad, so more points cannot change the verdict): lo_p1 at 07:48:41 UTC and shift0 at 07:48:51 UTC (exit 143, cap=no in exits.txt); started 06:40:06 UTC (shift0) and 07:22:39 UTC (lo_p1). Neither circle had closed: shift0 held 79 determinants (77 on the circle), lo_p1 30 (28 on the circle); the steps of the arg above pi/4: 22 and 7; the sums of the wrapped steps are +1 turn in both, which is not a result for an open circle, so there are no windings to compare.

shift 0: 79 determinants; lo +1: 30; matched (same lambda to the last bit): 30; |Δarg| above 0.5 rad at 5, above 0.01 rad at 26, largest 2.528 rad, smallest 0.0003 rad

| angle on the circle | \|λ − c\| | arg shift 0 | arg lo +1 | \|Δarg\| | ln\|det\| shift 0 | ln\|det\| lo +1 |
|---|---|---|---|---|---|---|
| -162.0° | 0.01 | +1.037 | +1.205 | 0.168 | -131.905 | -132.124 |
| -144.0° | 0.01 | +0.955 | +0.993 | 0.038 | -131.249 | -131.319 |
| -126.0° | 0.01 | +1.529 | +1.235 | 0.294 | -131.276 | -131.137 |
| -108.0° | 0.01 | +1.557 | +2.055 | 0.498 | -131.006 | -131.130 |
| -90.0° | 0.01 | +2.324 | +2.151 | 0.172 | -130.966 | -130.922 |
| -72.0° | 0.01 | +2.534 | +2.330 | 0.205 | -130.835 | -130.869 |
| -54.0° | 0.01 | +3.007 | +2.855 | 0.152 | -130.849 | -130.895 |
| -36.0° | 0.01 | -2.889 | -2.954 | 0.065 | -130.851 | -130.898 |
| -18.0° | 0.01 | -2.365 | -2.027 | 0.339 | -131.156 | -130.830 |
| 0.0° | 0.01 | -1.858 | -1.102 | 0.756 | -131.725 | -130.651 |
| 9.0° | 0.01 | -1.275 | -1.393 | 0.117 | -131.264 | -131.317 |
| 18.0° | 0.01 | -0.807 | -0.790 | 0.018 | -131.149 | -131.070 |
| 27.0° | 0.01 | -0.620 | -0.643 | 0.023 | -131.974 | -131.898 |
| 36.0° | 0.01 | -0.302 | -0.236 | 0.066 | -132.165 | -131.684 |
| 45.0° | 0.01 | +0.073 | +0.076 | 0.003 | -132.328 | -132.090 |
| 54.0° | 0.01 | +0.283 | +0.273 | 0.010 | -131.572 | -132.322 |
| 63.0° | 0.01 | +0.509 | +0.649 | 0.139 | -132.602 | -132.833 |
| 72.0° | 0.01 | +0.665 | +1.879 | 1.214 | -132.812 | -133.182 |
| 81.0° | 0.01 | +0.054 | +0.160 | 0.105 | -133.196 | -133.216 |
| 90.0° | 0.01 | +0.102 | +2.630 | 2.528 | -132.850 | -134.684 |
| 99.0° | 0.01 | -1.274 | -0.374 | 0.899 | -133.973 | -132.966 |
| 108.0° | 0.01 | -2.225 | -0.759 | 1.466 | -133.908 | -133.069 |
| 117.0° | 0.01 | -0.143 | -0.190 | 0.046 | -132.074 | -132.093 |
| 126.0° | 0.01 | -0.156 | -0.195 | 0.038 | -132.359 | -132.865 |
| 135.0° | 0.01 | -0.040 | -0.039 | 0.001 | -132.670 | -132.371 |
| 144.0° | 0.01 | +0.108 | +0.106 | 0.002 | -132.629 | -132.089 |
| 162.0° | 0.01 | +0.338 | +0.424 | 0.087 | -131.923 | -132.436 |
| 180.0° | 0.01 | +0.691 | +0.575 | 0.116 | -131.889 | -131.773 |
| 0.0° (beta point) | 0.02 | -1.016 | -1.016 | 0.000 | -129.514 | -129.437 |
| 180.0° (beta point) | 0.02 | +0.234 | +0.358 | 0.123 | -131.328 | -131.620 |


Wrapper control (the issue's last criterion): shift 0 and #498's plain run (I498-macm3/ulp29/plain, the old modecount_cx of 2026-11-06 with the high-part wrapper at shift 0) evaluate 44 common determinants, and all 44 are equal bit for bit in ln|det|, arg, pmin and pmax. Verdict by the criterion (|Delta arg| above 0.5 rad at some matched point): rounding noise at double-double; provisional until the quiet-side control of the 0.5 rad rule (I569-macm3) passes.
