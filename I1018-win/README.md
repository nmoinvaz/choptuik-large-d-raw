# I1018-win: sample c's K = 0 root at D 40.02 moved along the two deep directions out of the samples' plane by 1e-20 and 1e-19, 12 rough rt_sigma starts at each (#1018, are they tangent to the root set?)

Runner winb on the win laptop (Surface Laptop 4, i7-1185G7, Windows 11). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1018 (coordinator's plan, P7, follows #1006). Status: **done** 2026-11-19 11:55:43 UTC, reading **TANGENT** by the criteria below (result at the end of this file).

## Question

#1006 found d = 4 deep directions at D 40.02, one subspace at samples a, b and c (principal angles below 0.005 degrees, `rt_angles.py`). The chords a - c and b - c lie in it and are tangent (#968, #969, #972), so the root set is at least two-dimensional there. The other two directions of the span are untested.
`rt_angles.py --complement` gives them: an orthonormal pair q_0, q_1 in the span of p_1 .. p_4 of #1006's `T1_c24.npz`, orthogonal to the plane of a - c and b - c. `rt_perturb.py --dir Q --dir_k k` moves c along row k by delta max|z| (the row scaled to max-norm 1), delta = 1e-20 and 1e-19. Each of the four moved states is read with `rt_sigma.py --rough --starts 12` as in #972.
If both directions are tangent the root set is four-dimensional, and (H4)'s rows at k = 1/2 and 3/2 (four real conditions) are stage 2. If not, only two conditions are missing and the other two deep directions are weak but not roots.

## Inputs and code

| item | value |
|---|---|
| code | worktree `C:\Users\nathan\Source\choptuik-i1018` (new), detached at main `7745882e` (rt_angles --complement, rt_perturb --dir). `solver/rt/rt_sigma.py` and `rt_xcount.py` are unchanged from `c6c1ee6a` (#985, #1006) |
| C | `I951-win/solves/k0c_D40_mutnorows_D40.0201_32x121.npz` (sample c, K 0, D 40.020065, 32 x 121), sha256 prefix 0c8f3de8 |
| A | `I671-win/solves/k0_D40_mutnorows_D40.0201_32x121.npz` (sample a), sha256 prefix a6b9a729 |
| B | `I701-win/solves/k0b_D40_mutnorows_D40.0201_32x121.npz` (sample b), sha256 prefix b048df8c |
| x file | `I1006-win/x/T1_c24.npz` (24 starts at c, d = 4), sha256 prefix e843aaae |
| interpreter | `venv-t151` (Python 3.10.0, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0, multidouble 0.1.0), `rt_launch.py` and `resource.py` copied from `I972-win/` for rt_sigma, `python -I` for rt_perturb and rt_angles |
| rt_sigma | `rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --rough --starts 12`, cwd `<worktree>/solver/rt`, 2 BLAS threads, BelowNormal, one run at a time, cap 2 h each |

The 12 rough right-hand sides are the same for every state (default_rng(163)), so the runs compare with #963's random moves (the m_rand below) and #972's in-plane moves. The chords' sizes (max-norm over max|z_C| 0.1291061): a - c 1.6958e-20, b - c 2.7086e-20, so 1e-20 is a move of the chords' size and 1e-19 is about 6 times it.

## Readings (the issue's, fixed before the first run)

m(row, delta) is a run's median of 12 bounds (geometric mean of the two middle bounds, the convention of #701 to #1006). m_rand(delta) is #963's at the same delta: 5.4593e-24 (1e-20), 2.6809e-22 (1e-19) (`I963-win/README.md`, the issue's 5.46e-24 and 2.68e-22).

- **Tangent** if all four m (rows 0 and 1, 1e-20 and 1e-19) are at most 1e-3 m_rand at the same delta.
- **Not tangent** if any of the four m / m_rand lies in [0.1, 10].
- **Undecided** otherwise.
- A run that does not print all 12 bounds (cap) cannot be decided by these criteria and is reported as incomplete.

Reported per run: printed max|F|, the 12 bounds, m, products per start, cap hits (products at the `--max_products` default 250), start 0's mu share of x.
Checks of the moves themselves from the stored states (read-only, `check_1018.py`, not part of the readings): each move's realised size, its parallelism to its row of Q, its part in the plane of a - c and b - c, its part outside the deep span, and three kinds of control that must fail.

## Commands, in order

```
python -I rt_perturb.py --selftest --dir                          # exit 0, PASS (the issue's, first; plus the other selftests of rt_perturb and rt_angles, logs/selftests.log)
python -I rt_angles.py I1006-win/x/T1_c24.npz --complement C --chords A,B --write Q_c24.npz    # "2 directions ... ok" (logs/complement.log)
python -I rt_perturb.py C states/c_q${k}_d${d}.npz --delta $d --dir Q_c24.npz --dir_k $k      # k = 0 1, d = 1e-20 1e-19 (logs/perturb.log)
python -I check_1018.py                                           # the moves against the plane, the span and the controls (logs/check.log)
python run_1018.py                                                # the four runs, one at a time, via start_1018.cmd (q0 1e-20, q0 1e-19, q1 1e-20, q1 1e-19)
python table_1018.py                                              # tables and the reading
```

The first try of the rt_angles command in git bash gave `--chords A,B` as POSIX paths, which the shell converted only for the first path (FileNotFoundError on the second, no file written). The command above, with `C:/...` paths, is the one that ran.

## Files

| file | content |
|---|---|
| `Q_c24.npz` | rt_angles `--write`: `q` (2 x 13665, orthonormal rows q_0, q_1), `x`, `root`, `chords` |
| `run_1018.py` | the sequential driver (cap, STOP_1018), `--selftest` |
| `table_1018.py`, `table_1018.txt` | tables and the reading by the criteria above, `--selftest` (every branch, mutated bar, mutated "any" rule, an incomplete run, #963's medians re-read from `I963-win/logs`) |
| `check_1018.py`, `logs/check.log` | read-only, no run: the four moved states against the stored samples, Q and the deep span of `T1_c24.npz`, four control states that must fail, `--selftest` with planted vectors |
| `start_1018.cmd`, `rt_launch.py`, `resource.py` | detached BelowNormal launcher, the multidouble and fma shim, the `resource` shim (from `I972-win/`) |
| `states/c_q{0,1}_d{1e-20,1e-19}.npz` | the four moved states |
| `logs/` | `selftests.log`, `complement.log`, `perturb.log`, `check.log`, `sha256.txt` (A, B, C, `T1_c24.npz`, worktree commit), `c_q{0,1}_d*.log` and `.exit`, `run_1018.log`, `run_1018.exit` |

## Result

Started 2026-11-19 09:21:16 UTC (`start_1018.cmd`), all four runs exit 0, driver exit 0 at 11:55:43 UTC (2 h 34 min: 2332 s, 2322 s, 2312 s, 2302 s). Nothing else of mine ran.
`rt_perturb.py --selftest --dir` exit 0 (first), then the other eight selftests of rt_perturb and rt_angles as wanted (0, 1, 0, 0, 0, 1, 0, 1), and the selftests of `check_1018.py`, `table_1018.py` and `run_1018.py` pass (`logs/selftests.log`).
`rt_angles.py --complement`: chords a - c and b - c share 1.000000 and 1.000000 in the d = 4 span, "2 directions out of the chords' plane: largest cosine with the chords 1.1e-15, part outside the span 1.9e-15: ok". The rows q_0 and q_1 have norm 1 and q_0 . q_1 = -9.0e-17.
`check_1018.py` passes: the four moved states realised 1.000000e-20 and 1.000000e-19 of max|z|, equal to their row of Q (max abs of d / max abs d - q / max abs q 3e-13 to 3e-14), in the plane of a - c and b - c to 4e-15 at most, outside the deep span 2.8e-13 at most, and the four controls fail as they must (#972's sum moves lie in the plane, part 1.00, and #963's random moves lie outside the span, part 1.00).

**Reading: TANGENT.** The four m are 1.4e-10, 1.5e-11, 3.9e-10 and 1.3e-12 of m_rand at the same delta, the bar is 1e-3 for each and the "not tangent" band [0.1, 10] is 8 to 11 decades above.

| run | row | delta | printed max abs F | m (median of 12) | m_rand (#963) | m / m_rand | products per start | starts at the 250 cap | start 0 mu share of x |
|---|---|---|---|---|---|---|---|---|---|
| c_q0_d1e-20 | 0 | 1e-20 | 1.39e-30 | 7.3744e-34 | 5.4593e-24 | 1.351e-10 | 67 (all 12) | 0 of 12 | -1.00 |
| c_q0_d1e-19 | 0 | 1e-19 | 5.33e-30 | 3.9858e-33 | 2.6809e-22 | 1.487e-11 | 67 (all 12) | 0 of 12 | +1.00 |
| c_q1_d1e-20 | 1 | 1e-20 | 2.34e-29 | 2.1019e-33 | 5.4593e-24 | 3.850e-10 | 67 (all 12) | 0 of 12 | -1.00 |
| c_q1_d1e-19 | 1 | 1e-19 | 2.34e-28 | 3.4795e-34 | 2.6809e-22 | 1.298e-12 | 67 (all 12) | 0 of 12 | +0.574 |

The 12 bounds of each run are in `table_1018.txt`. Their best-to-worst spread is a factor 40.0, 10.6, 20.4 and 15.0. The worst max|J x - v| is 3.3e-18, 8.0e-21, 2.4e-18 and 2.1e-19.

The six directions that have been read from c, same 12 right-hand sides and the same delta (a - c is #968, b - c is #969, orth and sum are #972):

| direction | m at 1e-20 | m at 1e-19 | printed max abs F at 1e-20 | at 1e-19 | start 0 mu share of x at 1e-20 | at 1e-19 |
|---|---|---|---|---|---|---|
| a - c | 7.673e-34 | 4.754e-33 | 1.09e-30 | 5.20e-30 | -1.00 | +0.893 |
| b - c | 1.584e-33 | 4.811e-33 | 1.16e-30 | 3.27e-30 | +0.602 | +0.541 |
| orth | 3.973e-33 | 1.127e-32 | 9.75e-31 | 6.67e-30 | -1.00 | +0.280 |
| sum | 2.334e-33 | 2.254e-33 | 1.19e-30 | 3.04e-30 | -1.00 | +0.931 |
| q_0 (out of the plane) | 7.374e-34 | 3.986e-33 | 1.39e-30 | 5.33e-30 | -1.00 | +1.00 |
| q_1 (out of the plane) | 2.102e-33 | 3.480e-34 | 2.34e-29 | 2.34e-28 | -1.00 | +0.574 |
| random (#963) | 5.459e-24 | 2.681e-22 | 3.36e-18 | 3.36e-17 | | |

Observations beyond the criteria:
- All four moves read 3.5e-34 to 4.0e-33, inside the 1e-35 to 1e-32 range of the in-plane moves (#951's three samples read c 1.5e-35, a 2.7e-34, b 2.6e-33). The largest m / m_rand is 3.9e-10.
- The printed max|F| of q_1 is 2.34e-29 at 1e-20 and 2.34e-28 at 1e-19, linear in delta, which is 20 to 77 times the in-plane moves' at the same delta (1e-30 to 7e-30) and 7e-12 of the random move's (3.36e-17 at 1e-19). q_0's is 1.4e-30 and 5.3e-30, like the in-plane moves. I did not investigate it. The rows come from a double-precision SVD of the stored x, and the check shows their part outside the span at 2.7e-14 to 2.8e-13 of each move.
- From 1e-20 to 1e-19 m grows 0.73 decade along q_0 and falls 0.78 decade along q_1 (2.1e-33 to 3.5e-34, which is 24 times the unmoved c's m0 = 1.48e-35 from #963 and #985). The criteria compare with the random move only.
- The in-plane differences are led by mu (the sum move has mu / max-norm 1.0000 in `check.log`), the two out-of-plane rows are not (0.0151 and 0.0250 of the move's max-norm).
- What the runs test: the Jacobian's smallest gain, bounded by 12 right-hand sides, at points on one ray along each of q_0 and q_1 from c (the sign of a singular vector is arbitrary, so the opposite rays are not read), out to 1e-19 of max|z|. The chords' sizes are 1.7e-20 and 2.7e-20, so 1e-19 is past them. The runs do not resolve curvature, and the bound is not the kernel of J. They read at c only, not at a or b.
