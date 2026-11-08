# I118-macm3: lemma 6b1(5) C1 ray at h = 1e-12 and 1e-15, and the set radius over h

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint 0.9.0, FLINT 3.6.0, Python 3.13.3, macOS-26.3.1-arm64-arm-64bit-Mach-O), main c282ab8a.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/118

From solver/proof/ with venv-macm3, two rays in parallel, 1 thread each, nice 10 under caffeinate -i: lemma6b1_cover_M.py ray
--M=5 --c1 --x=<p^ of data/A_M2_box_M5_1e-10.json> --h=1e-12 --tag=_c1h12 and --h=1e-15 --tag=_c1h15 (each .cmd has the exact
line, exits.txt each exit and wall time). The run directories are copied here as lemma6b1_runs_M5_c1h12/ and _c1h15/. The
table of set radius over h at rows 1, 6, 9 and 11 uses these two logs, I112-macm3/ray_h1e-9.log and I37-macm3/ray.log.

Results (macm3, main c282ab8a; the lemma 6b1 code is unchanged since I37-macm3). Exits and wall times are in exits.txt.
  ray --c1 at h = 1e-12: exit 0, 518 s. At h = 1e-15: exit 0, 516 s. Both 17 segments, 2520 Lohner steps, run beside each other.
  radius_over_h.txt: the state set radius over X divided by h at the end of every segment, for h = 1e-9, 1e-12, 1e-15, 1e-18.
  Radius over h is the same, to 1%, for h = 1e-9, 1e-12 and 1e-15 (rows 1, 6, 9, 11: 2.58, 5.16, 11.1, 29.6 at 1e-9; 2.58, 5.16, 11.2,
  29.8 at 1e-15), and 2 to 11 times larger at 1e-18 (5.27, 38.3, 84.9, 277). The Lohner step counts are equal at every h.
  The excess is additive: radius = a(u) h + F(u), a(u) = radius(1e-9)/1e-9. F from h = 1e-15 and from h = 1e-18 agree within the
  printed 3 digits, and F/a is about 6e-18 to 8e-18 for |u| below 250 (1.0e-18 at the first segment end).
