# I178-macm3: the cut scan of the extra real zero at D 45.05, M 48 (small circles, kf 13 to 21)

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint 0.9.0, FLINT 3.6.0, hpkernel 0.1.0 neon), main e04d6f17.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/178

`run_kf.sh K [K ...]` runs the issue's command for each K in turn (1 thread, nice 10, caffeinate -is): python3 hp/modecount_circle.py hp/data/states/up7_D45.0507.npz
1.11,0,0.12 2.057,0,0.1 --M=48 --kf=K --fmax=1e-15 --tag=D45.0507_M48_kfK_circ --res=<raw>/I178-macm3/circles.jsonl, then moves the evaluation cache, the log and any
re-converged state from hp/data into data_kfK/. The up7 state is M 32 native, so each K resamples to M 48 and re-converges in its layout (Newton, then Levenberg-Marquardt).
No D 45 M 48 state is in hp/data at the start, so every K is fresh (hp_data_before.txt).

Written before the run.
  Controls (a control that fires stops the work until the cause is known): the 2.057 circle winds +1 at every K; the 1.11 circle winds 0 at kf 13 and +1 at kf 21
  (#70 job 7, #170). kf 13 runs first, alone, and its two controls are read before any other K starts.
  Verdict per K: the winding of the 1.11 circle with its largest phase step and verification mismatches, and the setup |F|. A setup above 1e-15 is reported, not forced.
  Locating: where the 1.11 circle winds +1, two circles of half radius (0.06) at 1.05 and 1.17 (the zero is real at kf 21, by the sign change in (1.0, 1.221)), then two of 0.03
  around the one that winds +1, to place the zero within about 0.03. A winding of +1 in neither half (zero off the axis, or two zeros) is reported as it is, with the windings.
  Cost note (not a result): the 1.11 circle's detrending point c - 2R = 0.87 lies 0.0014 from the expected zero lam_g = 0.8714, so beta is large and the circle needs more points;
  the winding does not depend on beta.

Results of the scan (kf 13 to 21; each K 29.6 to 31.2 min wall, exit 0, caffeinate -is held; awake.log): see circ_kf<K>.log and circles.jsonl.
  The 1.11 circle winds 0 at kf 13, 15, 17 and 19 and +1 at kf 21; the 2.057 circle winds +1 at every K; both controls hold. Setup |F| after Levenberg-Marquardt:
  2.0e-18 (kf 13, the saved state is byte-identical to #70 job 7's), 3.9e-19, 2.7e-18, 3.7e-17, 8.2e-17 (kf 21, as in #170). Every circle has max step 0.35 to 0.38 rad and 0 mismatches.
Locating at kf 21 (run_locate.sh, round 1: two circles of R 0.06 at 1.05 and 1.17, which cover the real segment 0.99 to 1.23 where #170's sign change is; round 2: two of R 0.03
  around the one that winds +1): round 1 re-converges the state (setup) and is compared to data_kf21/'s state with cmp; the state stays in hp/data for round 2 and moves out after it.
  Round 1 (exit 0, 20:08:54 UTC; the re-converged kf 21 state is byte-identical to data_kf21/'s, |F| 8.2e-17): circle 1.05 (R 0.06) winds 0, circle 1.17 (R 0.06) winds +1.
  So the zero is in the disc 1.17 +- 0.06. Round 2: circles of R 0.03 at 1.14 and 1.20 (together the real segment 1.11 to 1.23).
  Round 2 (exit 0, 20:33:16 UTC; state again byte-identical, moved to locate_r2/): circle 1.14 (R 0.03) winds +1 (29 points, max step 0.376 rad), circle 1.20 (R 0.03) winds 0
  (22 points, max step 0.609 rad), 0 mismatches in both. The zero is in the disc |lam - 1.14| < 0.03, which meets the real axis in (1.11, 1.17), inside #170's sign change (1.0, 1.221).

Final (macm3, main e04d6f17; awake time equals wall time in every run, awake.log): the extra zero is absent at kf 13, 15, 17 and 19 (7 to 10 odd harmonics in the set), present at kf 21
  (11), at lambda = 1.14 +- 0.03; the 2.057 control winds +1 at every K; the two setups run twice agree bit for bit (kf 13 with #70 job 7, kf 21 in four runs: #170's, the scan's, round 1 and round 2).
  hp/data unchanged by the whole task (hp_data_before.txt). summarize.txt: every circle.
