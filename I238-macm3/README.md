# I238-macm3: the extra zeros of D 55.04 and D 54.04 located (moments from the counts' samples, then circles)

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3-314 (Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon rebuilt on 1bad14fd, modecount_cx for 3.14), main d5ddb3ba.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/238 (D 54.04 added by the coordinator, and the B1a pair of #241's fixed-column count at D 55.04).

Inputs: the counts' evals files and modecount_results.jsonl, copied: D55/data from I232-macm3/D55 (automatic edges: B0 +2, U0 +1, U +1), D54/data from I240-macm3 (B0 +2, U0 +2), D55fixed/data from I241-macm3/D55 (fixed column Re -0.096 to 0.124: B1a +2).
Step 1 (moments, no new determinant: the evals files must have the same number of lines before and after): hp/modecount_moment.py <tag> <state> <boxes> --data=<D55|D54|D55fixed>/data --out=<...>/moments.json (moments.cmd).
Step 2 (circles, caffeinate -is, nice 10, one thread, on the saved kf 23 state of the count, loaded from hp/data so that setup does not re-converge, then moved out): hp/modecount_circle.py <state> RE,IM,R ... <lam_phys>,0,0.2 --M=48 --kf=23 --n0=20
--fmax=1e-15 --tag=<tag> --data=<folder>/data. R 0.2, smaller where zeros are closer; B0's moment positions are good to about 0.05 only and their spread cannot flag a bad one (#230).

Written before the run. A zero is "located" when its circle winds +1 (a winding 0 widens the circle; a winding 2 means two zeros, located by the circle's second moment output if it prints one). The lam_phys circle (R 0.2) must wind +1: if it does not,
the circles at that D are not read. Report: each zero's position (Re, Im) with the moment spread and the circle's own position estimate and its error estimate, the circle's winding, and Im lambda against omega for the U and U0 zeros
(equal to omega within the location's spread or not; omega is in each count's log: 3.444217 at D 55.04, 3.438215 at D 54.04). Then Re lambda of the pair as D goes 54.04 -> 55.04 (B0 pair of D 54.04, B1a pair of D 55.04) is the quantity to watch (coordinator).
Estimator ranges are not bounds. If #241's or #243's corrected windings differ from these counts' windings, the corrected ones are used and said.

Moments (exits.txt; moments.log and moments.json in D55/, D54/, D55fixed/; the evals files have the same line counts before and after: 177, 160, 260; no new determinant):
  D 54.04 (automatic edges), B0 (+2): upper-half zero -0.04917 +0.90331i, spread 6.6e-3 (and its conjugate); U0 (+2): -0.12734 +2.63934i (spread 2.7e-2) and 0.07037 +4.50130i (spread 2.1e-2).
  D 55.04 (automatic edges), B0 (+2): 0.20303 +0.25507i, spread 1.5e-2; U (+1): 0.32347 +3.33099i, spread 5.0e-2; U0 (+1): NOT LOCATED (the tool refuses: winding 1.000002 of the strip contour "is not a small non-negative integer", exit 1 of that call, reported not fixed).
  D 55.04 fixed column (#241), B1a (+2): 0.19969 +0.25186i, spread 6.5e-3 (half contour 0.19969 +0.25831i). It agrees with the B0 moment of the automatic count within the spreads (0.0034 in Re, 0.0032 in Im): the same pair.
Circles (circles.cmd per D; the saved kf 23 states are loaded from hp/data, sha256 in states_sha256.txt equal to I241's). D 55 adds a search circle (0.07, 4.5, R 0.5) for the U0 zero that the moment could not give, centred on D 54.04's U0 zero at 0.070 +4.501i; if it winds 0 or 2 that is reported, not tuned.

Second round (after the first circles): the moment tool refused D 55's U0 on the automatic-edge count (winding 1.000002), but accepts it on the fixed-column count of #241 (D55fixed/, moments_U0_U.log): U0 0.07342 +3.83880i (spread 1.0e-01), U 0.32862 +3.33743i (spread 7.2e-02); D54fixed/ (the fixed-column D 54.04 count): B0 -0.05073 +0.90592i (6.6e-03), U0 0.07551 +4.49619i (6.8e-02),
  equal to the circle's 0.071138 +4.504467i within the spread. A circle (0.07342, 3.83880, R 0.3; D55/circles_U0.cmd) for the D 55 U0 zero is run next; it keeps clear of the U zero (0.319, 3.331) and of the zero found by the search circle (-0.227, 4.280).

Results (macm3, main d5ddb3ba, venv-macm3-314 = Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0; awake.log: awake = wall; ran beside I231's M 40 counts). positions.txt (positions.py): every circle and every moment.
  Every circle winds +1 with 0 verification mismatches (R 0.1 to 0.5, 27 to 36 points, max step 0.42 rad); the lam_phys circles wind +1 and return the expected zero: D 54.04 2.048452 +0.000000i (estimate 7.0e-09, gamma_dd: 2.048451702933),
  D 55.04 2.047684 -0.000000i (4.0e-08, 2.04768412771). The saved kf 23 states are in D54/ and D55/hp_data_after/ (sha256 equal to I241's), hp/data back to its states apart from I231's running M 40 states.
  Positions (circle, estimate = the circle's own n0/2-against-n0 range, not a bound): D 54.04: B0 pair -0.022010 +0.936549i (1.1e-06; the moment gave -0.04917 +0.90331i, spread 6.6e-3, 0.043 away: B0's moment spread did not flag it, as #230 said);
  U0 -0.130957 +2.642560i (5.9e-07) and 0.071138 +4.504467i (1.5e-06). D 55.04: pair 0.199572 +0.254752i (4.7e-07 by the R 0.1 circle at B1a's moment; 2.8e-04 by the R 0.2 circle at B0's moment), U 0.318948 +3.331400i (5.5e-05),
  U0 0.061179 +3.852625i (6.1e-04; found with the fixed-column moment, the automatic-edge call refused its winding 1.000002), and one zero at -0.226688 +4.280040i (5.4e-03) found by the search circle (0.07, 4.5, R 0.5), outside U0's box (Re < -0.096).
  Im lambda against omega (3.438215 at D 54.04, 3.444217 at D 55.04): D 55.04 U zero 3.3314 (omega - 0.113), U0 zero 3.8526 (omega + 0.408); D 54.04 U0 zeros 2.6426 (omega - 0.796) and 4.5045 (omega + 1.066): none equal to omega.
  The pair (B0 at D 54.04, B0 and B1a at D 55.04) moves from -0.0220 +0.9365i to 0.1996 +0.2548i over delta D = 0.9938: Re lambda +0.222, Im lambda -0.682. Re lambda > 0 at D 55.04.
