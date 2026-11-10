# I270-macm3: the four circles of #270 on the D 61.03 M 48 kf 23 state with an inner node at 0.15

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon on 1bad14fd, modecount_cx with B = 5), main bfe5fd54 (--centre_tol of #265/#270). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/270. The state, the code and the control
come from the Mac subagent (I270-mac: wip/i265 at 406fefd merged into main; the control wound +1 there, 2.0435325241 + 1.2e-7i, estimate 6.7e-7).

Inputs: I270-mac/circles/ (the evals cache: 54 lines = the control circle's determinants and 24 of the first circle, the log and the records) copied into circles/; I270-mac/states/modecount_state_D61.0264_M48_kf23_ct1e-150.npz copied into hp/data (sha256 in state_sha256.txt, equal to the original), so that setup loads the layout with nodes 0.15, 0.3 ... 0.7, ks 127, |F| 1.3e-19 and does not re-converge.
Command (circles.cmd, caffeinate -is, nice 10, one thread): python3 hp/modecount_circle.py hp/data/seeds/local/up23_D61.0264.npz 1.3065,1.4158,0.2 2.0073,0.9727,0.2 2.5584,0.5825,0.2 3.0196,0,0.2 --M=48 --kf=23 --centre_tol=1e-150 --fmax=1e-15 --n0=20 --data=<raw>/I270-macm3/circles --tag=D61.0264_M48_kf23_inner015.

Reading rule, posted before the runs (coordinator, copied): all four circles wind 0 -> the extras belong to the layout (as the D 30 pair did); winding +1, +1, +1, +2 (#230's layout: the real-axis circle at 3.0196 holds the pair at 3.0196 +- 0.0958i) -> they persist; anything else is mixed and reported circle by circle with the zeros inside.
If a circle is not resolved, there is no reading. Gate: setup |F| <= 1e-15 and both series <= 1e-15 on the solution (setup refuses otherwise, #265), and the state must load without a refit: a Newton or LM line in the log is reported. Estimates are the circle's own ranges, not bounds.
Note on the cache: 54 determinants were evaluated on the M5 Mac for the same state with the same code; the new ones are evaluated here (both Apple ARM NEON builds); a mismatch between cached and recomputed values at a shared point would show as a difference in the cache's duplicate points and is looked for.

Results (macm3, main bfe5fd54; awake.log: awake = wall 5201 s, 00:15:06 to 01:41:47 UTC, exit 0; hp/data back to its states, the state in hp_data_after/). Setup loaded the inner-node layout as given (no Newton/LM line), |F| 1.3e-19, series on the solution centre 3.6e-234 (ratio 0.281 at 0.15), horizon 6.1e-38 (ratio 0.473 at 0.3).
  Cache: 54 lines before, 167 after (113 new determinants, ~50 s each under load). The four circles (R 0.2, n0 20, tol pi/4, alias rule), all with 0 verification mismatches and 0 alias bisections:
    1.3065 +1.4158i: winding +1, zero 1.306564 +1.415818i (estimate 1.0e-06), 27 points, largest step 0.389
    2.0073 +0.9727i: winding +1, zero 2.007342 +0.972730i (6.8e-07), 29 points, 0.363
    2.5584 +0.5825i: winding +1, zero 2.558433 +0.582466i (4.4e-07), 29 points, 0.367
    3.0196 +0.0000i (real axis): winding +2, zeros 3.019620 +0.095807i (5.0e-06) and 3.019620 -0.095807i (4.7e-06), 44 points, 0.390
  The control (I270-mac): winding +1 at 2.0435325241 (6.7e-7). Reading by the rule posted before the runs: +1, +1, +1, +2 -> the extras PERSIST on the inner-node layout; they do not belong to the old layout (first node 0.3).
