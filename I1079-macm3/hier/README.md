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
