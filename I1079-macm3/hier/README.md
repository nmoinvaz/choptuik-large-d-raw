# I1079-macm3/hier: hier.py's M = 3 solve started at each excited zero (#1079)

Machine: macm3 (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1, arm64; runner macm3b). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1079 (from #1076).
Task from the coordinator (hc of 2026-11-23, after round 3's acceptance; #1079 is paused): "a cheap independent check: `solver/inner_stokes/hier.py` (main's, unchanged) at M = 3 started at each excited zero, with the p you have
(A, wf, B3, C3). Read its usage first (AGENTS.md: at most --procs 2). Report each converged point (A, wf, B3, C3) beside zero_mp's and value_mp's, its residual and solve count." Written 2026-11-23 14:51 UTC, before the runs.

## Prediction (the coordinator's, written before)

hier converges to each excited zero within about 1e-9 in A and wf (a second solver that shares no code with inner_mp/argcount), or names why it cannot start there.

## Code and usage

`~/Source/choptuik-large-d-1079/solver/inner_stokes/hier.py` of the clean worktree of main at a4cd5eaa7b297ffc6f171551fa15ba054e970e21 (blob b4e4d887, sha256 prefix 6134b17259aa1812, last changed in 656396fd), importing `inner_np.py` (blob 80b7edaa) from the same folder;
python 3.14.3, numpy 2.5.4 (`~/Source/venv-macm3-1058b`). hier.py's usage (its docstring and `main`):

    python -u hier.py M A wf [--fixA] [--x=B3,C3,...] [--seed=FILE] [--xi1=0.2] [--procs N] [--verbose=2] [--schur] ...

- M = 3: the unknowns are x = (A, w/w_inf, B3, C3); `--x=B3,C3` gives the harmonic-3 start (M - 1 = 2 numbers, so no seed file value is used); without `--fixA` the selection is full: S_3 = 0 innermost, then S_1 = 0 for (A, w) outermost,
  every level a damped 2 x 2 Newton with finite-difference chord Jacobians; `--schur`, `--predict`, `--floor`, `--tol`, `--fasttrial` are not used (the solver is the one on main; `--schur` is for M >= 7).
- `--xi1` defaults to 0.2: hier's residuals are evaluated at its own radii (xi_top 0.2; the harmonic-3 jump at 0.2), where value_mp, zero_mp and the certificate use xi1 0.17 and 0.3 (the certificate: path to 0.3). A zero of the exact system does not depend on xi1;
  the two models are numerically different codes, so a difference between the converged points is a result.
- `--procs 2` (AGENTS.md: hier.py uses 2 processes at most). The two zeros run side by side, 2 processes each (4 of 8 CPUs), `nice -n 10`, 1 thread per BLAS, `--verbose=2` (every level's solves).
- Output: the last line `ZERO M 3: A .. w/w_inf .. r_1 ..i [seconds, N residuals]` and F_3/F_1, `r_3`; the solve count is the residual count N of that line (`NEV`).
- hier.py prints A and w/w_inf to 9 decimals and F_3/F_1 to 6, which cannot resolve 1e-9 in B3 and C3. So each zero is run **twice**: (1) `hier.py` exactly as above (the record), and (2) `hier_driver.py` (my own driver, `runner/`), which sets the same
  `sys.argv`, wraps `hier.report` so that it also prints the final x and r at full precision (`repr`), and calls `hier.main()` unchanged. Run (2) must reproduce (1)'s printed lines; if it does not, that is reported.

## The starting points and the references (all from files, computed in this README's generator)

| zero | A | w/w_inf | B3 = -2 Im F_3 | C3 = 2 Re F_3 | source |
|---|---|---|---|---|---|
| x1 start | 3.446218246366727 | 0.347606965217407 | 0.8054175863852927 | 0.011780043848505818 | zero_mp last row (zero1 run, raw c31b5d24) and value_mp point F_3 (`I1079-macm3/step1/point_x1.json`) |
| x1 certificate | 3.446218246366727149 | 0.347606965217407386 | 0.805417586385292321 | 0.011780043848505832 | refine `p_out` (numerics, `data/A_M_refine_M3_x1.json`) |
| x2 start | 3.526473056695715 | 0.211497981391215 | 0.9765085451976188 | -0.0017633195225818952 | zero_mp unapplied-step point (zero2 run) and value_mp point F_3 (`step1/point_x2.json`) |
| x2 certificate | 3.526473056695715496 | 0.211497981391215414 | 0.976508545197618541 | -0.00176331952258178 | refine `p_out` (`data/A_M_refine_M3_x2.json`) |

Reported afterwards: hier's converged (A, w/w_inf, B3, C3) beside these, the differences (in A and w/w_inf, and in B3 and C3), hier's residual r_1 and r_3 and its residual count and seconds. A converged point more than about 1e-9 from the start in A or w/w_inf
is reported with its distance and is not adjusted; if hier cannot start or does not converge, the message and the last lines of its log are the result.


## Results (2026-11-23, 14:51:45 to 14:53:27 UTC; each hier run 6 to 13 s on 2 processes)

**Verdict: hier does not converge to either excited zero in the sense of the prediction, and does not contradict it either. Started at each zero it accepts no step in A or w/w_inf (the outer level rejects every trial at its noise floor), and its residuals there are 3 to 4 orders above its residuals at the fundamental zero;
started 3.6e-6 away it lands within 7e-8 (x1) and 4e-8 (x2) of the zero_mp point, so it confirms the zeros at the 1e-7 level, not at the 1e-9 level.**

(1) `hier.py 3 A wf --x=B3,C3 --procs 2 --verbose=2` (the record, `hier/out/hier_plain_x{1,2}.log`) and (2) the same through `hier_driver.py` (`hier_driver_x{1,2}.log`, full precision) give the same printed lines (compared by `diff`, apart from the timings and the FULL lines): x1 `ZERO M 3: A 3.446218246 w/w_inf 0.347606965 ... r_1 +5.8509e-03-4.5483e-04i [87 residuals]`, x2 `ZERO M 3: A 3.526473057 w/w_inf 0.211497981 ... r_1 +2.1770e-02-3.3958e-02i [64 residuals]`.

| run | A | w/w_inf | B3 | C3 | minus the start: A, w/w_inf | minus the start: B3, C3 | \|r_1\|; \|r_3\| (hier, xi 0.2) | residuals; time |
|---|---|---|---|---|---|---|---|---|
| x1, hier from the start | 3.446218246366727 | 0.347606965217407 | 0.8054175863436057 | 0.011780043792103045 | +0.00e+00, +0.00e+00 | -4.17e-11, -5.64e-11 | 5.87e-03; 9.74e-05 | 87; 8 s |
| x2, hier from the start | 3.526473056695715 | 0.211497981391215 | 0.9765085466922837 | -0.0017633213067941044 | +0.00e+00, +0.00e+00 | +1.49e-09, -1.78e-09 | 4.03e-02; 5.60e-03 | 64; 6 s |
| x1, hier from the start moved by (+3e-6, -2e-6) in A, w/w_inf (extra) | 3.446218177255137 | 0.3476069284002131 | 0.8054176094334068 | 0.011780043623226454 | -6.91e-08, -3.68e-08 | +2.30e-08, -2.25e-10 | 1.02e-02; 1.66e-04 | 101; 10 s |
| x2, hier from the start moved by (+3e-6, -2e-6) (extra) | 3.526473034176512 | 0.21149802332627657 | 0.9765084792654547 | -0.00176330244769313 | -2.25e-08, +4.19e-08 | -6.59e-08, +1.71e-08 | 1.54e-01; 6.68e-02 | 158; 13 s |
| the fundamental, hier from the certified centre (extra control) | 2.726475885921854 | 1.0156030950364636 | 0.14441947846771588 | 0.01108742588573784 | +2.91e-10, +1.79e-10 (against the certified centre) | -2.36e-12, -2.38e-12 | 1.58e-06; 4.39e-11 | 46; 8 s |

The starting points are zero_mp's (A, w/w_inf) and value_mp's F_3 (B3 = -2 Im F_3, C3 = 2 Re F_3): x1 (3.446218246366727, 0.347606965217407, 0.8054175863852927, 0.011780043848505818), x2 (3.526473056695715, 0.211497981391215, 0.9765085451976188, -0.0017633195225818952).
The certificate's refine `p_out` (numerics) equals them to 3.3e-16 and 4.4e-16 in A and w/w_inf and to 1e-17 in B3, C3, so the "minus certificate" differences equal the "minus start" ones to those digits (`FULL` values are in the logs).

- **From the start (x1, x2):** A and w/w_inf come back as the start values to the last digit: every trial of the outer level was rejected with a fresh Jacobian ("noise floor": `level 1 (top): stop at |r_1| 5.87e-03` and `4.03e-02`). B3 and C3 moved by -4.2e-11, -5.6e-11 (x1) and +1.5e-9, -1.8e-9 (x2) against value_mp's. The residuals (hier's de-mixed jumps at xi 0.2) are |r_1| 5.9e-3 and 4.0e-2 and |r_3| 9.7e-5 and 5.6e-3, against 1.6e-6 and 4.4e-11 at the fundamental (control).
  The solve counts: 87 and 64 residuals (8 s and 6 s); the level-3 solves inside the outer level stop at the noise floor too ("a fresh Jacobian no longer halves |g|", "every trial rejected with a fresh Jacobian").
- **Why it cannot refine here:** the double-precision residual's noise floor is far above what 1e-9 in A needs. My probe (`hier_probe.py`, read-only: hier's raw residual and its 4 x 4 finite-difference Jacobian with hier's own steps; `hier/out/hier_probe_x*.log`): the raw Jacobian entries are 1e5 to 5e7; the linear Newton step from the start,
  -J^-1 r, is (+2.7e-8, +2.8e-8) in (A, w/w_inf) at x1 with hier's steps and (+5.7e-8, +4.6e-8) with half of them, and (-9.3e-9, +2.0e-9) / (+9.5e-9, +1.0e-8) at x2, i.e. it changes with the finite-difference step by its own size and at x2 in sign. hier resolves A and w/w_inf at the 1e-8 (x2) to 6e-8 (x1) level here, not at 1e-9.
- **From a displaced start (extra):** hier ends at (3.446218177255137, 0.3476069284002131) (x1) and (3.526473034176512, 0.21149802332627657) (x2): 6.9e-8, 3.7e-8 and 2.3e-8, 4.2e-8 from the zero_mp points, with residuals |r_1| 1.0e-2 and 0.15 and |r_3| 1.7e-4 and 6.7e-2. So a start 3.6e-6 away is brought back to within 7e-8, about 50 times closer, and no closer: the same resolution.
- **The fundamental (extra control):** from the certified centre hier ends 2.9e-10 in A and 1.8e-10 in w/w_inf away (B3 and C3: -2.4e-12 each) with |r_1| 1.6e-6 and |r_3| 4.4e-11, so the same code, the same radii and the same procs do converge to the 1e-10 level where the zero is well-conditioned in double precision.

**The prediction (before): "hier converges to each excited zero within about 1e-9 in A and wf, or names why it cannot start there": partly.** hier starts without trouble and does not move A and w/w_inf at all (so it is within 1e-9 of the start in the trivial sense); but it does so by rejecting every trial at its noise floor, with residuals 3 to 4 orders above its fundamental's, and from a displaced start
it lands within 7e-8, not 1e-9. The independent check supports the located zeros at the 1e-7 level and cannot say more, because of hier's double-precision noise floor at these points (the float64 count's located zeros sat at their floors too, in #1021: |F| 16.8 against a floor of 36.1 at x1 and 220.5 against 195.9 at x2, at xi1 0.17).
