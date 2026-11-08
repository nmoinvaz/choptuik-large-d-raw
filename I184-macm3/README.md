# I184-macm3: lemma 6a(5) rerun with the parameter box centred at the certificate's p^

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (Python 3.13.3, python-flint 0.9.0, FLINT 3.6.0, numpy 2.5.4, scipy 1.18.1, versions.txt),
main 9286b05b (review_39/ present). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/184. Box file: I103-macm3/A_M2_6a_M5_sub1e-18.json (its "p" is p^, it has no "x" key).

`run_i184.sh` (from solver/proof/, 1 thread, nice 10, caffeinate -is) runs #103's commands with --x=$PHAT, PHAT the six decimal strings of the box file's "p" (phat.txt, read by python json):
the run (--save-B, --json), then partial and coords with --load-B=<the new B> and --x=$PHAT, then swap (a full run), then review_39/b_float.py on the new B and with --mutate=w.
Each exit and wall time is in exits.txt, each command in cmd_*.txt.

Written before the run. Pass criteria (any miss is reported, not fixed):
  1. The main run exits 0 with rho_6a < 1 printed.
  2. The centre used equals p^. lemma6_jump_M.py prints no centre line (it sets FPM.ZEROS[M] from --x and takes xs from it, since the box file has no "x"). So the log carries a header line
     written by the shell before the run (centre_passed.txt, the --x argument verbatim, equal to the box file's "p" to every digit, checked by diff), and the effect of the centre is read off B:
     the new B's midpoints must differ from I103's (the old centre), by about 0.178 of B's radius as #39's float flow predicts.
  3. b_float.py on the new B: the "phat" line's max |B_float - mid(B)| / rad(B) below 0.01 (the old B gives 0.178), and its exit 0 (worst of the two lines below 1).
  4. Controls as in #103: partial exits 0 with "G_slow is 13 x 17 ... MUTATION partial: failure expected"; coords exits 2 with rho_6a above 1; swap exits 0 with "backward integration failed
     ... MUTATION swap: failure expected"; b_float.py --mutate=w exits 0 (the float flow lies outside B, the line says "must exceed 1").
  5. python-flint and FLINT versions recorded (versions.txt).

Results (macm3, main 9286b05b, python-flint 0.9.0, FLINT 3.6.0). Awake time equals wall time (awake.log).
  run: exit 0 at 20:44:28 UTC, 447 s, 615 steps, start box radius 4.39e-12, final state radius 1.07e-09, max radius of B 3.03e-05 (the old B: 3.24e-05), |H| <= 6.54e+01,
  |G_slow^-1| <= 5.30e+00, rho_6a = [0.2120798569 +/- 1.46e-11] < 1 (old B at x^: 0.2310), ok true. Lemma S contraction 0.7247, Lambda 0.4233.
  centre: centre_passed.txt (the --x argument) equals the box file's "p" to every digit (diff and compare_B_old_new.py); the run's log has no centre line (the script prints none).
  The effect of the centre: compare_B_old_new.txt, the new B's midpoints differ from #103's by up to 2.78e-06 = 0.183 of the new radius (0.178 of the old), none outside the new ball,
  which is the shift #39's float flow predicts.
  b_float.py on the new B (exit 0): the flow from p^ is within 5.31e-08 of rad(B) of mid(B) (below 0.01; max |B_float - mid(B)| 7.4e-13), the flow from x^ is at 0.183.
  Controls: partial exit 0 ("G_slow is 13 x 17 ... MUTATION partial: failure expected"), coords exit 2 (rho_6a 3.234, not below 1), swap exit 0 (step size underflow at t = 0.0585256,
  "MUTATION swap: failure expected"), b_float.py --mutate=w exit 0 (231 of rad(B) from both flows, must exceed 1).
  Observation for the coordinator (no code changed): with --x the script's "inside" test compares the centre with itself, and the script never reads the box file's "p", so the centre
  is only as right as the --x argument (checked here by diff). A box file with p and no x, run without --x, takes FPM.ZEROS silently, which is #103's case.
