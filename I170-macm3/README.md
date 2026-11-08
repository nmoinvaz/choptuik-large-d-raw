# I170-macm3: the D 45 mode count at M 48 with the cut raised to kf 21

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint 0.9.0, FLINT 3.6.0, hpkernel 0.1.0 neon), main e04d6f17.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/170

From the repository root with the venv's bin first on PATH, 1 thread, nice 10, caffeinate -is (count.cmd): python3 hp/modecount_wind.py hp/data/states/up7_D45.0507.npz
--M=48 --kf=21 --h0=0.6 --lam=2.056738610147195 --fmax=1e-15 --tag=D45.0507_M48_kf21 --data=<raw>/I170-macm3/data (empty, so every determinant is fresh).

Written before the run. The question is wind(g) in the 8 boxes (B0, U0, B1a, B1b, B1c, B1, U, full), not a stop. Reading, fixed now:
  wind(g) = 0 in every resolved box: the extra zeros of #159 belong to D 61 (not to M 48 with the higher cut alone).
  wind(g) nonzero in a resolved box: they come with M 48 and the higher cut at a second D (D 45 is clean at kf 13, #70 job 7).
An edge that does not resolve is "not a count" and its boxes are not read. Each box is set against #70 job 7 (D 45 M 48 kf 13: all 0) and #159 (D 61 M 48 kf 21).
Setup: the state up7_D45.0507.npz is M 32 native (769 unknowns, the same as the D 61 M 32 seed), so setup resamples to M 48 (1153 unknowns) and re-converges (Newton, then Levenberg-Marquardt) and saves
modecount_state_D45.0507_M48_kf21.npz into hp/data (moved here afterwards, hp/data restored). If |F| stays above --fmax = 1e-15 setup raises: that is a stop, reported
as such (as at D 61 kf 17 in #159), and the count is not run. #70's kf 13 setup reached |F| 2.0e-18 in 2648 s for 81 determinants at 25.7 s each.

Results (macm3, main e04d6f17). Awake time equals wall time if awake.log says so (see below).
  exits.txt: count exit 0 at 16:41:28 UTC. 3810 s wall from 15:37:58 (setup about 8.5 min: |F| 3.3e-09 in the layout, 3.2e-09 after Newton, 8.2e-17 after Levenberg-Marquardt, below the
  1e-15 gate, state saved to hp/data and moved to hp_data_after/), then 129 new determinants at 25.5 s each (data/modecount_D45.0507_M48_kf21_evals.jsonl, 127 distinct points).
  All 14 edges resolve (largest step 0.387 rad, 0 verification mismatches, at most 3 passes), so every box is a count.
  wind(g) is NOT 0: B1a +1, B1 +1, U +1, full +3 (B0, U0, B1b, B1c 0). One zero beyond the expected ones in B1a (0.3 < Re < 1.221, |Im| < 1.687), and, with the windings additive over the boxes,
  one in U and one in the mirror strip -5.061 < Im < -1.687 (full +3 less B1 +1 and U +1), which makes full +3. The real axis shows it too: the sign of det M changes in (0.5, 1.0) (expected lam_g 0.871),
  in (2.0, 2.5) (expected lam_phys 2.057) and in (1.0, 1.221), which #70's kf 13 count does not have (this reads the same determinants, not another evaluation).
  compare_boxes.txt: the boxes of #170, #70 job 7 (D 45 M 48 kf 13, all 0) and #159 (D 61 M 48 kf 21, +4 B1b, +2 B1c, U and full not counts). The extras are in other places at
  the two D. Evaluation noise at this count: the corner points evaluated twice differ by up to 1.3e-8 rad, pivot minima 4.9e-14..2.0e-06, so no winding is in doubt.
  This is the reading fixed above: extra zeros at a second D, with M 48 and the cut at 21 (and not at kf 13 or at M 32). Why, and which harmonics, is not tested here.
