# I168-macm3: the D 61 mode count at M 32 with the cut raised to kf 21

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint 0.9.0, FLINT 3.6.0,
hpkernel 0.1.0 neon), main e04d6f17. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/168

From the repository root with the venv's bin first on PATH, 1 thread, nice 10, caffeinate -is: python3 hp/modecount_wind.py
hp/data/seeds/local/up23_D61.0264.npz --M=32 --kf=21 --h0=0.6 --lam=2.043532530673195 --fmax=1e-15 --tag=D61.0264_M32_kf21
--data=<raw>/I168-macm3/data (empty, so every determinant is fresh).

Written before the run. The question is wind(g) in the 8 boxes (B0, U0, B1a, B1b, B1c, B1, U, full), not a stop. Reading, fixed now:
  wind(g) = 0 in every resolved box: the six zeros of #159 come with M 48 (not with the un-pinned harmonics alone).
  wind(g) = +4 in B1b, +2 in B1c, +6 in B1 (the #159 values): they follow the un-pinned harmonics 15 to 21.
  anything else (a different nonzero count) is reported as a third outcome, with the boxes.
An edge that does not resolve is "not a count" and its boxes are not read. Each box is set against #160 (kf 13, M 32: all 0) and #159 (kf 21, M 48).
Setup: if |F| of the seed in the kf 21 layout is above --fmax, setup re-converges and saves a state into hp/data (kf 21 name); it is moved here, hp/data restored.

Results (macm3, main e04d6f17). Awake time equals wall time (awake.log: no sleep since 2026-11-07 22:39 PST).
  count.log: 86 determinants (82 distinct points, four corners are evaluated twice), 8.9 s each, 766 s (15:13:38 to 15:26:24 UTC). Setup: the M 32 seed has
  |F| 3.8e-23 in the kf 21 layout, so no re-converge and no state saved. Exit status not captured (exits.txt). hp/data unchanged (hp_data_before.txt matches).
  wind(g) is 0 in all 8 boxes (printed -0.000006 to +0.000038, the residual of the phase sum): winding of det M B0 1, U0 0, B1a 1, B1b 1, B1c 0, B1 2, U -7, full -12,
  equal to #160's kf 13 count at M 32 in every box. Max phase step 0.384 rad, every edge verified with 0 mismatches. All edges resolve, so U and full are counts.
  #159 (M 48 kf 21): wind(g) +4 B1b, +2 B1c, +6 B1, 0 elsewhere (U +9 and full +24 are not counts, their edge Im = y2 is unresolved). So the extra zeros are not
  reproduced at M 32: this is the first reading of the README, "they come with M 48".
  compare_boxes.txt: the boxes of the three counts side by side, and the 82 shared points of kf 21 and kf 13 at M 32 (the two determinants are different functions:
  ln|det| differs by 404 to 478 and arg by a median 0.33 rad, so only the windings are compared). compare_repeats.txt: the corner points evaluated twice differ by
  up to 1.2e-4 rad (kf 21 M 32), 9e-6 (kf 21 M 48) and 1e-8 (kf 13 M 32), and the pivot minima are 3.0e-16..1.0e-10 (kf 21 M 32), 6.0e-15..2.0e-10 (kf 21 M 48),
  2.1e-14..8.6e-9 (kf 13 M 32): the evaluation is noisier at kf 21 M 32 than in the other two, 2.6 to 3.5 orders below the largest step of each edge (0.05 to 0.38 rad), so no winding moves; the 2e-5 to 4e-5 winding residuals are the same size, consistent with it (not separately tested).
