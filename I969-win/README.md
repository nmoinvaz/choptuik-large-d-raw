# I969-win: sample c's K = 0 root at D 40.02 moved along the line to sample b by 1e-20 and 1e-19, 12 rough rt_sigma starts at each, and the part of b - c orthogonal to a - c (#969, is the set of roots more than one-dimensional?)

Runner winb on the win laptop (Surface Laptop 4, i7-1185G7, Windows 11). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/969 (coordinator's plan, follows #968). Status: **done** 2026-11-18 22:10:43 UTC, verdict **ALONG THE ROOT SET** by the criteria below (result at the end of this file).

## Question

#968 found that moving sample c along the line to sample a keeps the rough bound at the root's level (medians 7.7e-34, 4.8e-33, 1.7e-32 at delta 1e-20, 1e-19, 1e-18, which is 1e-10 to 1e-12 of #963's random moves). Sample b is not on
that line (cosine of b - c with a - c 0.234, 97% of b - c off it, `I968-win/logs/collinear.log`). The samples' residuals put each within about 1e-28 of the set of roots, far below their 1e-21 separation, so if
b - c is also a null direction, the set of roots near c is at least two-dimensional. Test: move c along the line to b, `rt_perturb.py --along`, and read the rough bounds. Also, from the stored states only, the
component of b - c orthogonal to a - c, its relative size, and mu's share in a - c and in b - c.

## Inputs and code

| item | value |
|---|---|
| code | worktree `C:\Users\nathan\Source\choptuik-i968` (made for #968), detached at main `d96a09a1`. origin/main is `664ef3dd` now, `solver/rt` has no change between the two (`git diff --stat d96a09a1 origin/main -- solver/rt` is empty), so the worktree is not moved |
| C | `I951-win/solves/k0c_D40_mutnorows_D40.0201_32x121.npz` (sample c, K 0, D 40.020065, 32 x 121), sha256 prefix 0c8f3de8 |
| B | `I701-win/solves/k0b_D40_mutnorows_D40.0201_32x121.npz` (sample b, K 0), sha256 prefix b048df8c, the live raw clone's copy equals the push worktree's |
| A | `I671-win/solves/k0_D40_mutnorows_D40.0201_32x121.npz` (sample a, K 0), sha256 prefix a6b9a729, for the orthogonal component |
| interpreter | `venv-t151` (Python 3.10.0, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0, multidouble 0.1.0), `rt_launch.py` and `resource.py` copied from `I968-win/` |
| rt_perturb | run in `venv-t151` (`python -I`), not the system python3 |
| rt_sigma | `rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --rough --starts 12`, cwd `<worktree>/solver/rt`, 2 BLAS threads, BelowNormal, one run at a time, cap 2 h each (as #968) |

The move (rt_perturb --along): z' = z + delta max|z| r in double-double, r = (z_B - z_C) formed in double-double and scaled to max|r| = 1. max|b - c| / max|z| = 2.7086e-20 (`I968-win/logs/collinear.log`),
so delta = 1e-20 lies 0.37 of the way from c to b and 1e-19 runs 3.7 times the distance, past b along the same line.

## Pass criteria (the issue's, fixed before the first run)

m(delta) is a run's median of 12 bounds (geometric mean of the two middle bounds, the convention of #701 to #968). m_rand(delta) is #963's at the same delta: 5.4593e-24 (1e-20), 2.6809e-22 (1e-19)
(`I963-win/README.md`, the issue's 5.46e-24 and 2.68e-22).

- **Along the root set** if m(1e-20) and m(1e-19) are both at most 1e-3 m_rand at the same delta.
- **Not along** if both m / m_rand lie in [0.1, 10].
- **Undecided** otherwise. A run that does not print all 12 bounds (cap) cannot be decided by these criteria and is reported as incomplete.
- Read with #968 (along a - c): "along the root set" for both a - c and b - c makes the set at least two-dimensional (a - c and b - c are independent, the cosine is 0.234).

Reported per run: printed max|F|, the 12 bounds, m, products per start, cap hits (products at the `--max_products` default 250), start 0's mu share of x (the `mu` entry of the `start 0, x / max|x|` line).
From the stored states (read-only, no run): the component of b - c orthogonal to a - c, the sizes and the mu entry of each difference.

## Commands, in order

```
python -I solver/rt/rt_perturb.py --selftest --along            # exit 0, PASS (the tool is #968's, run again)
python -I solver/rt/rt_perturb.py --selftest --along --mutate   # exit 1, FAIL (the control)
python -I solver/rt/rt_perturb.py C states/c_alongb_d$d.npz --delta $d --along B     # d = 1e-20 1e-19   (logs/perturb.log)
python run_969.py                                              # the two runs, one at a time, via start_969.cmd
python orth_969.py                                             # the stored-state part (logs/orth.log)
python table_969.py                                            # tables and verdict
```

## Files

| file | content |
|---|---|
| `run_969.py` | the sequential driver (cap, STOP_969), `--selftest` |
| `table_969.py`, `table_969.txt` | tables and the verdict by the criteria above, `--selftest` with planted logs (every branch, a mutated bar, an incomplete run, #963's medians re-read from `I963-win/logs`) |
| `orth_969.py`, `logs/orth.log` | read-only, no run: a - c, b - c in double-double from the stored K 0 states, the component of b - c orthogonal to a - c, mu's share, `--selftest` with a planted vector and a mutated projection |
| `start_969.cmd` | detached BelowNormal launcher |
| `states/c_alongb_d*.npz` | the two moved states |
| `logs/` | `perturb.log`, `sha256.txt`, `selftests.log`, `c_alongb_d*.log` and `.exit`, `run_969.log`, `run_969.exit`, `orth.log` |

## Result

Started 2026-11-18 20:53:19 UTC (`start_969.cmd`), both runs exit 0, driver exit 0 at 22:10:43 UTC (1 h 17 min: 2312 s, 2332 s). Nothing else of mine ran.
`rt_perturb.py --selftest --along` exit 0 (cosine with the planted difference 1.000000000), `--selftest --along --mutate` exit 1 (`logs/selftests.log`, rerun after the runs, the first pass printed the same). The two moved states
realised 1.000000e-20 and 1.000000e-19 of max|z| 0.1291061, along C to B with max|B - C| / max|z| = 2.708562e-20.

**Verdict: ALONG THE ROOT SET.** m(1e-20) and m(1e-19) are 2.9e-10 and 1.8e-11 of m_rand at the same delta, the bar is 1e-3. With #968 (a - c along a family) and the cosine 0.234 between a - c and b - c,
the set of roots near c is at least two-dimensional by the issue's reading.

| run | delta | printed max abs F | m (median of 12) | m_rand (#963) | m / m_rand | products per start | starts at the 250 cap | start 0 mu share of x |
|---|---|---|---|---|---|---|---|---|
| c_alongb_d1e-20 | 1e-20 | 1.16e-30 | 1.5836e-33 | 5.4593e-24 | 2.901e-10 | 67 (all 12) | 0 of 12 | +0.602 |
| c_alongb_d1e-19 | 1e-19 | 3.27e-30 | 4.8112e-33 | 2.6809e-22 | 1.795e-11 | 67 (all 12) | 0 of 12 | +0.541 |

The 12 bounds of each run are in `table_969.txt`. Their best-to-worst spread is a factor 11.0 and 13.3. The worst max|J x - v| is 3.9e-19 and 5.2e-20.

Against #968 (c along a - c, same 12 right-hand sides, same delta):

| delta | m along b - c | m along a - c | ratio | printed max abs F along b - c | along a - c | start 0 mu share along b - c | along a - c |
|---|---|---|---|---|---|---|---|
| 1e-20 | 1.584e-33 | 7.673e-34 | 2.06 | 1.16e-30 | 1.09e-30 | +0.602 | -1.00 |
| 1e-19 | 4.811e-33 | 4.754e-33 | 1.01 | 3.27e-30 | 5.20e-30 | +0.541 | +0.893 |

The bound along the line: c 1.480e-35 (#963 control, printed max|F| 6.91e-31), delta 1e-20 (0.37 of the way to b) 1.584e-33, b 2.610e-33 (#951's table, win2's K 0), delta 1e-19 (3.7 times the distance, past b) 4.811e-33.

The stored-state part (`logs/orth.log`, no run), D 40.020065, 13665 entries, mu the last entry:

| vector | max-norm / max abs z | 2-norm / max abs z | mu entry | mu / max-norm | mu^2 / 2-norm^2 |
|---|---|---|---|---|---|
| a - c | 1.6958e-20 | 1.9273e-19 | -2.1893e-21 | 1.0000 | 7.74e-03 |
| b - c | 2.7086e-20 | 9.1319e-19 | -3.4969e-21 | 1.0000 | 8.80e-04 |
| o, b - c orthogonal to a - c | 1.6461e-20 | 8.8790e-19 | -1.0724e-21 | 0.5046 | 8.75e-05 |

b - c = 1.1074 (a - c) + o. The cosine of a - c and b - c is 0.233729, o is 0.9723 of b - c in 2-norm and 0.6078 in max-norm, and the cosine of o with a - c is 1.1e-16.
Share of the squared 2-norm by block:

| vector | w1 half | w2 | w3 | w4 | mu |
|---|---|---|---|---|---|
| a - c | 3.24e-03 | 0.1065 | 0.3859 | 0.4967 | 7.74e-03 |
| b - c | 1.08e-03 | 0.1535 | 0.1628 | 0.6817 | 8.80e-04 |
| o | 2.21e-03 | 0.1981 | 0.1785 | 0.6212 | 8.75e-05 |

Observations beyond the criteria:
- mu is the largest entry of both a - c and b - c (max-norm share 1.0000), so the max-norm distances #951 reported, 2.189e-21 and 3.497e-21, are mu's differences. In the 2-norm mu is under 1% of either difference, which lives mostly in w2 to w4 (w4 is 50% and 68%). o's mu entry is half its max-norm and 9e-5 of its squared 2-norm.
- The two lines read alike. At 1e-19 along b - c is within 1.2% of along a - c (4.81e-33 against 4.75e-33), at 1e-20 within a factor 2.1, and both are 1e-10 to 1e-11 of the random move. From 1e-20 to 1e-19 the bound along b - c grows 0.48 decade, along a - c 0.79.
- Start 0's mu share of x is +0.60 and +0.54 along b - c, -1.00 and +0.89 along a - c (the same right-hand side, so the sign and size of mu in x differ with the state).
- What the runs test: the Jacobian's smallest gain at points on the lines c to a and c to b (and the rays past them). They do not sample a point inside the plane through a, b, c, and they read the bound for 12 right-hand sides, not the kernel of J. The three samples are not collinear (cosine 0.234), and the residuals of both moved states are at the floor, 1.2e-30 and 3.3e-30.

