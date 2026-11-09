# I232-macm3: the D scan at M 48, kf 23 for the onset of the D 61 extra zeros (D 50.01 and D 55.04)

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3-314 (Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx for 3.14),
main d28566c0. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/232 (its body says I230-macm3 by mistake, the coordinator's correction: I232). Two counts at once, one thread each, beside #220's short run.

Commands (D50/count.cmd and D55/count.cmd, caffeinate -is, nice 10, from the repository root): python3 hp/modecount_wind.py hp/data/states/up8_D50.0075.npz --M=48 --kf=23 --h0=0.6 --lam=2.051843756433441
--fmax=1e-15 --resolve=last --tag=D50.0075_M48_kf23 --data=<raw>/I232-macm3/D50/data, and hp/data/states/up10_D55.0351.npz with --lam=2.04768412771239, tag D55.0351_M48_kf23, --data=<raw>/I232-macm3/D55/data.
No D 50 or D 55 M 48 kf 23 state is in hp/data and both --data folders are empty at the start (hp_data_before.txt), so setup resamples/re-converges and every determinant is fresh.

Written before the run. Table: the 8 boxes at each D beside #211 (D 45: all 0) and #212 (D 61: B1b +6, B1c +2, B1 +8, U +8, full +24, I212-macm3). Gate: each setup's |F| <= 1e-15 (setup raises above --fmax: a stop for that D,
|F| reported, the state it saves moved out of hp/data). Both mismatch counts per edge (all passes and the last pass). Onset reading, fixed now: the extras are "absent" at a D when wind(g) is 0 in every resolved box,
"present" when any box is nonzero; the outcomes are absent at both, present at both, or present at D 55 only (the issue's list); anything else (present at D 50 only) is reported as it is. An unresolved edge is "not a count"
and its boxes are not read. A zero with Re lambda > 0 beyond the expected ones would be an extra growth rate: this task counts, it does not locate.

D 50.01 result (macm3, main d28566c0, venv-macm3-314; D50/count.log, exit 0 at 07:18:28 UTC, 3018 s from 06:28:10, ran beside D 55's count and #220's 16 s run, awake): setup |F| 2.1e-08 in the layout, 2.1e-08 after Newton,
  2.3e-19 after Levenberg-Marquardt (gate passed; state moved to D50/hp_data_after/). 85 evaluations. wind(g) is 0 in all 8 boxes (winding of det M B0 1, U0 0, B1a 1, B1b 1, B1c 0, B1 2, U -7, full -12).
  All 14 edges resolve: mismatches 0 in any pass and 0 in the last pass, largest step 0.377 rad, at most 2 passes. Real axis: sign changes only in (0.5, 1.0) and (2.0, 2.5). So the extras are absent at D 50.

D 55.04 result (D55/count.log, exit 0 at 07:59:23 UTC, 5473 s from 06:28:10; awake.log: awake = wall for both counts): setup |F| 1.1e-07 in the layout, 1.1e-07 after Newton, 1.6e-19 after Levenberg-Marquardt (gate passed; state moved to
  D55/hp_data_after/). 177 evaluations (173 distinct points, four corners twice, equal to 4.2e-05 rad), 30 s each, pivot minima 4.5e-15 to 4.2e-09. All 14 edges resolve: mismatches 0 in any pass and 0 in the last pass, largest
  step 0.392 rad, at most 4 passes. wind(g) is NOT 0: B0 +2, U0 +1, U +1, full +2 (B1a, B1b, B1c, B1 0). Winding of det M: B0 3, U0 1, B1a 1, B1b 1, B1c 0, B1 2, U -6, full -10. Real axis: only the two expected sign changes.
  The extras sit elsewhere than at D 61: B0 and U0 are the left column Re (-0.096, 0.300) (B0 holds the expected zero at 0, it winds 3 = 1 + 2), the strips U (+1, with the mirror +1 inside the full box's +2) and none in B1.
  The full box here starts at Re = 0.300, so it does not contain B0 and U0 (and their mirror strips are not counted).
Onset (reading rule above): absent at D 45 (#211) and D 50.01, present at D 55.04 and D 61.03 (#212): the third outcome of the issue, present at D 55 only among the two new D. compare_boxes.txt has the four D side by side.
