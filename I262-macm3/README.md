# I262-macm3: the cut scan at D 61.03, M 40 (kf 21, 23, 25) with circles at the M 40 zeros

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon on 1bad14fd, modecount_cx with B = 5), main 6dd0e718. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/262 (low priority; I249 keeps the cores).
Pattern of #231: state hp/data/seeds/local/up23_D61.0264.npz (M 32 native), --M=40, --fmax=1e-15, tags D61.0264_M40_kf<K>, circles with n0 20 (circles_kf<K>.cmd, caffeinate -is, nice 10, one thread each). kf 21 and kf 25 run setups (resample to M 40, Newton/LM) in fresh folders;
kf 23 is #231's reference: its M 40 state (I231-macm3/D61_M40/hp_data_after, loaded from hp/data) and its evals cache (copied, evals only, into kf23/data), circles at the zeros that #231 did not circle.
Circles at the M 40 zero positions of #231 (D 61.03, kf 23): (a) 2.04259 +1.15073i (R 0.2; circle-confirmed in #231), (b) 2.7626 +0.6308i (R 0.2; moment, spread 7.5e-3), (c) 2.9141 +1.5885i (R 0.2; moment, spread 6.8e-3), (d) U0 0.0319 +3.0855i (R 0.3; moment, spread 2.3e-2),
plus the lam_phys control (2.043532530673195, R 0.2). B1b's moment zeros (spreads 0.1, 0.2) and the strip U's (spreads 0.25 to 0.7) are not used.

Written before the run. Gate: the setup's |F| <= 1e-15 per cut (else that cut stops and is reported). The lam_phys circle must wind +1 at a cut, else that cut's circles are not read. Tabulated against kf: each zero's circle winding and, for +1, its position and estimate.
Reading rule: a zero "stays" across the cuts when its circle winds +1 at all three cuts and its position changes by less than 0.05; "moves" when it winds +1 at a cut and its position differs from the kf 23 one by 0.05 or more; "absent" when a circle winds 0 at a cut (the circle of R 0.2 to 0.3 covers only a disc: a zero that moved farther is "absent" there).
The kf 23 circles at (b), (c), (d) are also the check of #231's moment positions. Estimates are the circle's own range, not bounds.

Results (macm3, main 6dd0e718; awake.log: awake = wall; the three batches ran beside I249's counts and circles; hp/data back to its states, the M 40 states in kf*/hp_data_after/). positions.txt (positions.py) tabulates every circle.
  Setups: kf 21 and kf 25: |F| 1.3e-06 in the layout, 1.3e-06 after Newton, 3.8e-19 after Levenberg-Marquardt (gate 1e-15 passed at both). The lam_phys circle winds +1 at each cut (kf 21: 2.043533 +0.0000i, estimate 2.6e-08; kf 25: 2.043532 -0.0000i, 8.5e-07; kf 23 from #231: 2.043533, 2.1e-07), so the circles are read.
  Zero by zero (winding, position): (a) 2.0426 +1.1507i: kf 21 0, kf 23 +1 (#231: 2.042590 +1.150727i), kf 25 0. (b) 2.7626 +0.6308i: kf 21 0, kf 23 +1 at 2.7995 +0.6290i (9.7e-07; the moment was 0.037 off), kf 25 0. (c) 2.9141 +1.5885i: kf 21 0, kf 23 +1 at 2.8997 +1.5920i (3.6e-06), kf 25 +1 at 3.0615 +1.7080i
  (9.9e-03; 40 points, 11 alias bisections): moved by 0.20 from kf 23. (d) U0 0.0319 +3.0855i: kf 21 0, kf 23 +1 at 0.0715 +3.0933i (1.1e-03), kf 25 0. All circles 0 verification mismatches. By the rule above: (a), (b), (d) exist at kf 23 only (absent at kf 21 and 25); (c) exists at kf 23 and kf 25 and moves by 0.20 (> 0.05); none "stays".
  A circle of R 0.2 to 0.3 covers a disc: "absent" means no zero within it.
