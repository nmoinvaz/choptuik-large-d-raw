# I112-macm3: lemma 6b1(5) c1check and its nov control at h = 1e-9

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint
0.9.0), main ed429084. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/112

From solver/proof/ with venv-macm3, 1 thread, nice 10 under caffeinate -i, in order (each .cmd has the exact line,
exits.txt each exit and wall time): lemma6b1_cover_M.py ray --c1, c1check, c1check --mutate=nov, all with --M=5
--x=<p^ of data/A_M2_box_M5_1e-10.json> --h=1e-9 --tag=_c1h9. The run directory solver/proof/lemma6b1_runs_M5_c1h9/ is
copied here as lemma6b1_runs_M5_c1h9/.

Results (macm3, main ed429084; the lemma 6b1 code is unchanged since I37-macm3). Exits and wall times are in exits.txt.
  ray --c1 at h = 1e-9: exit 0, 565 s, 17 segments, state set over X radius 2.34e-09 at the start and 1.40e-04 at |u| = 23.46.
  c1check: exit 0, 31 s, "C1 PLANTED TRUTH: every point inside its set: True", all 13 points in rows 1, 6, 9 and 11, set radii
      2.61e-09, 5.23e-09, 1.12e-08 and 2.99e-08.
  c1check --mutate=nov: exit 0, 31 s, "every off-centre point outside: True (must be True)": the 12 off-centre points are OUT
      in all four rows, set radius 1.00e-11 (the tolerance), so the control now fires.
  Side observation: set radius over h at rows 1, 6, 9 and 11 is 2.6, 5.2, 11 and 30 at h = 1e-9, and 5.3, 38, 85 and 277 at
  h = 1e-18 (I37-macm3 ray log), 2 to 9 times larger at the smaller h. The cause was not investigated.
