# I189-mac: independent review of Theorem A(5)'s trusted integration code, with CAPD as a second validated integrator

Machine: mac (Apple M5 Mac, 10 cores, macOS 27.0.1), /Users/nathan/venv-qd (Python 3.13.15, python-flint 0.9.0 with
FLINT 3.6.0, mpmath 1.3.0 with the pure-Python backend, numpy 2.5.4). CAPD 6.1.0 at commit
37057e5899bccaa6cd5701057b7e6ea5e232ef8b, built with -DCAPD_ENABLE_MULTIPRECISION=ON -DCAPD_INTERVAL_TYPE=NATIVE (filib
needs x86 SSE), against MPFR 4.2.2 and GMP 6.3.0 (Homebrew), Apple clang 21.0.0. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/189. Code: solver/proof/review_189/ on branch wip/i189. At most 2
processes, nice 10. exits.txt has each run's exit status and wall time; scripts/ the shell scripts that ran everything
(W = the review_189 directory, R = this folder).

Contents.

- inputs/: capd_m5's inputs, written by review_189/export_inputs.py from the stored files. start6b1.txt is the C^1
  start set of I38-macm3/lemma6b1_runs_M5_cert/ray.json sets["0"] at s0 = 405 e^{-3 i pi/4}. path6b1.txt has the 17
  ray legs and row 17's 10 disc times (exact binary values); path_leg1.txt is the first leg; path6b1_row00.txt is row 0's
  arc. start6a_I103.txt and start6a_I184_phat.txt are the hull of y and sigma(y) at xi1 = 0.3 from
  I103-macm3/A_M2_6a_M5_sub1e-18.json, with w at x^ (as I103 ran) and at p^ (as I184 ran). *_perturb* are the start
  mutations.
- b1_clean.log, cmp_b1_clean.{log,json}: lemma 6b1(5), capd_m5 c0 (128-bit C^0 doubleton, order 32, tol 1e-26) through
  the ray and row 17's arc, against ray.json starts and I39-mac/disc_inputs/row_17.json. b1_leg1_calibration.log is the
  first-leg calibration run with the same settings. b1_row00.log and cmp_b1_row00.* are row 0's arc.
- a_clean_I103.log, a_clean_I184.log and cmp_a_clean_*: lemma 6a(5), capd_m5 c1 (double C^1 doubleton, order 20,
  tol 1e-17) against I103's B (at x^) and I184's B (at p^). cmp_a_phat_run_vs_I103.* and cmp_a_xhat_run_vs_I184.* run
  each centre against the other's stored X and B (both must miss).
- mut_b1_*.log, cmp_mut_b1_*: the 6b1 mutations on the first ray leg: capd (capd_m5), orig (review_189/orig_mut.py, the
  original validated_int.Lohner with lemma6_common under the same mutation), cross (the two mutated runs against each
  other), and orig_none (the original unmutated, the harness control). mut_a_*.log, cmp_mut_a_*, B_orig_mut_*.json: the
  same for 6a's backward flow.
- series_check.log: review_189/series_check.py, the start data at s0 against an independent mpmath recursion of the
  formal series (numerical evidence).
- kmin_check*.log: review_189/kmin_check.py, the detected first nonzero orders of fixed_point.tail_maj against the
  structural ones, at x^ and at p^, and its mutation control. The first kmin_check_mut_series run (rc 1 in exits.txt)
  stopped on run_M's own refusal; the script now counts a refusal as non-structural, and the rerun exits 0.

Results (2026-11-08; the closing summary on #189 has the full tables).

- Lemma 6b1(5), ray and row 17: all 1053 components of the 27 stops (17 ray legs, 10 discs) overlap the stored boxes.
  All 1053 of the review's enclosures lie inside the stored ones, with radii 0.12 to 0.95 of the stored radii and
  midpoints within 6.0e-08 of the summed radii. CAPD takes 363 steps (236 on the ray, 127 on the arc) in 4877 s; the
  original took 2520 + 1838.
- Lemma 6a(5): 1482/1482 components (X and the four real enclosures of each B entry) overlap I103's at x^ and I184's at
  p^. Each centre's run misses the other centre's X on 15 of 38 components, while B overlaps.
- Mutations: the sign of [[C E] P], the coefficient 2 of -(2 + s) Q scaled by 1 + 1e-9 (6b1) or 1 + 1e-5 (6a), and a
  perturbed start (Re P_{+1} + 1e-15 for 6b1; Re D_{+1} + 1e-7 for 6a). Each makes both the review and the original miss
  the stored enclosures, and each pair of mutated runs agrees with itself.
- series_check: the independent series reproduces the stored centre to 2.3e-77, the estimated remainder is 3.5e-06 of
  the stored eta radius, and the derivative columns agree to 1.2e-27 of their radii. kmin_check passes at x^ and p^, and
  its series mutation fails.
