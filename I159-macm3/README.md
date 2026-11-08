# I159-macm3: what sets the D 61 M 48 residual floor with the cut, a higher cut

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint 0.9.0, FLINT 3.6.0,
hpkernel 0.1.0 neon), main e04d6f17. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/159

Hypotheses and reading, fixed in the issue body before the runs: (a) the double-double rounding floor of the residual (unlikely, M 32 reaches 3.8e-23 at
this D); (b) the cut itself, kf 13 freezing harmonics 13-23 at M 48 against 13-15 at M 32. If |F| falls as the cut rises, (b) holds; if it stays at
2.7e-15 for every cut, (a) or another floor.

From the repository root with the venv's bin first on PATH, 1 thread each, nice 10, caffeinate -is, --data in data/ (empty): job 6's line,
python3 hp/modecount_wind.py hp/data/seeds/local/up23_D61.0264.npz --M=48 --kf=K --h0=0.6 --lam=2.043532530673195 --fmax=1e-15
--tag=D61.0264_M48_kfK --data=<raw>/I159-macm3/data, for K = 17 and 21. setup saves a re-converged state into hp/data, which is copied to
hp_data_after_kfK/ and moved out. For reference: kf 13 (I70-macm3 job 6) stalled at 2.7e-15 in the layout, after Newton and after Levenberg-Marquardt.

Results (macm3, main e04d6f17). Awake time equals wall time (awake.log).
  kf 17: exit 1, 708 s. |F| 1.3e-06 in the M 48 layout, 9.3e-07 after Newton, 1.4e-15 after Levenberg-Marquardt, then RuntimeError "|F| = 1.4e-15 > 1e-15"; no count.
  kf 21: exit 0, 19277 s (5.35 h). |F| 1.3e-06 in the layout, 1.3e-06 after Newton, 1.3e-19 after Levenberg-Marquardt (passes); 707 new determinants (data/
  modecount_D61.0264_M48_kf21_evals.jsonl), 26.6 s each (5.22 h of the 5.35 h). For comparison kf 13 (I70-macm3 job 6, and October's cloud run): 2.7e-15 after Levenberg-Marquardt.
  Count at kf 21, edges: 14, 12 resolved; "Im=y2, Re aR->aL" has 350 points, phase change of g +79.57 rad, "verified 183 (mismatch 9) in 4 passes", UNRESOLVED; the
  boxes that use it (U, full) are printed "UNRESOLVED: not a count". Boxes (winding of g; expected zeros; winding of det M): B0 0; 1; 1. U0 0; 0; 0. B1a 0; 1; 1.
  B1b +4; 1; 5. B1c +2; 0; 2. B1 +6; 2; 8. U +9 (unresolved); 0; 2. full +24 (unresolved); 2; 12. wind(g) is not 0 in B1b, B1c and B1: a finding. The estimate posted
  at 12:20 UTC (480 to 510 evaluations, finishing 13:30 to 14:00) was low: the unresolved edge took 350 points on its own.
  hp/data: the new kf17 and kf21 states were copied to hp_data_after_kf17/ and hp_data_after_kf21/ and moved out. hp/data is clean.
