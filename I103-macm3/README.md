# I103-macm3: lemma 6a(5) at sub-boxes 1e-18 and 1e-20

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint
0.9.0), main 700da3ae (lemma6_jump_M.py as at 7a36683, so B is stored exactly). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/103

From solver/proof/ with venv-macm3, two chains in parallel, 1 thread each, nice 10 under caffeinate -i. Each chain runs
certify_M2.py krawczyk, certify_M2.py export6a, then lemma6_jump_M.py --M=5 --rp=0.08 --k=20 --save-B, and stops if
Krawczyk or export6a exits non-zero. Sub-boxes 1e-18,1e-26,1e-27 and 1e-20,1e-28,1e-29. Each line's exact command is in
its .cmd file and its exit and wall time in exits.txt.

Results so far (1e-20w still running when this was written):
  sub 1e-18 (1e-18,1e-26,1e-27): Krawczyk exit 0 (margins +1.000 +1.000 +0.980 +0.980 +0.932 +0.932), export6a exit 0 (max
      radius 4.39e-12), lemma 6a exit 0 after 534 s: 615 steps, start box radius 4.39e-12, final state radius 1.07e-09, max
      radius of B 3.24e-05, |H| <= 7.30e+01, |G_slow^-1| <= 5.92e+00, rho_6a [0.2309898799 +/- 4.42e-13] < 1.
  sub 1e-20 (1e-20,1e-28,1e-29): Krawczyk exit 1, margins +0.999 +1.000 -0.989 -0.989 -5.799 -5.799, so the chain stopped
      there (krawczyk_sub1e-20.log and .cmd are kept).
  sub 1e-20w (1e-20,1e-27,1e-28), the rerun the coordinator asked for by Remote Control: Krawczyk exit 0 (margins +0.999
      +1.000 +0.801 +0.801 +0.320 +0.320), export6a exit 0 (max radius 5.23e-13), lemma 6a running.

Final results.
  sub 1e-20w: lemma 6a exit 0 after 542 s (04:06:26 UTC): 615 steps, start box radius 5.23e-13, final state radius 1.24e-10,
      max radius of B 3.89e-06, |H| <= 1.50e+01, |G_slow^-1| <= 1.56e+00, rho_6a [0.08801448685 +/- 2.00e-12] < 1.
  Controls on the 1e-18 result (the coordinator's Remote Control message), each to its own log, exits in exits.txt:
    partial (--load-B=B_M5_sub1e-18.json --mutate=partial): exit 0, "G_slow is 13 x 17: not square ... [MUTATION partial:
        failure expected]", reload prints the saving run's radii (final state 1.07e-09, B 3.24e-05).
    coords (--load-B=B_M5_sub1e-18.json --mutate=coords): exit 2, rho_6a 3.412 (not < 1), |H| <= 1.56e+03, so caught.
    swap (full run, --mutate=swap, no --save-B or --json): exit 0 after 232 s, start box radius 3.48e-01 and "backward
        integration failed (step size underflow at t = 0.058581030927598476) ... [MUTATION swap: failure expected]".
