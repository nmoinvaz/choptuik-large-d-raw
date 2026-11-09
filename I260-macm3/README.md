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
