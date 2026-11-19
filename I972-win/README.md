# I972-win: sample c's K = 0 root at D 40.02 moved inside the plane of samples a, b, c (the part of b - c orthogonal to a - c, and the sum of the unit differences) by 1e-20 and 1e-19, 12 rough rt_sigma starts at each (#972, is the whole plane tangent to the root set?)

Runner winb on the win laptop (Surface Laptop 4, i7-1185G7, Windows 11). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/972 (coordinator's plan, follows #969). Status: **done** 2026-11-19 00:51:55 UTC, verdict **IN THE ROOT SET** by the criteria below (result at the end of this file).

## Question

#968 and #969 found a - c and b - c each tangent to the root set: moves of sample c toward a or b keep the rough bound 1e-10 to 1e-12 below a random move's. The two differences are far from parallel (cosine 0.234).
Two moves inside their plane test whether every direction in it is tangent, as a two-dimensional root set requires. A union of two curves through c would leave other directions in the plane non-tangent.
The moves, `rt_perturb.py --along A --along2 B --mode orth|sum`: orth is the part of b - c orthogonal (2-norm) to a - c, sum is (a - c) / max|a - c| + (b - c) / max|b - c|, both scaled to max = 1 and times delta max|z|.

## Inputs and code

| item | value |
|---|---|
| code | worktree `C:\Users\nathan\Source\choptuik-i972`, detached at main `41fe9573` (rt_perturb: --along2, --mode). `solver/rt` differs from #969's `d96a09a1` only in `rt_perturb.py` |
| C | `I951-win/solves/k0c_D40_mutnorows_D40.0201_32x121.npz` (sample c, K 0, D 40.020065, 32 x 121), sha256 prefix 0c8f3de8 |
| A | `I671-win/solves/k0_D40_mutnorows_D40.0201_32x121.npz` (sample a, K 0), sha256 prefix a6b9a729 |
| B | `I701-win/solves/k0b_D40_mutnorows_D40.0201_32x121.npz` (sample b, K 0), sha256 prefix b048df8c |
| interpreter | `venv-t151` (Python 3.10.0, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0, multidouble 0.1.0), `rt_launch.py` and `resource.py` copied from `I969-win/` |
| rt_perturb | run in `venv-t151` (`python -I`), not the system python3 |
| rt_sigma | `rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --rough --starts 12`, cwd `<worktree>/solver/rt`, 2 BLAS threads, BelowNormal, one run at a time, cap 2 h each (as #963, #968, #969) |

Sizes from `I969-win/logs/orth.log` (max-norm over max|z| 0.1291061): a - c 1.6958e-20, b - c 2.7086e-20, the orth part 1.6461e-20 (cosine of a - c and b - c 0.2337). So delta = 1e-20 is a move of 0.61 times the orth part's size and 1e-19 of 6.1 times.

## Pass criteria (the issue's, fixed before the first run)

m(mode, delta) is a run's median of 12 bounds (geometric mean of the two middle bounds, the convention of #701 to #969). m_rand(delta) is #963's at the same delta: 5.4593e-24 (1e-20), 2.6809e-22 (1e-19)
(`I963-win/README.md`, the issue's 5.46e-24 and 2.68e-22).

- **In the root set** if all four m (orth and sum, 1e-20 and 1e-19) are at most 1e-3 m_rand at the same delta.
- **Not** if any of the four m / m_rand lies in [0.1, 10].
- **Undecided** otherwise.
- A run that does not print all 12 bounds (cap) cannot be decided by these criteria and is reported as incomplete.

Reported per run: printed max|F|, the 12 bounds, m, products per start, cap hits (products at the `--max_products` default 250), start 0's mu share of x (the `mu` entry of the `start 0, x / max|x|` line).
Checks of the moves themselves from the stored states (read-only, `check_972.py`, not part of the criteria): the cosine of each move with a - c, its part outside the plane of a - c and b - c, and the control that the
check rejects #969's along-b move as an orth move.

## Commands, in order

```
python -I solver/rt/rt_perturb.py --selftest --orth          # exit 0, PASS (the issue's)
python -I solver/rt/rt_perturb.py C states/c_${m}_d$d.npz --delta $d --along A --along2 B --mode $m    # m = orth sum, d = 1e-20 1e-19   (logs/perturb.log)
python check_972.py                                          # the moves against the plane (logs/check.log)
python run_972.py                                            # the four runs, one at a time, via start_972.cmd (orth 1e-20, orth 1e-19, sum 1e-20, sum 1e-19)
python table_972.py                                          # tables and verdict
```

## Files

| file | content |
|---|---|
| `run_972.py` | the sequential driver (cap, STOP_972), `--selftest` |
| `table_972.py`, `table_972.txt` | tables and the verdict by the criteria above, `--selftest` with planted logs (every branch, a mutated bar, a mutated "any" rule, an incomplete run, #963's medians re-read from `I963-win/logs`) |
| `check_972.py`, `logs/check.log` | read-only, no run: the four moved states against the stored samples (cosines with a - c and b - c, the part outside the plane, the deviation from the sum direction) and two controls, `--selftest` with planted vectors |
| `start_972.cmd` | detached BelowNormal launcher |
| `states/c_{orth,sum}_d*.npz` | the four moved states |
| `logs/` | `perturb.log`, `sha256.txt`, `selftests.log`, `check.log`, `c_{orth,sum}_d*.log` and `.exit`, `run_972.log`, `run_972.exit` |

## Result

Started 2026-11-18 22:17:38 UTC (`start_972.cmd`), all four runs exit 0, driver exit 0 at 2026-11-19 00:51:55 UTC (2 h 34 min: 2322 s, 2322 s, 2312 s, 2302 s). Nothing else of mine ran.
`rt_perturb.py --selftest --orth` exit 0 (cosine with d1 1.9e-12, part outside the plane 2.7e-10, `logs/selftests.log`). The four moved states realised 1.000000e-20 and 1.000000e-19 of max|z| 0.1291061 in both modes.
`check_972.py` passes: the orth moves have cosine +2.4e-16 and -2.8e-17 with a - c and lie in the plane to 1.2e-13 and 1.2e-14, the sum moves deviate from (a - c) / max|a - c| + (b - c) / max|b - c| by 3.6e-13 and 3.3e-14,
and both controls fail as they must (#969's along-b moves as orth moves, cosine 0.2337 with a - c; the orth moves as sum moves, deviation 0.82).

**Verdict: IN THE ROOT SET.** The four m are 7.3e-10, 4.2e-11, 4.3e-10 and 8.4e-12 of m_rand at the same delta, the bar is 1e-3 for each.

| run | mode | delta | printed max abs F | m (median of 12) | m_rand (#963) | m / m_rand | products per start | starts at the 250 cap | start 0 mu share of x |
|---|---|---|---|---|---|---|---|---|---|
| c_orth_d1e-20 | orth | 1e-20 | 9.75e-31 | 3.9732e-33 | 5.4593e-24 | 7.278e-10 | 67 (all 12) | 0 of 12 | -1.00 |
| c_orth_d1e-19 | orth | 1e-19 | 6.67e-30 | 1.1266e-32 | 2.6809e-22 | 4.202e-11 | 67 (all 12) | 0 of 12 | +0.280 |
| c_sum_d1e-20 | sum | 1e-20 | 1.19e-30 | 2.3335e-33 | 5.4593e-24 | 4.274e-10 | 67 (all 12) | 0 of 12 | -1.00 |
| c_sum_d1e-19 | sum | 1e-19 | 3.04e-30 | 2.2542e-33 | 2.6809e-22 | 8.408e-12 | 67 (all 12) | 0 of 12 | +0.931 |

The 12 bounds of each run are in `table_972.txt`. Their best-to-worst spread is a factor 6.9, 9.2, 20.8 and 12.0. The worst max|J x - v| is 2.0e-19, 5.9e-21, 1.4e-19 and 2.0e-20.

The four directions of the plane that have been read, same 12 right-hand sides and the same delta (a - c is #968, b - c is #969):

| direction | m at 1e-20 | m at 1e-19 | printed max abs F at 1e-20 | at 1e-19 | start 0 mu share of x at 1e-20 | at 1e-19 |
|---|---|---|---|---|---|---|
| a - c | 7.673e-34 | 4.754e-33 | 1.09e-30 | 5.20e-30 | -1.00 | +0.893 |
| b - c | 1.584e-33 | 4.811e-33 | 1.16e-30 | 3.27e-30 | +0.602 | +0.541 |
| orth (b - c minus its part along a - c) | 3.973e-33 | 1.127e-32 | 9.75e-31 | 6.67e-30 | -1.00 | +0.280 |
| sum (unit a - c plus unit b - c) | 2.334e-33 | 2.254e-33 | 1.19e-30 | 3.04e-30 | -1.00 | +0.931 |
| random (#963) | 5.459e-24 | 2.681e-22 | 3.36e-18 | 3.36e-17 | | |

Observations beyond the criteria:
- All four moves read 1e-33 to 1e-32, the range of #968 and #969 and the spread of #951's three samples (a 2.7e-34, b 2.6e-33, c 1.5e-35), and the largest, orth at 1e-19, is 4.2e-11 of the random move at that size. The printed max|F| stays at 1e-30 to 7e-30.
- The two deltas are 0.61 and 6.1 times the orth part's size (max-norm 1.646e-20 of max|z|). From 1e-20 to 1e-19 the bound grows 0.45 decade along orth and is flat along sum (-0.015 decade), against 0.79 and 0.48 along a - c and b - c.
- Start 0's mu share of x is -1.00 at 1e-20 in three of the four runs (+0.60 along b - c) and +0.28 to +0.93 at 1e-19.
- What the runs test: the Jacobian's smallest gain, bounded by 12 right-hand sides, at points on four rays from c inside the plane through a, b, c (a - c, b - c, orth, sum), out to 1e-19 of max|z|. The sizes a - c, b - c, orth are 1.7e-20, 2.7e-20 and 1.6e-20, so a delta of 1e-19 is past all of them. The runs do not resolve the curvature of a surface or other directions out of the plane, and the bound is not the kernel of J.

