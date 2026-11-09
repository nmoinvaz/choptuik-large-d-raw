# I260-macm3: the full D 30.07 count at M 48, no cut, on #141's inner-node layout (nodes 0.15 ... 0.7)

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3-314 (Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon rebuilt on 1bad14fd, modecount_cx for 3.14 with B = 5), main d4a74472
(#242's alias rule and #141's fitted layout). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/260.

State: I141-mac/states/modecount_state_D30.0688_M48_inner015.npz (sha256 in state_sha256.txt): D 30.068824, M 48, nodes [0.15, 0.3, 0.4, 0.5, 0.6, 0.7], kt 36, kc 414, ks 100, stored |F| 2.4e-26. Because M equals the state's M, setup loads this file as given (no resample, no fit_nodes, no saved copy).
Command (count.cmd, caffeinate -is, nice 10, one thread): python3 hp/modecount_wind.py <state> --M=48 --h0=0.6 --lam=2.0797477 --fmax=1e-15 --resolve=last --tag=D30.0688_M48_inner015 --data=<raw>/I260-macm3/data. Below D 35 the default layout has no cut (no --kf).
No cache for this tag is in --data (empty), so every determinant is fresh.

Written before the run. Setup: if it refits the layout or refuses the state (a RuntimeError, a Newton/LM line in the log), the count is stopped and that is reported before counting (coordinator); the expected line is the stored |F| (no Newton) and "series truncation".
Gate: setup |F| <= 1e-15. Table: the 8 boxes with both mismatch counts per edge (all passes and the last pass), against October's no-cut D 30 M 48 count (B1c +2, full +2: the pair at 4.267 + 1.324i, #68, #148) and the kf 13 count of #148 (all 0).
Reading rules, fixed now: the pair is "absent on this layout" when B1c and full are 0 and no other box is nonzero (then the October pair came with the old layout); any box nonzero is reported as a finding, with its winding, whether or not it is B1c. An edge that does not resolve under --resolve=last is "not a count" and its boxes are not read.
The alias rule (#242, on main) is the code's default; its effect is read from the log if it prints one. No zero is located here.

Result (macm3, main d4a74472, venv-macm3-314 = Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0; awake.log: awake = wall 3701 s; hp/data unchanged, no state saved):
  Setup (count.log): loaded the state as given: no Newton or Levenberg-Marquardt line, |F| 2.4e-26 (gate 1e-15), series truncation centre 1.7e-106 (ratio 0.566 at 0.15), horizon 3.8e-39 (ratio 0.389 at 0.3); the setup neither refit the layout nor refused the state.
  Count: exit 0 at 19:37:46 UTC, 82 determinants (78 distinct points, four corners twice, equal to 3.6e-12 rad), 45.1 s each (load 6 to 7), pivot minima 7.3e-09 to 2.1e-03. All 14 edges resolve: mismatches 0 in any pass and 0 in the last pass, alias bisections 0 on every edge,
  largest step 0.376 rad, at most 3 passes; the real axis has only the two expected sign changes. wind(g) is 0 in all 8 boxes (winding of det M: B0 1, U0 -1, B1a 1, B1b 1, B1c 0, B1 2, U -7, full -12; contour aLL -0.150, aL 0.300, a1 1.2318, a2 2.6797, aR 6.1820, omega 3.198742).
  October's no-cut count (B1c +2, full +2: the pair at 4.267 + 1.324i) is absent on this layout, and no other box changed (all 0 as in the kf 13 count of #148). Reading rule: "absent on this layout".
