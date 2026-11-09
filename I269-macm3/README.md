# I269-macm3: two of #231's M 40 circles rerun under the circle tool's alias rule

Machine: macm3 (Apple M3), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon on 1bad14fd, modecount_cx with B = 5), main e82c7648 (hp/modecount_circle.py with the alias rule of 14ddb64, #254/#257).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/269. The Mac has no M 40 build; macm3 has one (#231).

Inputs: the M 40 evals files of I231-macm3 (D55_M40/data: 433 lines, D61_M40/data: 856 lines: the counts' 293 and 723 determinants plus #231's circles), copied into D55/data and D61/data (evals only; cache_lines_before.txt), and the saved M 40 kf 23 states of the same runs, loaded from hp/data so that setup does not re-converge (sha256 in states_sha256.txt; they were
I231's, |F| 3.3e-19 and 3.8e-19). Commands (circles.cmd, caffeinate -is, nice 10, one thread, D 55 then D 61): hp/modecount_circle.py hp/data/states/up10_D55.0351.npz 0.06118,3.85263,0.3 2.04768412771239,0,0.2 and hp/data/seeds/local/up23_D61.0264.npz 2.0073,0.9727,0.2 2.043532530673195,0,0.2,
each with --M=40 --kf=23 --n0=20 --fmax=1e-15 and #231's tag (D55.0351_M40_kf23, D61.0264_M40_kf23), --data=<raw>/I269-macm3/<D>/data. Same centre, R and n0 as in #231.

Written before the run. Pass: the lam_phys circle at each D winds +1 (else that D's circle is not read). Each rerun winding is "unchanged" when it equals #231's (D 55.04 at 0.0612 + 3.8526i, R 0.3: 0; D 61.03 at 2.0073 + 0.9727i, R 0.2: +1 with the zero at 2.042590 + 1.150727i), "corrected" when it differs;
for a winding +1 the zero's position and its estimate are compared with #231's. The new tool's own output (any alias line) is reported as printed. The number of new determinants (cache lines after minus before) is reported.

Results (macm3, 19:28 to 19:32 UTC; awake.log: awake = wall; hp/data back to its states, the M 40 states in D55/ and D61/hp_data_after/). Cache lines before/after: D 55 433 -> 434 (1 new determinant), D 61 856 -> 863 (7 new determinants); circles.log of each D.
  D 55.04, circle (0.06118, 3.85263, R 0.3): winding 0 (29 points, max step 0.382, 0 mismatches, alias bisections 0, largest arc*scale 0.88): UNCHANGED (#231: 0). lam_phys circle (2.04768412771239, R 0.2): winding +1, zero 2.047684 -0.000000i, estimate 4.6e-08 (as #231), alias bisections 0 (0.52).
  D 61.03, circle (2.0073, 0.9727, R 0.2): winding +1 (37 points against 30 in #231, max step 0.352, 0 mismatches, alias bisections 9, largest arc*scale 0.93), zero 2.042590 +1.150727i, estimate 6.4e-03: UNCHANGED (#231: +1, the same zero and estimate). lam_phys circle (2.043532530673195, R 0.2): +1, zero 2.043533 -0.000000i, estimate 2.1e-07 (as #231), alias bisections 0 (0.49).
  The alias rule added 9 bisections to the D 61 circle (7 new determinants), and changed no winding and no position.
