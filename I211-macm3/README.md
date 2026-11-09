# I211-macm3: the full D 45 count at M 48 with the cut at kf 23

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3-314 (Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx for 3.14),
main d72280ff. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/211. Runs in parallel with I212-macm3's count, one thread each.

Command (count.cmd, caffeinate -is, nice 10, from the repository root): python3 hp/modecount_wind.py hp/data/states/up7_D45.0507.npz --M=48 --kf=23 --h0=0.6 --lam=2.056738610147195 --fmax=1e-15
--resolve=last --tag=D45.0507_M48_kf23 --data=<raw>/I211-macm3/data > count.log. The up7 state is M 32 native, so setup resamples to M 48 and re-converges (I190: |F| 2.0e-19 at kf 23, 25 min including two circles);
the saved state moves out of hp/data afterwards. No D 45 M 48 kf 23 state or cache is in hp/data or --data at the start.

Written before the run. The 8 boxes' windings are set against #70 job 7's kf 13 count (all 0; I70-macm3/data) and #170's kf 21 count (B1a +1, B1 +1, U +1, full +3). wind(g) not 0 in a resolved box is a finding.
Gate: setup |F| <= 1e-15 (a miss raises: a stop, reported). Both mismatch counts are reported per edge (all passes, and the last pass as --resolve=last judges it). An unresolved edge is "not a count".
Expectation to be tested, not assumed: #190 saw the 1.14 circle wind 0 at kf 23, so B1a should be 0 at kf 23 where #170 had +1; the strip zeros of #170 (U +1, mirror +1) are not covered by #190's circles.

Results (macm3, main d72280ff, venv-macm3-314 = Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0; awake.log: awake = wall; this count ran in parallel with I212's, one thread each).
  count.log: exit 0 at 00:51:06 UTC, 2871 s (00:03:15 start). Setup: |F| 3.3e-09 in the layout, 3.3e-09 after Newton, 2.0e-19 after Levenberg-Marquardt (below 1e-15; the saved state moved to hp_data_after/, hp/data back to
  its states of hp_data_before.txt apart from I212's running kf 23 state). 81 evaluations (79 distinct points, two corners twice, equal to 4.4e-08 rad), 31 s each at the start (pivot minima 1.9e-12 to 1.6e-06).
  wind(g) is 0 in all 8 boxes (printed +-0.000000), exactly #70 job 7's kf 13 count box for box (compare_boxes.txt) and not #170's kf 21 count (B1a +1, B1 +1, U +1, full +3). Winding of det M B0 1, U0 0, B1a 1, B1b 1,
  B1c 0, B1 2, U -7, full -12. All 14 edges resolve under both rules: mismatches 0 in any pass and 0 in the last pass, largest step 0.382 rad, at most 2 passes, so U and full are counts. Real axis: sign changes only in
  (0.5, 1.0) and (2.0, 2.5) (expected lam_g and lam_phys), the kf 21 count's extra change in (1.0, 1.221) is gone.
  No finding. So at D 45, M 48: no extra zero at kf 13 and kf 23, extra zeros (B1a +1, one in each strip) at kf 21 only.
