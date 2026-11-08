# I37-macm3: lemma 6b1(5) pilot, the C1 ray and the innermost row 17, on p^ +- 1e-18

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint
0.9.0), main 700da3ae. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/37

From solver/proof/ with venv-macm3, 1 thread, nice 10 under caffeinate -i, in this order (each .cmd has the exact line,
exits.txt each exit and wall time): lemma6b1_cover_M.py ray --c1, c1check, c1check --mutate=nov, row --j=17, mutate
--j=17, all with --M=5 --x=<p^ of data/A_M2_box_M5_1e-10.json> --h=1e-18 --tag=_cert. The run directory
solver/proof/lemma6b1_runs_M5_cert/ is copied here as lemma6b1_runs_M5_cert/ at each push.

Results (macm3, main 700da3ae). Exits and wall times are in exits.txt.
  ray --c1: exit 0, 484 s, 17 segments from |u| = 405 to 23.46, 2520 Lohner steps, state set over X radius 2.34e-18 at the
      start, 5.27e-18 after the first segment, 1.20e-12 at |u| = 23.46; 0.189 s per step.
  c1check: exit 0, "C1 PLANTED TRUTH: every point inside its set: True" (rows 1, 6, 9, 11), 34 s.
  c1check --mutate=nov: exit 3, "every off-centre point outside: False (must be True)", 28 s. The control did not fire.
      The planted points x^ +- h are equal to x^ as doubles in the first three parameters (ulp 4.4e-16, 1.1e-16, 2.8e-17
      against h = 1e-18), and c1check inflates every set by tol = 1e-11, so at h = 1e-18 the check cannot tell the
      derivative columns from their absence.
  row 17: exit 0, 353 s, all 10 discs certified, Lam 0.332 down to 0.211, box radius 1.2e-12 up to 3.3e-05,
      1838 Lohner steps (0.192 s per step). row_17.json in the run directory is this result (mutate runs do not save).
  mutate --j=17: exit 0, 354 s, 0 of 10 discs certified (must be 0).
Projection of the full run: projection.txt, from design_M5.txt and the ray log.
