# I240-macm3: D 54.04 counted at M 48, kf 23, inside the onset bracket (53.79, 55.04]

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3-314 (Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx for 3.14),
main 25b50d1d. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/240. Beside I231-macm3's two M 40 counts.

Commands (gamma.cmd, count.cmd, caffeinate -is, nice 10, one thread): python3 hp/gamma_dd.py <raw>/I240-macm3/gamma.jsonl hp/data/states/up10_D54.0414.npz (lam_phys is not in hp/data/gamma_dd.jsonl, its default layout is
the kf 13 cut from D 35 on), then python3 hp/modecount_wind.py hp/data/states/up10_D54.0414.npz --M=48 --kf=23 --h0=0.6 --lam=<lam of the record> --fmax=1e-15 --resolve=last --tag=D54.0414_M48_kf23 --data=<raw>/I240-macm3/data.
The state is M 32 native, so setup resamples to M 48 and re-converges (as I232, I237). No D 54.04 kf 23 state or cache is in hp/data or --data (hp_data_before.txt).

Written before the run. Gate: gamma_dd's own residual gate (--fmax 1e-20; a skip is reported and the count is not run), then setup |F| <= 1e-15 (a miss is a stop, reported). Table: the 8 boxes with both mismatch counts per edge,
beside D 53.79 (all 0) and D 55.04 (B0 +2, U0 +1, U +1, full +2). Reading rule, fixed now: extras "present" when wind(g) is nonzero in any resolved box, "absent" when 0 in all; absent narrows the onset bracket to
(54.04, 55.04], present to (53.79, 54.04]; the boxes where they appear say whether they enter through the left column (B0, U0) as D 55's do. An unresolved edge is "not a count" and its boxes are not read.

gamma_dd on D 54.041398 (gamma.jsonl, exit 0): not skipped, |F| 4.3e-24 in its kf 13 layout, lam_phys = 2.048451702933493 (gamma 0.4881735793760459, formula lam 2.048452025831, one sign change). The count uses it (count.cmd).

Results (macm3, main 25b50d1d, venv-macm3-314 = Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0; awake.log: awake = wall; gamma_dd 35 s, the count 4492 s = 75 min, exit 0 at 10:27:34 UTC, side by side with I231's two M 40 runs for the first minute only).
  Setup: |F| 7.9e-08 in the layout, 7.9e-08 after Newton, 1.1e-19 after Levenberg-Marquardt (gate 1e-15 passed; state moved to hp_data_after/). 160 evaluations (156 distinct points, four corners twice, equal to 2.5e-05 rad), 25.9 s each.
  wind(g) is NOT 0: B0 +2, U0 +2 (B1a, B1b, B1c, B1, U, full 0). Winding of det M: B0 3, U0 2, B1a 1, B1b 1, B1c 0, B1 2, U -7, full -12. All 14 edges resolve: mismatches 0 in any pass and 0 in the last pass, largest step 0.389 rad,
  at most 3 passes. Real axis: only the two expected sign changes. The extras are PRESENT at D 54.04, in the left column (B0, U0), as at D 55.04 (B0 +2, U0 +1, U +1).
  Onset bracket (rule above): present, so the onset lies in (53.79, 54.04]; narrowed from (53.79, 55.04].
  Caveat on comparing boxes across D: the contour's Re edges move with D (the box B0 spans Re -0.150 to 0.124 here, -0.096 to 0.300 at D 55.04, -0.150 to 0.300 at D 53.79), so B0 and U0 are not the same region at every D.
