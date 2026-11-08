# I160-macm3: the D 61 mode count at M 32 with the cut

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint 0.9.0, FLINT 3.6.0,
hpkernel 0.1.0 neon), main e04d6f17. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/160

From the repository root with the venv's bin first on PATH, 1 thread, nice 10, caffeinate -is: python3 hp/modecount_wind.py
hp/data/seeds/local/up23_D61.0264.npz --M=32 --kf=13 --h0=0.6 --lam=2.043532530673195 --fmax=1e-15 --tag=D61.0264_M32_kf13
--data=<raw>/I160-macm3/data (empty, so every determinant is fresh). The seed is M 32 and native (|F| 3.8e-23), so setup does not resample or save.
The 8 boxes are compared with October's D 61 M 32 records (hp/data/modecount_D61.0264_M32.log and its cache). wind(g) not 0 in any box is a finding.

Results (macm3, main e04d6f17). Awake time equals wall time (awake.log).
  count.log: exit 0, 974 s, setup |F| 3.8e-23 (the seed, no resample, no save), 86 new determinants (data/modecount_D61.0264_M32_kf13_evals.jsonl). wind(g) is 0 in all 8
  boxes (printed +0.000000 or -0.000000): no extra zero. winding of det M: B0 1, U0 0, B1a 1, B1b 1, B1c 0, B1 2, U -7, full -12. Max phase step 0.384.
  compare_D61_M32.txt: October's hp/data/modecount_D61.0264_M32.log has two completed runs (10-21 22:45:46 and a replay 10-22 04:22:23, 16 box lines, no CR). The later
  one equals this run in every winding field (the sign of the printed zero and the max phase step differ). The earlier one has expected zeros inside 1 (U) and 4 (full)
  where this run and the later one have 0 and 2, with the same winding of det M (-7, -12). October's cache has 284 lines (159 with CR, 125 without, the Windows ones
  from the taller-strip and Re 12 variants); 42 of this run's points are in it, all on non-CR lines (written by the cloud): ln|det| differs by at most 3.3e-08 (median
  3.0e-12), arg by at most 1.2e-08, the largest differences at points with pivot minima of 2e-14 to 4e-14 on the Im = 5.215 and Re = -0.08 edges. None is on a CR line.
  hp/data: unchanged by this run.
